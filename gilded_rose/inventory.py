"""O inventario da loja."""

from typing import List

from .item import Item
from .registry import updater_for


class GildedRose:
    """Atualiza o inventario ao final de cada dia.

    Sua unica responsabilidade e percorrer os itens; quem sabe envelhecer cada
    um deles e o updater correspondente.
    """

    def __init__(self, items: List[Item]) -> None:
        self.items = items

    def update_quality(self) -> None:
        for item in self.items:
            updater_for(item).update(item)
