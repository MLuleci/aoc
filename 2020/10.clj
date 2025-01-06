(require '[clojure.string :as str])

(def adapters
  (->> "10.txt"
    (slurp)
    (str/split-lines)
    (map parse-long)
    (sort)))

(let [diffs (frequencies (map - adapters (conj adapters 0)))]
  (println (* (diffs 1) (+ (diffs 3) 1))))

(let [m (apply max adapters)
      comb (reduce (fn [a v]
                    ; a = map of adapter -> number of combinations
                    (assoc a v (reduce + (for [i '(1 2 3) 
                                              :let [x (a (- v i))] 
                                              :when x]
                                          x))))
                  { 0 1 } 
                  adapters)]
  (println (comb m)))