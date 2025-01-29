(require '(clojure [string :as str]))

(defstruct point :x :y)

(defn touching? [p1 p2]
    (and (<= (abs (- (:x p1) (:x p2))) 1)
         (<= (abs (- (:y p1) (:y p2))) 1)))

(defstruct move :direction :steps)

(defn parse-move [line]
    (let [[_ d s] (re-matches #"(.) (\d+)" line)]
        (struct move (keyword d) (Integer/parseInt s))))

(defn move-point [p m]
    (case (:direction m)
        :U (update p :y inc)
        :D (update p :y dec)
        :L (update p :x dec)
        :R (update p :x inc)))

(defn sign [x]
    (cond 
        (< x 0) -1
        (= x 0) 0
        (> x 0) 1))

(defn follow [h t]
    (if (touching? h t)
        t
        (let [{x :x y :y} t
              dx (sign (- (:x h) (:x t)))
              dy (sign (- (:y h) (:y t)))]
            (struct point (+ x dx) (+ y dy)))))

(defn do-move [m rope visits]
    (if (= (:steps m) 0)
        (list rope visits)
        (let [[head & rest] rope
              new-rope (reduce 
                (fn [r k] (conj r (follow (last r) k)))
                [(move-point head m)] 
                rest)
              tail (last new-rope)]
            (recur 
                (update m :steps dec) 
                new-rope
                (conj visits tail)))))

(defn make-rope [len] (vec (for [_ (range len)] (struct point 0 0))))

; 9-1
(->> "9.txt"
    (slurp)
    (str/split-lines)
    (map parse-move)
    (reduce #(apply do-move %2 %1) (list (make-rope 2) #{}))
    (last)
    (count)
    (println))

; 9-2
(->> "9.txt"
    (slurp)
    (str/split-lines)
    (map parse-move)
    (reduce #(apply do-move %2 %1) (list (make-rope 10) #{}))
    (last)
    (count)
    (println))