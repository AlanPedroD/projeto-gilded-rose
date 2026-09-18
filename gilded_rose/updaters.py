"""Uma classe por regra de envelhecimento (SRP).

No legado, as regras dos cinco tipos de item estavam entrelacadas em um unico
metodo. Aqui cada tipo sabe apenas da propria regra e nada sabe dos outros.
"""

from abc import ABC, abstractmethod

from . import quality
from .item import Item
from .registry import register, register_default
from .rules import (
    AGED_BRIE,
    BACKSTAGE_FIRST_TIER_DAYS,
    BACKSTAGE_PASSES,
    BACKSTAGE_SECOND_TIER_DAYS,
    EXPIRED_MULTIPLIER,
    LAST_SELLABLE_DAY,
    SULFURAS,
)


class ItemUpdater(ABC):
    """Passagem de um dia para um item.

    A ordem e a mesma do sistema legado: a qualidade muda considerando os dias
    que ainda restavam, e so depois o prazo de venda avanca.
    """

    def update(self, item: Item) -> None:
        self._change_quality(item)
        self._advance_sell_in(item)

    @staticmethod
    @abstractmethod
    def matches(name: str) -> bool:
        """Este updater e responsavel por um item com este nome?"""

    @abstractmethod
    def _change_quality(self, item: Item) -> None:
        """Aplica a variacao de qualidade de um dia."""

    def _advance_sell_in(self, item: Item) -> None:
        item.sell_in -= 1

    @staticmethod
    def _is_expired(item: Item) -> bool:
        """O prazo de venda termina ao final do dia em que sell_in chega a 0."""
        return item.sell_in <= LAST_SELLABLE_DAY


@register_default
class StandardItemUpdater(ItemUpdater):
    """Item comum: perde qualidade, e dobro disso depois de vencido."""

    DAILY_DEGRADATION = 1

    @staticmethod
    def matches(name: str) -> bool:
        return True

    def _change_quality(self, item: Item) -> None:
        quality.decrease(item, self._degradation_for(item))

    def _degradation_for(self, item: Item) -> int:
        if self._is_expired(item):
            return self.DAILY_DEGRADATION * EXPIRED_MULTIPLIER
        return self.DAILY_DEGRADATION


@register
class AgedBrieUpdater(ItemUpdater):
    """Aged Brie: valoriza com o tempo, e mais rapido depois de vencido."""

    DAILY_APPRECIATION = 1

    @staticmethod
    def matches(name: str) -> bool:
        return name == AGED_BRIE

    def _change_quality(self, item: Item) -> None:
        quality.increase(item, self._appreciation_for(item))

    def _appreciation_for(self, item: Item) -> int:
        if self._is_expired(item):
            return self.DAILY_APPRECIATION * EXPIRED_MULTIPLIER
        return self.DAILY_APPRECIATION


@register
class BackstagePassUpdater(ItemUpdater):
    """Ingressos: valorizam conforme o show se aproxima e viram po depois dele."""

    BASE_APPRECIATION = 1
    NEAR_SHOW_APPRECIATION = 2
    IMMINENT_SHOW_APPRECIATION = 3

    @staticmethod
    def matches(name: str) -> bool:
        return name == BACKSTAGE_PASSES

    def _change_quality(self, item: Item) -> None:
        if self._is_expired(item):
            quality.drop_to_zero(item)
            return
        quality.increase(item, self._appreciation_for(item.sell_in))

    @classmethod
    def _appreciation_for(cls, days_remaining: int) -> int:
        if days_remaining <= BACKSTAGE_SECOND_TIER_DAYS:
            return cls.IMMINENT_SHOW_APPRECIATION
        if days_remaining <= BACKSTAGE_FIRST_TIER_DAYS:
            return cls.NEAR_SHOW_APPRECIATION
        return cls.BASE_APPRECIATION


@register
class LegendaryItemUpdater(ItemUpdater):
    """Sulfuras: lendario, nunca e vendido e nunca perde qualidade."""

    @staticmethod
    def matches(name: str) -> bool:
        return name == SULFURAS

    def update(self, item: Item) -> None:
        """Um item lendario nao muda: nem sell_in, nem quality."""

    def _change_quality(self, item: Item) -> None:
        """Nao ha variacao de qualidade para itens lendarios."""
