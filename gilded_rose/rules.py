"""Constantes compartilhadas por todos os tipos de item.

Substituem os numeros magicos espalhados pelo codigo legado. O que e
especifico de um tipo - seu nome, suas faixas, suas taxas - vive na classe
dele em updaters.py, para que um tipo novo nao precise alterar este arquivo.
"""

MIN_QUALITY = 0
MAX_QUALITY = 50

# O dia da venda e o ultimo dia valido; a partir dai o item esta vencido.
LAST_SELLABLE_DAY = 0

# Depois de vencido, a variacao diaria de qualidade dobra.
EXPIRED_MULTIPLIER = 2
