(require '[clojure.string :as str])

(defn reduce-row 
    ([row] (reduce-row row -1 []))
    ([row m coll]
        (let [[f & r] row]
            (if-not row
                coll
                (recur r (max m f) (conj coll (< m f)))))))

(defn ltr [g f]
    (map f g))

(defn rtl [g f]
    (map #(reverse (f (reverse %))) g))

(defn ttb [g f]
    (apply map list (apply map #(f %&) g)))

(defn btt [g f]
    (apply map list (apply map #(reverse (f (reverse %&))) g)))

(defn or-seq 
    ([f & seq] (or-seq (conj seq f)))
    ([seq] (reduce #(or %1 %2) seq)))

(def nums { \0 0 \1 1 \2 2 \3 3 \4 4 \5 5 \6 6 \7 7 \8 8 \9 9 })

(def grid 
    (->> "8.txt"
        (slurp)
        (str/split-lines)
        (mapv #(mapv nums %))))

(def visible
    (map
        (fn [& rows] (apply map or-seq rows)) 
        (rtl grid reduce-row)
        (ltr grid reduce-row)
        (ttb grid reduce-row)
        (btt grid reduce-row)))

; 8-1
(println (count (filter identity (flatten visible))))

(defn scenic-score
    ([coll] (scenic-score coll 0 []))
    ([coll index result]
        (if (>= index (count coll))
            result
            (let [[head [current & _]] (split-at index coll)
                blocker (reduce 
                    #(if (>= %2 current)
                        (reduced (dec %1))
                        (dec %1))
                    index (reverse head))]
                (recur coll (inc index) (conj result (- index blocker)))))))

(def scores
    (map (fn [& rows] (apply map * rows))
        (rtl grid scenic-score)
        (ltr grid scenic-score)
        (ttb grid scenic-score)
        (btt grid scenic-score)))

; 8-2
(println (apply max (flatten scores)))