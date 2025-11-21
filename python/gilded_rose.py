# -*- coding: utf-8 -*-

# Polymorphic refactor: introduce Item subclasses and delegate update logic to them.
# Items are converted in-place to the appropriate subclass in GildedRose.__init__
# to preserve object identity while enabling polymorphic updates.



class Item:
    LOWEST_QUALITY = 0
    HIGHEST_QUALITY = 50
    SELL_BY_DATE = 0

    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "(%s, %s, %s)" % (self.name, self.sell_in, self.quality)

    # Helpers
    def _decrease_quality(self, amount=1):
        if self.quality > self.LOWEST_QUALITY:
            self.quality = max(self.LOWEST_QUALITY, self.quality - amount)

    def _increase_quality(self, amount=1):
        if self.quality < self.HIGHEST_QUALITY:
            self.quality = min(self.HIGHEST_QUALITY, self.quality + amount)

    def _remove_quality(self):
        self.quality = 0

    def _decrease_sell_in(self, amount=1):
        self.sell_in -= amount

    def _is_past_sell_date(self):
        return self.sell_in < self.SELL_BY_DATE
    
    def pre_quality_update(self):
        self._decrease_quality(1)

    def post_sell_date_update(self):
        if self._is_past_sell_date():
            self._decrease_quality(1)
    
    def decrease_sell_in(self):
        self._decrease_sell_in(1)

    # Default behavior for a normal item
    def update(self):
        self.pre_quality_update()
        self.decrease_sell_in() 
        self.post_sell_date_update()

class AgedBrie(Item):
    def pre_quality_update(self): 
        self._increase_quality(1)

    def post_sell_date_update(self):
        if self._is_past_sell_date():
            self._increase_quality(1)

class BackstagePass(Item):
    LATE_PASS_THRESHOLD = 11
    SUPER_LATE_PASS_THRESHOLD = 6

    def pre_quality_update(self):
        if self.sell_in < self.SUPER_LATE_PASS_THRESHOLD:
                self._increase_quality(3)
        elif self.sell_in < self.LATE_PASS_THRESHOLD:
            self._increase_quality(2)

    def post_sell_date_update(self):
        if self._is_past_sell_date():
            self._remove_quality()
    
class Sulfuras(Item):
    def update(self):
        # Legendary item does not change
        pass

class Conjured(Item):

    def pre_quality_update(self):
        # First quality update (twice as fast)
        self._decrease_quality(2)

    def post_sell_date_update(self):
        if self._is_past_sell_date():
            self._decrease_quality(2)


class GildedRose(object):
    AGED_BRIE = "Aged Brie"
    BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
    SULFURAS = "Sulfuras, Hand of Ragnaros"
    CONJURED = "Conjured Mana Cake"

    def __init__(self, items):
        # Convert passed-in items to appropriate subclass in-place
        # to preserve object identity used by callers/tests
        self.items = items
        for item in self.items:
            # If already a specialized subclass, leave it as-is
            if isinstance(item, (AgedBrie, BackstagePass, Sulfuras, Conjured)):
                continue
            if item.name == self.AGED_BRIE:
                item.__class__ = AgedBrie
            elif item.name == self.BACKSTAGE_PASSES:
                item.__class__ = BackstagePass
            elif item.name == self.SULFURAS:
                item.__class__ = Sulfuras
            elif item.name == self.CONJURED:
                item.__class__ = Conjured
            else:
                # Normal Item remains base Item
                pass

    def update_quality(self) -> None:
        for item in self.items:
            item.update()
