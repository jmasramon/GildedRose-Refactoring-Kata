# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    """     def test_foo(self):
            items = [Item("foo", 0, 0)]
            gilded_rose = GildedRose(items)
            gilded_rose.update_quality()
            self.assertEqual("fixme", items[0].name)
    """
    def test_not_AgedBrie_or_BackstagePasses_or_Sulfuras_and_positive_quality(self):
        initialQuality = 1
        initialSellIn = 10
        items = [Item("foo", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)
        self.assertEqual(initialQuality-1, items[0].quality)
        self.assertEqual(initialSellIn-1, items[0].sell_in)
        
    def test_AgedBrie_and_quantity_smaller_than_50(self):
        initialQuality = 50 - 1
        initialSellIn = 10
        items = [Item("Aged Brie", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Aged Brie", items[0].name)
        self.assertEqual(initialQuality+1, items[0].quality)
        self.assertEqual(initialSellIn-1, items[0].sell_in)
    
    def test_BackstagePasses_and_quantity_smaller_than_50(self):
        initialQuality = 50 - 1
        initialSellIn = 11
        items = [Item("Backstage passes to a TAFKAL80ETC concert", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Backstage passes to a TAFKAL80ETC concert", items[0].name)
        self.assertEqual(initialQuality, items[0].quality)
        self.assertEqual(initialSellIn-1, items[0].sell_in)

    def test_BackstagePasses_and_quantity_smaller_than_49_and_sell_in_smaller_that_11(self):
        initialQuality = 50 - 2
        initialSellIn = 10
        items = [Item("Backstage passes to a TAFKAL80ETC concert", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Backstage passes to a TAFKAL80ETC concert", items[0].name)
        self.assertEqual(initialQuality+2, items[0].quality)
        self.assertEqual(initialSellIn-1, items[0].sell_in)

    def test_BackstagePasses_and_quantity_smaller_than_49_and_sell_in_smaller_that_6(self):
        initialQuality = 50 - 3
        initialSellIn = 5
        items = [Item("Backstage passes to a TAFKAL80ETC concert", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Backstage passes to a TAFKAL80ETC concert", items[0].name)
        self.assertEqual(initialQuality+3, items[0].quality)
        self.assertEqual(initialSellIn-1, items[0].sell_in)

    def test_Sulfuras_does_not_change(self):
        initialQuality = 80
        initialSellIn = -1
        items = [Item("Sulfuras, Hand of Ragnaros", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Sulfuras, Hand of Ragnaros", items[0].name)
        self.assertEqual(initialQuality, items[0].quality)
        self.assertEqual(initialSellIn, items[0].sell_in)

    def test_RemoveQuality(self):
        initialQuality = 10
        initialSellIn = 0
        items = [Item("Backstage passes to a TAFKAL80ETC concert", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Backstage passes to a TAFKAL80ETC concert", items[0].name)
        self.assertEqual(0, items[0].quality)
        self.assertEqual(initialSellIn-1, items[0].sell_in)

    def test_Second_quality_update_not_AgedBrie_or_BackstagePasses_or_Sulfuras_and_positive_quality(self):
        initialQuality = 2
        initialSellIn = 0
        items = [Item("foo", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)
        self.assertEqual(initialQuality-2, items[0].quality)
        self.assertEqual(initialSellIn-1, items[0].sell_in)

    def test_Second_quality_update_AgedBrie_and_quantity_smaller_than_49(self):
        initialQuality = 50 - 2
        initialSellIn = 0
        items = [Item("Aged Brie", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Aged Brie", items[0].name)
        self.assertEqual(initialQuality+2, items[0].quality)
        self.assertEqual(initialSellIn-1, items[0].sell_in)

    def test_Second_quality_update_Backstage_and_past_latest_day(self):
        initialQuality = 50 - 2
        initialSellIn = 0
        items = [Item("Backstage passes to a TAFKAL80ETC concert", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Backstage passes to a TAFKAL80ETC concert", items[0].name)
        self.assertEqual(0, items[0].quality)
        self.assertEqual(initialSellIn-1, items[0].sell_in)
    
    def test_Conured_degrades_twice_as_fast(self):
        initialQuality = 40
        initialSellIn = 20
        items = [Item("Conjured Mana Cake", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Conjured Mana Cake", items[0].name)
        self.assertEqual(initialQuality-2, items[0].quality)
        self.assertEqual(initialSellIn-1, items[0].sell_in)
    
    def test_Conured_degrades_twice_as_fast_past_sell_in(self):
        initialQuality = 40
        initialSellIn = 0
        items = [Item("Conjured Mana Cake", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Conjured Mana Cake", items[0].name)
        self.assertEqual(initialQuality-4, items[0].quality)
        self.assertEqual(initialSellIn-1, items[0].sell_in)

    # Boundary and invariant tests added below

    def test_BackstagePasses_boundary_sell_in_equals_6_increases_by_2(self):
        initialQuality = 47
        initialSellIn = 6
        items = [Item("Backstage passes to a TAFKAL80ETC concert", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Backstage passes to a TAFKAL80ETC concert", items[0].name)
        self.assertEqual(initialQuality+2, items[0].quality)
        self.assertEqual(initialSellIn-1, items[0].sell_in)

    def test_BackstagePasses_quality_capped_at_50(self):
        initialQuality = 49
        initialSellIn = 10  # triggers +2
        items = [Item("Backstage passes to a TAFKAL80ETC concert", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Backstage passes to a TAFKAL80ETC concert", items[0].name)
        self.assertEqual(50, items[0].quality)
        self.assertEqual(initialSellIn-1, items[0].sell_in)

    def test_AgedBrie_quality_capped_at_50(self):
        initialQuality = 50
        initialSellIn = 10
        items = [Item("Aged Brie", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Aged Brie", items[0].name)
        self.assertEqual(50, items[0].quality)
        self.assertEqual(initialSellIn-1, items[0].sell_in)

    def test_AgedBrie_quality_capped_at_50_after_sell_date(self):
        initialQuality = 50
        initialSellIn = 0
        items = [Item("Aged Brie", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Aged Brie", items[0].name)
        self.assertEqual(50, items[0].quality)
        self.assertEqual(initialSellIn-1, items[0].sell_in)

    def test_NormalItem_quality_never_negative(self):
        initialQuality = 0
        initialSellIn = 5
        items = [Item("foo", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)
        self.assertEqual(0, items[0].quality)
        self.assertEqual(initialSellIn-1, items[0].sell_in)

    def test_Conjured_quality_never_negative_pre_sell_date(self):
        initialQuality = 1
        initialSellIn = 10
        items = [Item("Conjured Mana Cake", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Conjured Mana Cake", items[0].name)
        self.assertEqual(0, items[0].quality)
        self.assertEqual(initialSellIn-1, items[0].sell_in)

    def test_Conjured_quality_never_negative_post_sell_date(self):
        initialQuality = 3
        initialSellIn = 0
        items = [Item("Conjured Mana Cake", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Conjured Mana Cake", items[0].name)
        self.assertEqual(0, items[0].quality)
        self.assertEqual(initialSellIn-1, items[0].sell_in)

    def test_Sulfuras_quality_remains_80_not_capped(self):
        initialQuality = 80
        initialSellIn = 5
        items = [Item("Sulfuras, Hand of Ragnaros", initialSellIn, initialQuality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Sulfuras, Hand of Ragnaros", items[0].name)
        self.assertEqual(80, items[0].quality)
        self.assertEqual(initialSellIn, items[0].sell_in)

if __name__ == '__main__':
    unittest.main()
