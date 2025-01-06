(require '[clojure.string :as str])

(def input 
    (->> "3.txt"
        (slurp)
        (str/split-lines)
        (map vec)))

(defn count-trees [grid dx dy]
    (let [width (count (first grid))
          rows (take-nth dy grid)
          cells (map-indexed #(nth %2 (mod (* %1 dx) width)) rows)]
        (count (filter #(= % \#) cells))))

(println (count-trees input 3 1))
(println (reduce * (map 
                        #(apply count-trees input %) 
                        ['(1 1) '(3 1) '(5 1) '(7 1) '(1 2)])))