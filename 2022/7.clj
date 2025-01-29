(require '[clojure.string :as str])

(defn parse-logs 
    ([logs] (parse-logs logs {} []))
    ([logs tree path]
        (let [[line & tail] logs]
            (cond
                (not logs) tree
                (str/starts-with? line "$ cd")
                    (let [[_ dir] (re-matches #"\$ cd (.+)" line)
                        new-path (conj path dir)]
                        (if (= dir "..")
                            (recur tail tree (pop path)) ; go up
                            (recur tail (assoc-in tree new-path {:size 0}) new-path))) ; go down
                (or
                    (str/starts-with? line "$ ls")
                    (str/starts-with? line "dir"))
                        (recur tail tree path) ; skip
                :else
                    (let [[_ match] (re-matches #"(\d+) .+" line)
                          size (parse-long match)
                          paths (for [i (range (count path))]
                                    (conj (vec (take (+ i 1) path)) :size))
                          node (reduce #(update-in %1 %2 + size) tree paths)] ; increment nodes along path
                        (recur tail node path))))))

(defn get-sizes [node]
    (let [size (node :size)
          children (vals (dissoc node :size))]
        (if (> (count children) 0)
            (conj (flatten (mapv get-sizes children)) size)
            [size])))

(def sizes
    (->> "7.txt"
        (slurp)
        (str/split-lines)
        (#(parse-logs %))
        (#(get-sizes (get % "/")))))

; 7-1
(->> sizes
    (filter #(<= % 100000))
    (apply +)
    (println))

; 7-2
(def needed (- 30000000 (- 70000000 (first sizes))))
(->> sizes
    (filter #(>= % needed))
    (apply min)
    (println))