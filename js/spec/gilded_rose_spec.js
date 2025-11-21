describe("Gilded Rose", function() {

  it("quality degrades by one when a day pass", function() {
  	initialQuality = 2;
    gildedRose = GildedRose([new Item("a_regular_item", "not_used", initialQuality)]);

    gildedRose.passDay();

    expect(gildedRose.getNthItem(0).quality).toEqual(1);
  });

  it("days to sell in decreases by one when a day pass", function() {
  	daysToSellIn = 3;
    gildedRose = GildedRose([new Item("a_regular_item", daysToSellIn, "not_used")]);

    gildedRose.passDay();

    expect(gildedRose.getNthItem(0).sell_in).toEqual(2);
  });

  
  it("age brie quality increases by one as days pass", function() {
  	initialQuality = 4;
    gildedRose = GildedRose([new Item("Aged Brie", "not_used", initialQuality)]);

    gildedRose.passDay();

    expect(gildedRose.getNthItem(0).quality).toEqual(5);
  });  

   it("never has to be sold or decreases in quality", function() {
  	initialQuality = 4;
  	daysToSellIn = 6;
    gildedRose = GildedRose([new Item("Sulfuras", daysToSellIn, initialQuality)]);

    gildedRose.passDay();

    expect(gildedRose.getNthItem(0).quality).toEqual(initialQuality);
    expect(gildedRose.getNthItem(0).sell_in).toEqual(daysToSellIn);
  });  
});
