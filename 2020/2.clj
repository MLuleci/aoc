(require '[clojure.string :as str])

(defn parse-line [l]
    (let [[_ min max char str] (re-matches #"(\d+)-(\d+) (.): (.+)" l)]
        (vector (parse-long min) (parse-long max) (.charAt char 0) str)))

(defn valid-count? [min max char str]
    (let [x (count (filter #(= % char) str))]
        (and (<= min x) (>= max x))))

(defn valid-position? [min max char str]
    (= 1 (count 
        (filter
            #(or (= (dec min) %) (= (dec max) %)) 
            (keep-indexed #(when (= char %2) %1) str)))))

(def input
    (->> "2.txt"
        (slurp)
        (str/split-lines)
        (map parse-line)))

(println (count (filter #(apply valid-count? %) input)))
(println (count (filter #(apply valid-position? %) input)))