(require '(clojure [string :as str] [set :as set]))

(def groups
    (->> "6.txt"
        (slurp)
        (#(str/split % #"\n\n"))
        (map (fn [g] (map #(into #{} %) (str/split-lines g))))))

(println
    (->> groups
        (map #(count (reduce set/union %)))
        (reduce +)))

(println
    (->> groups
        (map #(count (reduce set/intersection %)))
        (reduce +)))