"""Operacoes de qualidade, centralizadas (DRY).

No codigo legado o par "checa o limite / soma ou subtrai 1" aparecia sete
vezes. Aqui ele existe uma vez so, e os limites ficam garantidos por
construcao: nenhum updater mexe em item.quality diretamente.
"""

from .item import Item
from .rules import MAX_QUALITY, MIN_QUALITY


def increase(item: Item, amount: int) -> None:
    """Valoriza o item sem ultrapassar o teto de qualidade.

    Um item que ja esta no teto (ou acima dele, como o Sulfuras) nao muda.
    """
    if item.quality >= MAX_QUALITY:
        return
    item.quality = min(MAX_QUALITY, item.quality + amount)


def decrease(item: Item, amount: int) -> None:
    """Degrada o item sem deixar a qualidade ficar negativa."""
    item.quality = max(MIN_QUALITY, item.quality - amount)


def drop_to_zero(item: Item) -> None:
    """Zera a qualidade: o item perdeu todo o valor."""
    item.quality = MIN_QUALITY
