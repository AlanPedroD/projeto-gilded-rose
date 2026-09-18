"""Testes das regras de negocio, escritos na linguagem do dominio.

Enquanto o golden master prova "nada mudou", estes testes documentam
"o que o sistema faz" e continuam valendo se o legado for apagado.
"""

import unittest

from gilded_rose import GildedRose, Item
from gilded_rose.rules import (
    AGED_BRIE,
    BACKSTAGE_PASSES,
    LEGENDARY_QUALITY,
    MAX_QUALITY,
    SULFURAS,
)

NORMAL_ITEM = "+5 Dexterity Vest"

CONJURED_ITEM = "Conjured Mana Cake"

class ItemTestCase(unittest.TestCase):
    def update(self, name, sell_in, quality, days=1):
        item = Item(name, sell_in, quality)
        store = GildedRose([item])
        for _ in range(days):
            store.update_quality()
        return item

    def assertUpdatesTo(self, name, before, after, days=1):
        item = self.update(name, before[0], before[1], days)
        self.assertEqual(after, (item.sell_in, item.quality))


class ItemComumTest(ItemTestCase):
    def test_perde_um_de_qualidade_e_um_de_prazo_por_dia(self):
        self.assertUpdatesTo(NORMAL_ITEM, (10, 20), (9, 19))

    def test_degrada_duas_vezes_mais_rapido_depois_de_vencido(self):
        self.assertUpdatesTo(NORMAL_ITEM, (-1, 20), (-2, 18))

    def test_o_dia_da_venda_ainda_e_um_dia_normal(self):
        self.assertUpdatesTo(NORMAL_ITEM, (1, 20), (0, 19))

    def test_no_dia_seguinte_ao_prazo_ja_degrada_em_dobro(self):
        self.assertUpdatesTo(NORMAL_ITEM, (0, 20), (-1, 18))

    def test_a_qualidade_nunca_fica_negativa(self):
        self.assertUpdatesTo(NORMAL_ITEM, (5, 0), (4, 0))

    def test_a_qualidade_nunca_fica_negativa_nem_vencido(self):
        self.assertUpdatesTo(NORMAL_ITEM, (-5, 1), (-6, 0))


class AgedBrieTest(ItemTestCase):
    def test_valoriza_um_por_dia(self):
        self.assertUpdatesTo(AGED_BRIE, (10, 20), (9, 21))

    def test_valoriza_em_dobro_depois_de_vencido(self):
        self.assertUpdatesTo(AGED_BRIE, (-1, 20), (-2, 22))

    def test_respeita_o_teto_de_qualidade(self):
        self.assertUpdatesTo(AGED_BRIE, (5, MAX_QUALITY), (4, MAX_QUALITY))

    def test_nao_ultrapassa_o_teto_ao_valorizar_em_dobro(self):
        self.assertUpdatesTo(AGED_BRIE, (-1, 49), (-2, MAX_QUALITY))


class SulfurasTest(ItemTestCase):
    def test_nunca_muda(self):
        self.assertUpdatesTo(SULFURAS, (5, LEGENDARY_QUALITY), (5, LEGENDARY_QUALITY))

    def test_nao_muda_nem_depois_do_prazo(self):
        self.assertUpdatesTo(SULFURAS, (-1, LEGENDARY_QUALITY), (-1, LEGENDARY_QUALITY))

    def test_continua_imutavel_ao_longo_do_tempo(self):
        self.assertUpdatesTo(
            SULFURAS, (0, LEGENDARY_QUALITY), (0, LEGENDARY_QUALITY), days=100
        )

    def test_mantem_a_qualidade_acima_do_teto_normal(self):
        item = self.update(SULFURAS, 5, LEGENDARY_QUALITY)
        self.assertGreater(item.quality, MAX_QUALITY)


class BackstagePassTest(ItemTestCase):
    def test_valoriza_um_por_dia_faltando_mais_de_dez_dias(self):
        self.assertUpdatesTo(BACKSTAGE_PASSES, (11, 20), (10, 21))

    def test_valoriza_dois_por_dia_faltando_dez_dias_ou_menos(self):
        self.assertUpdatesTo(BACKSTAGE_PASSES, (10, 20), (9, 22))
        self.assertUpdatesTo(BACKSTAGE_PASSES, (6, 20), (5, 22))

    def test_valoriza_tres_por_dia_faltando_cinco_dias_ou_menos(self):
        self.assertUpdatesTo(BACKSTAGE_PASSES, (5, 20), (4, 23))
        self.assertUpdatesTo(BACKSTAGE_PASSES, (1, 20), (0, 23))

    def test_perde_todo_o_valor_depois_do_show(self):
        self.assertUpdatesTo(BACKSTAGE_PASSES, (0, 20), (-1, 0))

    def test_continua_sem_valor_depois_do_show(self):
        self.assertUpdatesTo(BACKSTAGE_PASSES, (-1, 20), (-2, 0))

    def test_respeita_o_teto_mesmo_valorizando_tres(self):
        self.assertUpdatesTo(BACKSTAGE_PASSES, (5, 49), (4, MAX_QUALITY))


class ConjuredItemTest(ItemTestCase):
    """Feature nova: itens conjurados degradam duas vezes mais rapido."""

    def test_perde_dois_de_qualidade_por_dia(self):
        self.assertUpdatesTo(CONJURED_ITEM, (10, 20), (9, 18))

    def test_perde_quatro_de_qualidade_depois_de_vencido(self):
        self.assertUpdatesTo(CONJURED_ITEM, (-1, 20), (-2, 16))

    def test_o_dia_da_venda_ainda_perde_dois(self):
        self.assertUpdatesTo(CONJURED_ITEM, (1, 20), (0, 18))

    def test_no_dia_seguinte_ao_prazo_ja_perde_quatro(self):
        self.assertUpdatesTo(CONJURED_ITEM, (0, 20), (-1, 16))

    def test_a_qualidade_nunca_fica_negativa(self):
        self.assertUpdatesTo(CONJURED_ITEM, (5, 1), (4, 0))

    def test_a_qualidade_nunca_fica_negativa_quando_vencido(self):
        self.assertUpdatesTo(CONJURED_ITEM, (-5, 3), (-6, 0))

    def test_a_qualidade_zerada_continua_zerada(self):
        self.assertUpdatesTo(CONJURED_ITEM, (5, 0), (0, 0), days=5)

    def test_degrada_exatamente_o_dobro_de_um_item_comum(self):
        for sell_in in (10, 1, 0, -3):
            with self.subTest(sell_in=sell_in):
                normal = self.update(NORMAL_ITEM, sell_in, 40)
                conjured = self.update(CONJURED_ITEM, sell_in, 40)
                self.assertEqual(2 * (40 - normal.quality), 40 - conjured.quality)
                self.assertEqual(normal.sell_in, conjured.sell_in)

    def test_a_regra_vale_para_qualquer_item_conjurado(self):
        self.assertUpdatesTo("Conjured Sword of Testing", (10, 20), (9, 18))

    def test_convive_com_os_outros_itens_no_inventario(self):
        items = [Item(NORMAL_ITEM, 10, 20), Item(CONJURED_ITEM, 10, 20)]
        GildedRose(items).update_quality()
        self.assertEqual([19, 18], [item.quality for item in items])

    def test_diverge_do_legado_de_proposito(self):
        """O legado tratava um item conjurado como item comum (perdia 1)."""
        conjured = self.update(CONJURED_ITEM, 10, 20)
        normal = self.update(NORMAL_ITEM, 10, 20)
        self.assertNotEqual(normal.quality, conjured.quality)


class InventarioTest(ItemTestCase):
    def test_atualiza_todos_os_itens_da_lista(self):
        items = [
            Item(NORMAL_ITEM, 10, 20),
            Item(AGED_BRIE, 10, 20),
            Item(BACKSTAGE_PASSES, 10, 20),
        ]
        GildedRose(items).update_quality()
        self.assertEqual([19, 21, 22], [item.quality for item in items])

    def test_inventario_vazio_nao_quebra(self):
        GildedRose([]).update_quality()

    def test_a_qualidade_permanece_entre_zero_e_cinquenta(self):
        names = [NORMAL_ITEM, AGED_BRIE, BACKSTAGE_PASSES]
        items = [Item(name, 12, 25) for name in names]
        store = GildedRose(items)
        for _ in range(60):
            store.update_quality()
            for item in items:
                self.assertGreaterEqual(item.quality, 0)
                self.assertLessEqual(item.quality, MAX_QUALITY)


class ExtensibilidadeTest(unittest.TestCase):
    """OCP: um tipo novo entra sem alterar nenhuma classe existente."""

    def test_um_updater_novo_pode_ser_registrado_sem_tocar_no_codigo_existente(self):
        from gilded_rose import register, updater_for
        from gilded_rose.registry import _updaters
        from gilded_rose.updaters import ItemUpdater

        @register
        class FrozenItemUpdater(ItemUpdater):
            @staticmethod
            def matches(name):
                return name.startswith("Frozen")

            def _change_quality(self, item):
                pass

        try:
            item = Item("Frozen Yogurt", 5, 20)
            GildedRose([item]).update_quality()
            self.assertEqual((4, 20), (item.sell_in, item.quality))
            self.assertIsInstance(updater_for(item), FrozenItemUpdater)
        finally:
            _updaters.remove(FrozenItemUpdater)

    def test_itens_desconhecidos_usam_a_regra_padrao(self):
        from gilded_rose.updaters import StandardItemUpdater
        from gilded_rose import updater_for

        self.assertIsInstance(updater_for(Item("Qualquer Coisa", 5, 20)),
                              StandardItemUpdater)


if __name__ == "__main__":
    unittest.main()
