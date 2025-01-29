(require '[clojure.string :as str])
 
(defn contains? [a b]
  (and
    (<= (first a) (first b))
    (>= (last a) (last b))))
 
(defn parse-range [s]
  (let [ [start end] (str/split s #"-") ]
    (list (parse-long start) (parse-long end))))
 
;; 4-1
(->> "4.txt"
  (slurp)
  (str/split-lines)
  (map (fn [s] (map parse-range (str/split s #","))))
  (filter #(or (apply contains? %) (apply contains? (reverse %))))
  (count)
  (println))
 
(defn overlaps? [a b]
  (and
    (<= (first a) (last b))
    (<= (first b) (last a))))
 
;; 4-2
(->> "4.txt"
  (slurp)
  (str/split-lines)
  (map (fn [s] (map parse-range (str/split s #","))))
  (filter #(apply overlaps? %))
  (count)
  (println))