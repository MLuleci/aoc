(require '[clojure.string :as str])

;; 1-1
(->> "1.txt"
    (slurp)
    ((fn [s] (str/split s #"\n\n")))
    (map (fn [coll] (map parse-long (str/split-lines coll))))
    (map #(apply + %))
    (apply max)
    (println))

;; 1-2
(->> "1.txt"
    (slurp)
    ((fn [s] (str/split s #"\n\n")))
    (map (fn [coll] (map parse-long (str/split-lines coll))))
    (map #(apply + %))
    (sort)
    (take-last 3)
    (apply +)
    (println))