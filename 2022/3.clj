(require '(clojure [string :as str] [set :as set]))
 
(defn priority [ch]
  (let [i (int ch)]
    (cond
      (and (> i 96) (< i 123)) (- i 96)
      (and (> i 64) (< i 91)) (+ (- i 64) 26)
      :else 0)))
 
(defn duplicate [sack]
  (let [half (/ (count sack) 2)
        left (set (take half sack))
        right (set (drop half sack))]
    (first (set/intersection left right))))
 
;; 3-1
(->> "3.txt"
  (slurp)
  (str/split-lines)
  (map duplicate)
  (map priority)
  (apply +)
  (println))
 
(defn reduce-duplicates [& sets]
  (reduce set/intersection sets))
 
;; 3-2
(->> "3.txt"
  (slurp)
  (str/split-lines)
  (partition 3)
  (map #(map set %))
  (map #(first (apply reduce-duplicates %)))
  (map priority)
  (apply +)
  (println))