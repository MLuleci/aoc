(require '(clojure [string :as str]))
                    
(defn parse-instruction [instr]
    (condp re-matches instr
        #"addx (-?\d+)" :>> (fn [[_ v]] `(0 ~(Integer/parseInt v)))
        #"noop" '(0)))

(def history
    (->> "10.txt"
        (slurp)
        (str/split-lines)
        (reduce #(concat %1 (parse-instruction %2)) '())
        (reduce #(conj %1 (+ %2 (first %1))) '(1))
        (reverse)
        (vec)))
    
; 10-1
(println (reduce #(+ %1 (* %2 (get history (dec %2)))) 0 (range 20 221 40)))

; 10-2
(doseq [line (->> history 
            (map-indexed #(if (<= (abs (- (mod %1 40) %2)) 1) \# \.))
            (partition 40 40))]
    (println line))