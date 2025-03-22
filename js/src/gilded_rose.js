function Item(name, sell_in, quality) {
  this.name = name;
  this.sell_in = sell_in;
  this.quality = quality;
}

var items = [];

// Item Updater Class
class ItemUpdater {
  constructor(item) {
    this.item = item;
  }

  update() {
    if (this.item.name.includes("Conjured")) {
      this.updateConjured();
    } else {
      switch (this.item.name) {
        case "Aged Brie":
          this.updateAgedBrie();
          break;
        case "Backstage passes to a TAFKAL80ETC concert":
          this.updateBackstagePasses();
          break;
        case "Sulfuras, Hand of Ragnaros":
          return; // Sulfuras does not change
        default:
          this.updateNormalItem();
      }
    }

    if (this.item.name !== "Sulfuras, Hand of Ragnaros") {
      this.item.sell_in -= 1;
    }

    if (this.item.sell_in < 0) {
      this.handleExpiredItem();
    }
  }

  increaseQuality(amount = 1) {
    this.item.quality = Math.min(50, this.item.quality + amount);
  }

  degradeQuality(amount = 1) {
    this.item.quality = Math.max(0, this.item.quality - amount);
  }

  updateAgedBrie() {
    this.increaseQuality();
  }

  updateBackstagePasses() {
    if (this.item.sell_in > 10) {
      this.increaseQuality();
    } else if (this.item.sell_in > 5) {
      this.increaseQuality(2);
    } else if (this.item.sell_in > 0) {
      this.increaseQuality(3);
    } else {
      this.item.quality = 0; // Expired backstage passes
    }
  }

  updateNormalItem() {
    this.degradeQuality();
  }

  updateConjured() {
    this.degradeQuality(2);
  }

  handleExpiredItem() {
    if (this.item.name === "Aged Brie") {
      this.increaseQuality();
    } else if (this.item.name === "Backstage passes to a TAFKAL80ETC concert") {
      this.item.quality = 0;
    } else if (this.item.name.includes("Conjured")) {
      this.degradeQuality(2);
    } else {
      this.degradeQuality();
    }
  }
}

// Refactored update_quality function
function update_quality() {
  items.forEach((item) => new ItemUpdater(item).update());
}
