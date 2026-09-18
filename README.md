# Gilded Rose

Sistema de controle de estoque de uma estalagem fictícia chamada **Gilded Rose**, responsável por atualizar diariamente a **qualidade** e o **prazo de validade** (`sell_in`) dos itens vendidos.

Este repositório é a refatoração de um código legado: o comportamento original foi preservado e provado por testes, e sobre ele entrou uma feature nova, os itens conjurados.

## 📋 O que o programa faz

Todo item possui três atributos:

- **name**: nome do item
- **sell_in**: quantos dias restam para vender o item
- **quality**: o quão valioso o item é (varia normalmente entre **0 e 50**; o Sulfuras, lendário, fica em **80**)

A cada "dia" que passa (ou seja, a cada chamada do método `update_quality`), o programa atualiza esses valores automaticamente, seguindo regras diferentes dependendo do tipo do item.

## 🧪 Regras de atualização

| Item | Comportamento |
|---|---|
| **Item comum** | Perde 1 de qualidade por dia. Após o `sell_in` vencer, perde 2 por dia. Nunca fica abaixo de 0. |
| **Aged Brie** | Ganha qualidade com o tempo, ao invés de perder. Após vencer, ganha o dobro. Nunca passa de 50. |
| **Backstage passes** | Ganha qualidade conforme o show se aproxima: +1 por dia, +2 faltando 10 dias ou menos, +3 faltando 5 ou menos. Após o show, a qualidade cai para **0** — o passe não vale mais nada. |
| **Sulfuras, Hand of Ragnaros** | Item lendário: nunca muda de qualidade nem de `sell_in`. |
| **Conjurado** (ex.: `Conjured Mana Cake`) | Degrada duas vezes mais rápido que um item comum: perde 2 por dia, e 4 após vencer. Nunca fica abaixo de 0. |

As regras completas, com os casos de borda, estão em [docs/REGRAS_DE_NEGOCIO.md](docs/REGRAS_DE_NEGOCIO.md).

> ⚠️ Em alguns casos o código original contradiz esse documento — por exemplo, um item comum que começa com qualidade 80 cai para 78, em vez de ser limitado a 50. A refatoração preserva o comportamento do código. Os quatro casos estão explicados em [docs/ARQUITETURA.md](docs/ARQUITETURA.md).

## 📁 Estrutura do projeto

```
.
├── gilded_rose/            # Código principal
│   ├── item.py             #   o Item: só guarda estado
│   ├── inventory.py        #   GildedRose: percorre o estoque a cada dia
│   ├── updaters.py         #   uma classe com a regra de cada tipo de item
│   ├── registry.py         #   descobre qual classe cuida de cada item
│   ├── quality.py          #   aumenta/diminui qualidade respeitando 0 e 50
│   └── rules.py            #   constantes compartilhadas por todos os tipos
├── legacy/                 # O código original, congelado (usado só nos testes)
├── tests/                  # Testes automatizados
├── docs/                   # Regras de negócio e arquitetura
├── main.py                 # Simulação de alguns dias no terminal
└── README.md               # Este arquivo
```

## ⚙️ Instalação

Não há dependências externas — o projeto usa apenas Python puro, inclusive nos testes.

Requisitos:
- Python 3 (testado no 3.14)

Basta clonar o repositório.

## ▶️ Como rodar

Para ver o estoque mudando dia a dia no terminal:

```bash
python3 main.py        # 2 dias
python3 main.py 10     # 10 dias
```

Para usar as classes no seu próprio código, importe-as do pacote `gilded_rose`:

```python
from gilded_rose import Item, GildedRose

# Cria a lista de itens do estoque
itens = [
    Item("Aged Brie", sell_in=2, quality=0),
    Item("Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
    Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
    Item("Elixir of the Mongoose", sell_in=5, quality=7),
    Item("Conjured Mana Cake", sell_in=3, quality=6),
]

estoque = GildedRose(itens)

# Simula a passagem de um dia
estoque.update_quality()

# Mostra o estado atual dos itens
for item in itens:
    print(item)
```

Para simular vários dias, basta chamar `update_quality()` várias vezes (por exemplo, dentro de um loop `for` ou `while`).

## ✅ Testes

```bash
python3 -m unittest discover -s tests -t .
```

São duas camadas:

- **`test_characterization.py`** compara o sistema novo com o código de `legacy/` em cerca de nove mil combinações de item, `sell_in` e qualidade, dia após dia. É a prova de que a refatoração não mudou o comportamento.
- **`test_business_rules.py`** descreve as regras na linguagem do negócio, uma por teste.

## 🚀 Funcionalidades

- Atualização automática de qualidade e prazo de venda
- Suporte a 5 tipos diferentes de item, cada um com sua própria classe e regra
- Garantia de que a qualidade nunca fica negativa nem ultrapassa 50 ao valorizar
- Novos tipos de item entram sem alterar nenhum código existente

## 🔧 Adicionando um novo tipo de item

Um tipo novo é **uma classe nova** em `gilded_rose/updaters.py`, e nada mais. Não é preciso alterar nenhum método, nenhuma lista e nenhum arquivo de constantes:

```python
@register
class FrozenItemUpdater(ItemUpdater):
    """Itens congelados não mudam de qualidade."""

    NAME = "Frozen Yogurt"

    def _change_quality(self, item):
        pass
```

1. Herde de `ItemUpdater` — ou de outro updater, se a regra for uma variação dele (o conjurado herda do item comum e só dobra a taxa)
2. Declare o nome do item em `NAME`, ou sobrescreva `matches` se precisar de outra regra (o conjurado reconhece qualquer nome que comece com `Conjured`)
3. Implemente `_change_quality` usando as funções de `quality.py`, que já garantem os limites de 0 e 50
4. Decore a classe com `@register`

Se dois tipos reconhecerem o mesmo item, o sistema acusa o conflito com um erro, em vez de escolher um deles em silêncio.

## 📄 Licença

Projeto de estudo, livre para uso e modificação.
