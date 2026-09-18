"""Gilded Rose - sistema de inventario da loja."""

from .inventory import GildedRose
from .item import Item
from .registry import register, register_default, updater_for

# Importado pelo efeito colateral: registra os updaters de cada tipo de item.
from . import updaters  # noqa: F401  isort:skip

__all__ = ["GildedRose", "Item", "register", "register_default", "updater_for"]
