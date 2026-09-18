"""Registro de updaters (OCP).

Adicionar um tipo novo de item significa criar uma classe e decora-la com
@register. Nenhum codigo existente precisa ser alterado - nao ha um if/elif
central para crescer a cada item novo.
"""

from typing import List, Optional, Type

from .item import Item

_updaters: List[Type] = []
_default_updater: Optional[Type] = None


def register(updater_class: Type) -> Type:
    """Registra um updater especializado. Usado como decorator."""
    _updaters.append(updater_class)
    return updater_class


def register_default(updater_class: Type) -> Type:
    """Registra o updater usado quando nenhum outro reconhece o item."""
    global _default_updater
    _default_updater = updater_class
    return updater_class


def updater_for(item: Item):
    """Devolve o updater responsavel por este item."""
    for updater_class in _updaters:
        if updater_class.matches(item.name):
            return updater_class()
    if _default_updater is None:
        raise LookupError("Nenhum updater padrao registrado")
    return _default_updater()
