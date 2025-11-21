(ns gilded.core-test
  (:require [clojure.test :refer [deftest is testing]]
            [gilded.core :as gilded]))

;; Helper functions
(defn- make-item [name quality sell-in]
  {:name name :quality quality :sell-in sell-in})

(defn- get-first-item [store]
  (first (gilded/item-seq store)))

(defn- update-store-n-times! [store n]
  (dotimes [_ n]
    (gilded/update-quality! store)))

(defn- assert-item [item expected-name expected-quality expected-sell-in]
  (is (= expected-name (:name item)))
  (is (= expected-quality (:quality item)))
  (is (= expected-sell-in (:sell-in item))))

(deftest normal-item-test
  (testing "Normal items degrade in quality and sell-in"
    (let [store (gilded/make-store [(make-item "Normal Item" 20 10)])
          _ (gilded/update-quality! store)
          item (get-first-item store)]
      (assert-item item "Normal Item" 19 9)))

  (testing "Normal items reach zero quality"
    (let [store (gilded/make-store [(make-item "Normal Item" 20 10)])
          _ (update-store-n-times! store 30)]
      (assert-item (get-first-item store) "Normal Item" 0 -20))))

(deftest aged-brie-test
  (testing "Aged Brie increases in quality over time"
    (let [store (gilded/make-store [(make-item "Aged Brie" 20 10)])
          _ (gilded/update-quality! store)
          item (get-first-item store)]
      (assert-item item "Aged Brie" 21 9)))

  (testing "Aged Brie quality caps at 50"
    (let [store (gilded/make-store [(make-item "Aged Brie" 48 5)])
          _ (update-store-n-times! store 10)]
      (assert-item (get-first-item store) "Aged Brie" 50 -5)))

  (testing "Aged Brie continues improving after sell date"
    (let [store (gilded/make-store [(make-item "Aged Brie" 20 -1)])
          _ (gilded/update-quality! store)
          item (get-first-item store)]
      (assert-item item "Aged Brie" 22 -2))))

(deftest sulfuras-test
  (testing "Sulfuras never changes in quality or sell-in"
    (let [store (gilded/make-store [(make-item "Sulfuras, Hand of Ragnaros" 80 0)])
          _ (update-store-n-times! store 100)
          item (get-first-item store)]
      (assert-item item "Sulfuras, Hand of Ragnaros" 80 0))))

(deftest backstage-passes-test
  (testing "Backstage passes increase by 1 when > 10 days"
    (let [store (gilded/make-store [(make-item "Backstage passes to a TAFKAL80ETC concert" 20 15)])
          _ (gilded/update-quality! store)
          item (get-first-item store)]
      (assert-item item "Backstage passes to a TAFKAL80ETC concert" 21 14)))

  (testing "Backstage passes increase by 2 when 6-10 days"
    (let [store (gilded/make-store [(make-item "Backstage passes to a TAFKAL80ETC concert" 20 8)])
          _ (gilded/update-quality! store)
          item (get-first-item store)]
      (assert-item item "Backstage passes to a TAFKAL80ETC concert" 22 7)))

  (testing "Backstage passes increase by 3 when ≤ 5 days"
    (let [store (gilded/make-store [(make-item "Backstage passes to a TAFKAL80ETC concert" 20 3)])
          _ (gilded/update-quality! store)
          item (get-first-item store)]
      (assert-item item "Backstage passes to a TAFKAL80ETC concert" 23 2)))

  (testing "Backstage passes become worthless after concert"
    (let [store (gilded/make-store [(make-item "Backstage passes to a TAFKAL80ETC concert" 20 0)])
          _ (gilded/update-quality! store)
          item (get-first-item store)]
      (assert-item item "Backstage passes to a TAFKAL80ETC concert" 0 -1))))

(deftest quality-bounds-test
  (testing "Quality never exceeds 50 (except Sulfuras)"
    (let [store (gilded/make-store [(make-item "Backstage passes to a TAFKAL80ETC concert" 49 3)])
          _ (gilded/update-quality! store)
          item (get-first-item store)]
      (assert-item item "Backstage passes to a TAFKAL80ETC concert" 50 2)))

  (testing "Quality never goes below 0"
    (let [store (gilded/make-store [(make-item "Normal Item" 1 -5)])
          _ (gilded/update-quality! store)
          item (get-first-item store)]
      (assert-item item "Normal Item" 0 -6))))

(deftest conjured-items-test
  (testing "Conjured items degrade twice as fast as normal items"
    (let [store (gilded/make-store [(make-item "Conjured sword" 10 5)])
          _ (gilded/update-quality! store)
          item (get-first-item store)]
      (assert-item item "Conjured sword" 8 4)))

  (testing "Conjured items degrade four times as fast after sell date"
    (let [store (gilded/make-store [(make-item "Conjured sword" 10 -1)])
          _ (gilded/update-quality! store)
          item (get-first-item store)]
      (assert-item item "Conjured sword" 6 -2))))