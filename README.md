# Gilded Rose

Sistema de controle de estoque de uma estalagem fictícia chamada **Gilded Rose**, responsável por atualizar diariamente a **qualidade** e o **prazo de validade** (`sell_in`) dos itens vendidos.

## 📋 O que o programa faz

Todo item possui três atributos:

- **name**: nome do item
- **sell_in**: quantos dias restam para vender o item
- **quality**: o quão valioso o item é (varia normalmente entre **0 e 50**)

A cada "dia" que passa (ou seja, a cada chamada do método `update_quality`), o programa atualiza esses valores automaticamente, seguindo regras diferentes dependendo do tipo do item.

## 🧪 Regras de atualização

| Item | Comportamento |
|---|---|
| **Item comum** | Perde 1 de qualidade por dia. Após o `sell_in` vencer, perde 2 por dia. Nunca fica abaixo de 0. |
| **Aged Brie** | Ganha qualidade com o tempo, ao invés de perder. Após vencer, ganha o dobro. Nunca passa de 50. |
| **Backstage passes** | Ganha qualidade conforme o show se aproxima (mais rápido faltando 10 e 5 dias). Após o show (`sell_in < 0`), a qualidade cai para **0** — o passe não vale mais nada. |
| **Sulfuras, Hand of Ragnaros** | Item lendário: nunca muda de qualidade nem de `sell_in`. |

## 📁 Estrutura do projeto

```
.
├── gilded_rose_refatorado.py   # Código principal (classes Item e GildedRose)
└── README.md                   # Este arquivo
```

## ⚙️ Instalação

Não há dependências externas — o projeto usa apenas Python puro.

Requisitos:
- Python 3.6 ou superior

Basta baixar/clonar o arquivo `gilded_rose_refatorado.py` para sua máquina.

## ▶️ Como rodar

O arquivo atual contém apenas as classes (`Item` e `GildedRose`). Para usá-lo, importe as classes e crie seus itens, como no exemplo abaixo:

```python
from gilded_rose_refatorado import Item, GildedRose

# Cria a lista de itens do estoque
itens = [
    Item("Aged Brie", sell_in=2, quality=0),
    Item("Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
    Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
    Item("Elixir of the Mongoose", sell_in=5, quality=7),
]

estoque = GildedRose(itens)

# Simula a passagem de um dia
estoque.update_quality()

# Mostra o estado atual dos itens
for item in itens:
    print(item)
```

Para simular vários dias, basta chamar `update_quality()` várias vezes (por exemplo, dentro de um loop `for` ou `while`).

## 🚀 Funcionalidades

- Atualização automática de qualidade e prazo de venda
- Suporte a 4 tipos diferentes de item, cada um com sua própria regra
- Garantia de que a qualidade nunca ultrapassa 50 nem fica negativa
- Estrutura pensada para facilitar a adição de novos tipos de item no futuro

## 🔧 Adicionando um novo tipo de item

Graças à organização do código em métodos pequenos, adicionar uma nova regra é simples:

1. Adicione uma nova constante com o nome do item (ex: `CONJURED = "Conjured Mana Cake"`)
2. Crie um método específico para a regra desse item (ex: `_atualizar_conjured`)
3. Chame esse método dentro de `_atualizar_qualidade_antes_do_prazo` (e, se necessário, em `_atualizar_qualidade_apos_vencimento`)

## 📄 Licença

Projeto de estudo, livre para uso e modificação.