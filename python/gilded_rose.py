# -*- coding: utf-8 -*-
class GildedRose:
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            self.get_updater(item).update()

    def get_updater(self, item):
        """Returns the appropriate updater class for the item"""
        if item.name == "Aged Brie":
            return AgedBrieUpdater(item)
        elif item.name == "Backstage passes to a TAFKAL80ETC concert":
            return BackstagePassUpdater(item)
        elif item.name == "Sulfuras, Hand of Ragnaros":
            return SulfurasUpdater(item)
        elif "Conjured" in item.name:
            return ConjuredItemUpdater(item)
        else:
            return NormalItemUpdater(item)


class ItemUpdater:
    """Base class for updating item quality and sell-in values"""

    def __init__(self, item):
        self.item = item

    def update(self):
        self.update_quality()
        self.update_sell_in()
        if self.item.sell_in < 0:
            self.handle_expired()

    def update_quality(self):
        """Default behavior for normal items"""
        self.decrease_quality()

    def update_sell_in(self):
        """All items except Sulfuras decrease sell_in"""
        self.item.sell_in -= 1

    def handle_expired(self):
        """Handles quality changes when sell_in < 0"""
        self.decrease_quality()

    def increase_quality(self, amount=1):
        """Increases quality but caps it at 50"""
        self.item.quality = min(50, self.item.quality + amount)

    def decrease_quality(self, amount=1):
        """Decreases quality but ensures it doesn't go below 0"""
        self.item.quality = max(0, self.item.quality - amount)


class AgedBrieUpdater(ItemUpdater):
    def update_quality(self):
        self.increase_quality()

    def handle_expired(self):
        self.increase_quality()


class BackstagePassUpdater(ItemUpdater):
    def update_quality(self):
        if self.item.sell_in > 10:
            self.increase_quality()
        elif self.item.sell_in > 5:
            self.increase_quality(2)
        elif self.item.sell_in > 0:
            self.increase_quality(3)
        else:
            self.item.quality = 0  # Expired passes have 0 quality


class SulfurasUpdater(ItemUpdater):
    def update_quality(self):
        pass  # Sulfuras never changes

    def update_sell_in(self):
        pass  # Sulfuras never changes


class ConjuredItemUpdater(ItemUpdater):
    def update_quality(self):
        self.decrease_quality(2)  # Conjured items degrade twice as fast

    def handle_expired(self):
        self.decrease_quality(2)


class NormalItemUpdater(ItemUpdater):
    pass  # Uses default behavior from ItemUpdater


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return f"{self.name}, {self.sell_in}, {self.quality}"
