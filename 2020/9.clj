(require '[clojure.string :as str])

(def input
  (->> "9.txt"
    (slurp)
    (str/split-lines)
    (mapv parse-long)))

(defn two-sum [coll target]
  (let [compliment (reduce (fn [a v] (assoc a v (- target v))) {} coll)]
    (some #(contains? compliment (compliment %)) coll)))

(def invalid
  (let [[preamble nums] (split-at 25 input)]
    (reduce (fn [a v]
              (if (two-sum a v)
                (conj (vec (rest a)) v)
                (reduced v)))
            preamble
            nums)))
(println invalid)

(loop [start 0 len 0]
  (let [sv (subvec input start (+ start len)) sum (reduce + sv)]
    (if (= sum invalid)
      (println (+ (apply min sv) (apply max sv)))
      (if (< sum invalid)
        (recur start (inc len))
        (recur (inc start) (dec len))))))