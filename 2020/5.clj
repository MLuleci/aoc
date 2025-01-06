(require '[clojure.string :as str])

(defn decode 
    ([s]
        (let [[row col] (split-at 7 s)]
            [(decode row 128 \F \B) (decode col 8 \L \R)]))
    ([s n lm hm]
        (loop [lo 0 hi n coll s]
            (if (empty? coll)
                lo
                (let [mid (quot (+ hi lo) 2) [[head] tail] (split-at 1 coll)]
                    (cond
                        (= head lm) (recur lo mid tail)
                        (= head hm) (recur mid hi tail)))))))

(defn seat-id [[r c]] (+ (* r 8) c))

(def ids
    (->> "5.txt"
        (slurp)
        (str/split-lines)
        (map decode)
        (map seat-id)))

(println (reduce max ids))
(println 
    (->> ids
        (sort)
        (reduce (fn [a v] (if (> (- v a) 1) (reduced (+ a 1)) v)))))