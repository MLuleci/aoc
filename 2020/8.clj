(require '[clojure.string :as str])

(defn run [coll]
    (loop [i 0 acc 0 seen (transient #{})]
        (if (or (= i (count coll)) (contains? seen i))
            [i acc]
            (let [[op n] (nth coll i) next (conj! seen i)]
                (case op
                    "nop" (recur (+ i 1) acc next)
                    "acc" (recur (+ i 1) (+ acc n) next)
                    "jmp" (recur (+ i n) acc next))))))

(defn find-next [coll start]
    (reduce (fn [a [op _]] 
                (if (contains? #{ "nop" "jmp" } op)
                    (reduced a)
                    (+ a 1)))
            start
            (drop start coll)))

(defn swap-instr [coll index]
    (let [[head [[op n] & tail]] (split-at index coll)
           other (if (= op "nop") "jmp" "nop")]
        (concat head [[other n]] tail)))

(def instr
    (->> "8.txt"
        (slurp)
        (str/split-lines)
        (mapv #(let [[i n] (str/split % #" ")] [i (parse-long n)]))))

(println (second (run instr)))
(println
    (loop [start 0]
        (let [index (find-next instr start)
              swapped (swap-instr instr index)
              [i acc] (run swapped)]
            (if (= i (count instr))
                acc
                (recur (+ index 1))))))