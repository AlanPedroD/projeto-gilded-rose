"""Constantes do dominio.

Substituem os numeros e strings magicas espalhados pelo codigo legado.
"""

MIN_QUALITY = 0
MAX_QUALITY = 50

# Sulfuras e lendario: sua qualidade e fixa em 80 e ignora o teto normal.
LEGENDARY_QUALITY = 80

# O dia da venda e o ultimo dia valido; a partir dai o item esta vencido.
LAST_SELLABLE_DAY = 0

# Depois de vencido, a variacao diaria de qualidade dobra.
EXPIRED_MULTIPLIER = 2

# Faixas de valorizacao dos ingressos de backstage (dias restantes -> ganho).
BACKSTAGE_FIRST_TIER_DAYS = 10
BACKSTAGE_SECOND_TIER_DAYS = 5

# Nomes dos itens especiais.
AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
CONJURED_PREFIX = "Conjured"
