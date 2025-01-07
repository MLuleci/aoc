(def input
    (->> "11.txt"
      (slurp)
      (clojure.string/split-lines)))
(def height (count input))
(def width (count (first input)))

(def init 
    (->> input
      (mapcat (fn [i line] (map-indexed (fn [j ch] [`(~i ~j) ch]) line)) (range))
      (into {})))

(defn neighbors-1 [[i j]]
  (for [di [-1 0 1] 
        dj [-1 0 1] 
        :when (and
          (or (not= di 0) (not= dj 0))
          (<= 0 (+ i di) (dec height))
          (<= 0 (+ j dj) (dec width)))]
    [(+ i di) (+ j dj)]))

(defn neighbors-n [[i j]]
  (keep identity
        (for [di [-1 0 1] 
              dj [-1 0 1]
              :when (or (not= di 0) (not= dj 0))]
          (loop [ii (+ i di) jj (+ j dj)]
            (if (and (<= 0 ii (dec height)) (<= 0 jj (dec width)))
              (if (= (get init [ii jj]) \.)
                (recur (+ ii di) (+ jj dj))
                [ii jj])
              nil)))))

(defn step [state neighbors-fn threshold]
  (reduce (fn [a [pos ch]]
            (let [n (count (filter #(= \# (get state %)) (neighbors-fn pos)))]
              (assoc a pos 
                (cond
                  (and (= ch \L) (= n 0)) \#
                  (and (= ch \#) (>= n threshold)) \L
                  :else ch))))
          {}
          state))

(defn until-stable [state neighbors-fn threshold]
  (let [stepped (step state neighbors-fn threshold)]
    (if (= state stepped)
      state
      (recur stepped neighbors-fn threshold))))

(println (count (filter (fn [[pos ch]] (= ch \#)) (until-stable init neighbors-1 4))))
(println (count (filter (fn [[pos ch]] (= ch \#)) (until-stable init neighbors-n 5))))
