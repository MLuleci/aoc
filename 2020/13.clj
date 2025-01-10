(require '[clojure.string :as str])

(def text (->> "13.txt" 
               (slurp)
               (str/split-lines)))
(def earliest (parse-long (first text)))
(def busses (let [items (str/split (second text) #",")]
            (for [i (range (count items)) 
                  :let [item (nth items i)] 
                  :when (not= item "x")]
              [i (parse-long item)])))

(println
  (->> ids
    (map (fn [[_ i]] (vector (- i (mod earliest i)) i)))
    (sort)
    (first)
    (apply *)))

; Mathchads, I kneel.
(println
  (loop [time 0 step 1 [item & tail] busses]
    (if (nil? item)
      time
      (let [[offset bus] item
            i (first (drop-while #(not= (mod (+ time (* % step) offset) bus) 0) (range)))]
        (recur (+ time (* i step)) (* step bus) tail)))))