"""Teste de caracterizacao (golden master).

Prova que a refatoracao preserva o comportamento: para toda combinacao de
nome, sell_in e quality, o sistema novo produz exatamente o mesmo resultado
que o codigo legado - dia apos dia.

O legado e a unica fonte de verdade aqui, inclusive nos cantos que a
documentacao de regras nao descreve (por exemplo: um item comum com quality
80 cai para 78, porque o teto de 50 so e verificado ao aumentar).
"""

import unittest

from gilded_rose import GildedRose, Item
from legacy import gilded_rose as legacy

# O legado nao conhece itens conjurados; eles sao a feature nova e por isso
# ficam de fora da comparacao (a divergencia e testada em test_business_rules).
LEGACY_ITEM_NAMES = [
    "+5 Dexterity Vest",
    "Elixir of the Mongoose",
    "Aged Brie",
    "Sulfuras, Hand of Ragnaros",
    "Backstage passes to a TAFKAL80ETC concert",
]

SELL_IN_RANGE = range(-10, 21)
QUALITY_RANGE = list(range(0, 56)) + [80, 100]
DAYS_SIMULATED = 30


class GoldenMasterTest(unittest.TestCase):
    def test_um_dia_produz_o_mesmo_resultado_do_legado(self):
        for name in LEGACY_ITEM_NAMES:
            for sell_in in SELL_IN_RANGE:
                for quality in QUALITY_RANGE:
                    with self.subTest(name=name, sell_in=sell_in, quality=quality):
                        legacy_item = legacy.Item(name, sell_in, quality)
                        legacy.GildedRose([legacy_item]).att()

                        item = Item(name, sell_in, quality)
                        GildedRose([item]).update_quality()

                        self.assertEqual(
                            (legacy_item.sell_in, legacy_item.quality),
                            (item.sell_in, item.quality),
                        )

    def test_trinta_dias_seguidos_produzem_a_mesma_trajetoria(self):
        for name in LEGACY_ITEM_NAMES:
            for sell_in in (-1, 0, 1, 5, 6, 10, 11, 20):
                for quality in (0, 1, 10, 49, 50, 80):
                    with self.subTest(name=name, sell_in=sell_in, quality=quality):
                        legacy_item = legacy.Item(name, sell_in, quality)
                        legacy_store = legacy.GildedRose([legacy_item])

                        item = Item(name, sell_in, quality)
                        store = GildedRose([item])

                        for day in range(DAYS_SIMULATED):
                            legacy_store.att()
                            store.update_quality()
                            self.assertEqual(
                                (legacy_item.sell_in, legacy_item.quality),
                                (item.sell_in, item.quality),
                                "divergiu no dia %d" % (day + 1),
                            )

    def test_inventario_completo_e_atualizado_como_no_legado(self):
        def build(item_class):
            return [
                item_class("+5 Dexterity Vest", 10, 20),
                item_class("Aged Brie", 2, 0),
                item_class("Elixir of the Mongoose", 5, 7),
                item_class("Sulfuras, Hand of Ragnaros", 0, 80),
                item_class("Sulfuras, Hand of Ragnaros", -1, 80),
                item_class("Backstage passes to a TAFKAL80ETC concert", 15, 20),
                item_class("Backstage passes to a TAFKAL80ETC concert", 10, 49),
                item_class("Backstage passes to a TAFKAL80ETC concert", 5, 49),
            ]

        legacy_items = build(legacy.Item)
        legacy_store = legacy.GildedRose(legacy_items)
        items = build(Item)
        store = GildedRose(items)

        for _ in range(DAYS_SIMULATED):
            legacy_store.att()
            store.update_quality()
            self.assertEqual(
                [repr(each) for each in legacy_items],
                [repr(each) for each in items],
            )


if __name__ == "__main__":
    unittest.main()
