(require '[clojure.string :as str])

(def moves {"A" 1 "B" 2 "C" 3 "X" 1 "Y" 2 "Z" 3})

;      1  2  3
; 1r - r3 p6 s0
; 2p - r0 p3 s6
; 3s - r6 p0 s3
;  0 - 3
; -1 - 6
; -2 - 0
;  1 - 0
;  2 - 6

(defn do-round-1 [a b]
    (let [i (moves a)
          j (moves b)]
        (+ (case (- i j)
                 0 3
                -1 6
                 1 0
                -2 0
                 2 6)
            j)))

;; 2-1
(->> "2.txt"
    (slurp)
    (str/split-lines)
    (map #(str/split % #" "))
    (map #(apply do-round-1 %))
    (apply +)
    (println))

(def lose {"A" "Z" "B" "X" "C" "Y"})
(def win {"A" "Y" "B" "Z" "C" "X"})

(defn do-round-2 [a b]
    (case b
        "X" (do-round-1 a (lose a))
        "Y" (do-round-1 a a)
        "Z" (do-round-1 a (win a))))

;; 2-2
(->> "2.txt"
    (slurp)
    (str/split-lines)
    (map #(str/split % #" "))
    (map #(apply do-round-2 %))
    (apply +)
    (println))