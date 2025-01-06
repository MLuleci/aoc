(require '[clojure.string :as str])

(def input 
    (->> "1.txt"
        (slurp)
        (str/split-lines)
        (map parse-long)
        (into #{})))

(defn two-sum [s n]
    (seq (filter #(contains? s (- n %)) s)))

(println (reduce * (two-sum input 2020)))
(println (reduce * (filter #(when-let [x (two-sum input (- 2020 %))] %) input)))