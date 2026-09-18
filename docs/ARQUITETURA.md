# Arquitetura

Como o sistema está organizado, por que ficou assim e o que você precisa saber
antes de mexer.

Para **o que** o sistema faz, leia [REGRAS_DE_NEGOCIO.md](REGRAS_DE_NEGOCIO.md).

---

## O ponto de partida

O sistema original era um único método, `att`, com complexidade ciclomática 19,
seis níveis de aninhamento e a regra dos cinco tipos de item entrelaçada em 29
linhas. Ele funcionava. O problema era que ninguém conseguia mudá-lo com
segurança.

Depois da refatoração, nenhuma função passa de complexidade 4 nem de dois
níveis de aninhamento.

---

## Os módulos

| Módulo | Responsabilidade |
| --- | --- |
| `gilded_rose/item.py` | Guarda estado. Nenhuma regra de negócio. |
| `gilded_rose/rules.py` | Constantes do domínio: limites, prazos, nomes. |
| `gilded_rose/quality.py` | As três operações possíveis sobre qualidade. |
| `gilded_rose/updaters.py` | Uma classe por regra de envelhecimento. |
| `gilded_rose/registry.py` | Descobre qual updater cuida de cada item. |
| `gilded_rose/inventory.py` | Percorre o inventário ao final do dia. |
| `legacy/` | O código original, congelado. Não é usado em produção. |

O fluxo de um dia é curto: `GildedRose.update_quality()` percorre os itens,
pergunta ao registro quem cuida de cada um, e delega.

---

## Três decisões que explicam o resto

### 1. Ninguém altera `item.quality` diretamente

Toda mudança passa por `quality.increase`, `quality.decrease` ou
`quality.drop_to_zero`. No código original, o par "checa o limite / soma ou
subtrai 1" aparecia **sete vezes**, e bastava esquecer uma para furar o teto de
50 ou deixar a qualidade negativa.

Centralizando, os limites deixam de depender de disciplina: eles são garantidos
por construção. Um updater não *consegue* violá-los.

### 2. Cada tipo de item é uma classe, e elas não se conhecem

No original, para saber o que acontecia com o Aged Brie era preciso ler as
regras de todos os outros itens, porque estavam misturadas nos mesmos `if`s.
Hoje `AgedBrieUpdater` sabe apenas da própria regra.

A classe base define o formato de um dia — muda a qualidade, depois avança o
prazo — e cada subclasse preenche só a parte que lhe cabe.

### 3. Adicionar um tipo novo não exige alterar código existente

O registro funciona por decorator. Um tipo novo é uma classe nova:

```python
@register
class FrozenItemUpdater(ItemUpdater):
    @staticmethod
    def matches(name):
        return name.startswith("Frozen")

    def _change_quality(self, item):
        pass  # itens congelados não mudam
```

Não há um `if/elif` central para crescer a cada item. Itens não reconhecidos
caem no updater padrão. É assim que os itens conjurados entraram, e há um teste
que garante que continua funcionando.

---

## A ordem das operações importa

A qualidade muda **antes** de o prazo avançar, considerando os dias que ainda
restavam. Essa é a ordem do sistema original, e não é um detalhe cosmético: é o
que faz um ingresso com `sell_in = 1` ganhar 3 de qualidade antes de virar pó no
dia seguinte.

Um item está vencido quando `sell_in <= 0` no início do dia — ou seja, o dia em
que `sell_in` chega a 0 ainda é um dia normal de venda.

---

## Quatro comportamentos que a documentação de regras não descreve

O código original faz coisas que o documento de regras contradiz. A refatoração
preserva **o código**, não o documento, porque é o código que está em produção.

| Situação | O que acontece | O que as regras dizem |
| --- | --- | --- |
| Item comum com qualidade 80 | cai para 78 | "nunca acima de 50" |
| Aged Brie com qualidade 80 | permanece em 80 | — |
| Sulfuras com qualidade 10 | permanece em 10 | "fixo em 80" |
| Ingresso vencido | zera, venha de onde vier | idem |

A causa é a mesma nos quatro casos: **o teto de 50 só é verificado ao aumentar a
qualidade, nunca ao diminuir**. Um item que chega acima do teto nunca é puxado
para baixo até ele; apenas para de valorizar.

Se um dia o negócio decidir que esses casos devem mudar, isso é uma mudança de
comportamento deliberada — e vai quebrar o teste de caracterização, como deve.

---

## Os testes, e por que são dois tipos

```
python3 -m unittest discover -s tests -t .
```

São 36 testes, sem dependências além da biblioteca padrão.

**`test_characterization.py` prova que nada mudou.** Ele importa o código de
`legacy/` e compara as duas implementações em cerca de nove mil combinações de
nome, `sell_in` (-10 a 20) e qualidade (0 a 55, mais 80 e 100), além de trinta
dias consecutivos de trajetória e do inventário completo. É o que permitiu
reescrever tudo sem medo.

**`test_business_rules.py` documenta o que o sistema faz.** Está escrito na
linguagem do domínio e sobrevive se o código legado for apagado.

Os dois se complementam: o primeiro tem cobertura enorme e legibilidade zero; o
segundo, o oposto.

### Por que `legacy/` continua no repositório

Ele é a fonte de verdade do teste de caracterização. **Não altere aquele
código** — se ele mudar, o teste deixa de provar qualquer coisa.

Quando o sistema estiver estável e a confiança for suficiente, a pasta pode ser
removida junto com `test_characterization.py`. Os testes de regra de negócio
cobrem o comportamento sozinhos, mas a rede de segurança para refatorações
futuras vai junto.

---

## A única divergência intencional

Itens conjurados degradam duas vezes mais rápido que itens comuns: perdem 2 de
qualidade por dia e 4 depois de vencidos. O código original os tratava como
itens comuns.

Por ser comportamento novo, eles ficam **de fora** do teste de caracterização, e
a divergência é registrada em um teste próprio — para que ninguém a confunda com
uma regressão.
