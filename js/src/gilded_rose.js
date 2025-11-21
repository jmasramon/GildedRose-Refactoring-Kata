
var GildedRose = function(items) {
  "use strict";
  var types = {
    "Aged Brie": AgedBrie,
    "Sulfuras" : Sulfuras
  };

  return {
    passDay: passDay,
    getNthItem: getNthItem
  };

  function passDay() {
    var degradableItems = items.map(createItem);
    degradableItems
      // .filter(function(item) {
      //   return item.name != "Sulfuras";
      // })
      .forEach(ageOneDay); 
  }

  function getNthItem(n) {
    return items[n];
  }

  function DegradableItem(item) {
    return {
      updateQuality: function() {
        item.quality -= 1;
      },
      age: function() {
        item.sell_in -= 1;
      }
    };
  }

  function AgedBrie(item) {
    var degradableItem = DegradableItem(item);
    return {
      updateQuality: function() {
        item.quality += 1;
      },
      age: function() {
        degradableItem.age();
      }
    };
  }

  function Sulfuras() {
    return {
      updateQuality: function() {
      },
      age: function() {
      }
    };
  }

  function createItem(item) {
    if (types.hasOwnProperty(item.name)) {
      return types[item.name](item);
    }
    return DegradableItem(item);
  }

  function ageOneDay(degradableItem) {
    degradableItem.age();
    degradableItem.updateQuality();
  }

};

function Item(name, sell_in, quality) {
  this.name = name;
  this.sell_in = sell_in;
  this.quality = quality;
}

