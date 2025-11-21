(ns gilded.core
  (:require
   [clojure.string :as str]))

;; Quality bounds
(def ^:const MIN_QUALITY 0)
(def ^:const MAX_QUALITY 50)

;; Backstage pass thresholds
(def ^:const BACKSTAGE_MEDIUM_DAYS 11)
(def ^:const BACKSTAGE_HIGH_DAYS 6)

;; Quality change amounts (business domain concepts)
(def ^:const NORMAL_DEGRADATION 1)
(def ^:const CONJURED_DEGRADATION 2)
(def ^:const BRIE_IMPROVEMENT 1)
(def ^:const BACKSTAGE_NORMAL_IMPROVEMENT 1)
(def ^:const BACKSTAGE_MEDIUM_IMPROVEMENT 2)
(def ^:const BACKSTAGE_HIGH_IMPROVEMENT 3)

(defn make-store [items]
  (assert (vector? items))
  (->> items
       (map (fn [item] (atom item)))
       vec))

(defn item-seq [store]
  (->> store
       (map deref)))

;; Level 7: Item data access (encapsulates internal structure)
(defn- item-name [item]
  (:name @item))

(defn- item-sell-in [item]
  (:sell-in @item))

(defn- item-quality [item]
  (:quality @item))

(defn- set-item-quality! [item new-quality]
  (swap! item assoc :quality new-quality))

(defn- update-item-quality! [item update-fn]
  (swap! item update :quality update-fn))

(defn- update-item-sell-in! [item update-fn]
  (swap! item update :sell-in update-fn))

;; Level 6: Item classification and state predicates
(defn- sulfuras? [item]
  (= (item-name item) "Sulfuras, Hand of Ragnaros"))

(defn- brie? [item]
  (= (item-name item) "Aged Brie"))

(defn- concert? [item]
  (= (item-name item) "Backstage passes to a TAFKAL80ETC concert"))

(defn- conjured? [item]
  (str/starts-with? (item-name item) "Conjured"))

(defn- past-sell-date? [item]
  (neg? (item-sell-in item)))


;; Level 5: Pure quality calculations (no side effects)
(defn- calculate-bounded-quality [current-quality change]
  (-> current-quality
      (+ change)
      (min MAX_QUALITY)
      (max MIN_QUALITY)))

;; Level 4: Item property mutations
(defn- apply-quality-change! [item change]
  (when (not= change 0)
    (update-item-quality! item #(calculate-bounded-quality % change))))

(defn- set-quality! [item new-quality]
  (set-item-quality! item new-quality))

(defn- decrease-sell-in! [item]
  (when-not (sulfuras? item)
    (update-item-sell-in! item dec)))


;; Level 3: Business rule calculations (pure functions)
(defn- calculate-backstage-quality-change [sell-in]
  (cond
    (< sell-in BACKSTAGE_HIGH_DAYS) BACKSTAGE_HIGH_IMPROVEMENT
    (< sell-in BACKSTAGE_MEDIUM_DAYS) BACKSTAGE_MEDIUM_IMPROVEMENT
    :else BACKSTAGE_NORMAL_IMPROVEMENT))

(defn- calculate-quality-change-before-sell-date [item]
  (cond
    (sulfuras? item) 0
    (brie? item) BRIE_IMPROVEMENT
    (concert? item) (calculate-backstage-quality-change (item-sell-in item))
    (conjured? item) (- CONJURED_DEGRADATION)
    :else (- NORMAL_DEGRADATION)))

(defn- calculate-quality-change-after-sell-date [item]
  (cond
    (sulfuras? item) 0
    (brie? item) BRIE_IMPROVEMENT
    (concert? item) :zero ; Special case - set to zero
    (conjured? item) (- CONJURED_DEGRADATION)
    :else (- NORMAL_DEGRADATION)))

;; Level 2: Apply business rules
(defn- update-quality-before-sell-date [item]
  (let [change (calculate-quality-change-before-sell-date item)]
    (apply-quality-change! item change)))

(defn- update-quality-after-sell-date [item]
  (when (past-sell-date? item)
    (let [change (calculate-quality-change-after-sell-date item)]
      (cond
        (= change :zero) (set-quality! item 0)
        :else (apply-quality-change! item change)))))

;; Level 1: Main business operation
(defn update-quality! [store]
  (doseq [item store]
    (update-quality-before-sell-date item)
    (decrease-sell-in! item)
    (update-quality-after-sell-date item)))


