(require '(clojure [string :as str]))

(defn in? [v i] (some #(= i %) v))

(defn transpose [v] (apply map list v)) 

(defn empty-idx [v] (into #{} (keep-indexed (fn [idx row] (if-not (in? row \#) idx)) v)))

(defn taxicab [a b] (reduce + 0 (map #(abs (- %1 %2)) a b)))

(defn pairs [coll]
  (let [head (first coll) tail (next coll)]
    (when tail
      (lazy-cat
        (map #(vec [head %]) tail)
        (pairs tail)))))

(defn count-in-set [coll rng]
  (count (filter #(contains? coll %) rng)))
 
(defn range-between [a b]
  (range (min a b) (max a b)))
 
(def input (->> "11.txt"
                (slurp)
                (str/split-lines)
                (map seq)))
(def empty-rows (empty-idx input))
(def empty-cols (empty-idx (transpose input)))
(def galaxies (mapcat (fn [y i]
                        (keep-indexed (fn [x ch]
                                        (if (= ch \#) [x y]))
                                      i))
                      (range)
                      input))

(defn distance [n a b]
  (+ (taxicab a b)
     (* (- n 1)
        (+ (count-in-set empty-cols (range-between (first a) (first b)))
           (count-in-set empty-rows (range-between (second a) (second b)))))))

; 11-1
(println (reduce + (map #(apply distance 2 %) (pairs galaxies))))
 
; 11-2
(println (reduce + (map #(apply distance 1000000 %) (pairs galaxies))))