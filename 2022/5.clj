(require '[clojure.string :as str])
 
(def input (slurp "5.txt"))
 
; (top ... bottom)
(def stacks
  (->> input
    (str/split-lines)
    (take-while #(not (str/blank? %))) ; take the diagram part
    (drop-last) ; ignore line of numbers
    (map #(flatten (partition 1 4 (drop 1 %)))) ; skip first character, take every 4th character, flatten into sequence
    (reverse) ; reverse, so last row is first
    (apply mapv (fn [& items] (reverse (take-while #(not (= % \space)) items)))))) ; take columns, filter space characters
 
; <count from to>
(def steps
  (->> input
    (str/split-lines)
    (drop-while #(not (str/blank? %))) ; take instructions part
    (drop 1) ; drop blank line
    (map #(map parse-long (re-seq #"\d+" %))))) ; match groups of numbers using RegEx
 
(defn assocs [map coll]
  (loop [c (transient coll)
         items (seq map)]
    (if (nil? items)
      (persistent! c)
      (let [[[key val] & rest] items]
        (recur (assoc! c key val) rest)))))
 
(defn move [stack step]
  (let [[n from to] step
        from-index (- from 1)
        to-index (- to 1)
        prev-from (get stack from-index)
        prev-to (get stack to-index)
        length (count prev-from)
        [items next-from] (split-at n prev-from)
        next-to (into prev-to items)]
    (assocs {from-index next-from to-index next-to} stack)))
 
;; 5-1
(println (str/join
  (map first
    (loop [stack stacks
          [step & rest] steps]
      (if (nil? step)
        stack
        (recur (move stack step) rest))))))

(defn move-2 [stack step]
    (let [[n from to] step
        from-index (- from 1)
        to-index (- to 1)
        prev-from (get stack from-index)
        prev-to (get stack to-index)
        length (count prev-from)
        [items next-from] (split-at n prev-from)
        next-to (into prev-to (reverse items))]
    (assocs {from-index next-from to-index next-to} stack)))

;; 5-2
(->> (loop [stack stacks
            [step & rest] steps]
        (if (nil? step)
            stack
            (recur (move-2 stack step) rest)))
    (map first)
    (str/join)
    (println))