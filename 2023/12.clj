(require '(clojure set [string :as str]))

(defn count-adjacent [coll]
  (map count
    (reduce (fn [v i]
      (let [l (or (last v) #{})
            h (vec (drop-last 1 v))
            m (if (empty? l) (- i 1) (apply max l))]
          (if (= (- i m) 1) ; non-empty or consecutive
            (conj h (conj l i))
            (conj v #{i}))))
      []
      (sort coll))))
 
(defn k-combs [coll k]
  (defn iter [comb rem]
    (if (= (count comb) k)
      [comb]
      (if (empty? rem)
        []
        (let [h (first rem)
              t (rest rem)]
          (concat (iter (conj comb h) t)
                  (iter comb t))))))
  (vec (iter #{} coll)))

(defn valid? [sel req]
  (= (count-adjacent sel) req))

(defn indices-of [pred coll]
  (filter identity
    (map #(and (pred %1) %2)
      coll
      (range (count coll)))))

(defn solve-row [row req]
  (let [q-idx (indices-of #(= % \?) row)
        h-idx (set (indices-of #(= % \#) row))
        k (- (apply + req) (count h-idx))
        cmb (k-combs q-idx k)]
    (filter #(valid? (clojure.set/union % h-idx) req) cmb)))

(defn parse-nums [s]
  (map parse-long (str/split s #",")))

; 12-1
(->> "12.txt"
  (slurp)
  (str/split-lines)
  (map #(let [[x y] (str/split % #" ")] [x (parse-nums y)]))
  (map #(count (apply solve-row %)))
  (reduce +)
  (println))

(def solve-dp
  (memoize (fn [seq grp n]
             (let [[g & nxt] grp
                   [c & rem] seq]
               (cond
                 (empty? seq) (if (empty? grp) 1 0)
                 (= c \#) (cond
                            (or (empty? grp) (>= n g)) 0 ; too many #'s
                            (and (= (count seq) (count grp) 1) (= g (+ n 1))) 1 ; special last #
                            :else (solve-dp rem grp (+ n 1))) ; grow group
                 (= c \.) (if (> n 0)
                            (if (or (empty? grp) (not= n g))
                              0 ; group too big
                              (solve-dp rem nxt 0)) ; group done
                            (solve-dp rem grp 0)) ; not growing group, skip .
                 (= c \?) (+ (solve-dp (conj rem \#) grp n) ; try ? -> #
                             (solve-dp (conj rem \.) grp n))))))) ; try ? -> .

(defn dup5 [coll sep]
  (str/join sep (take 5 (repeat coll))))

(->> "12.txt"
  (slurp)
  (str/split-lines)
  (map #(let [[x y] (str/split % #" ")] 
          [(seq (dup5 x "?")) 
           (parse-nums (dup5 y ","))
           0]))
  (map #(apply solve-dp %))
  (reduce +)
  (println))