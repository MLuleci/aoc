(defn remove-char [m i]
    (let [n (m i)]
        (cond
            (not n) m
            (> n 1) (assoc! m i (dec n))
            :else (dissoc! m i))))

(defn add-char [m i]
    (assoc! m i (if-let [n (m i)] (inc n) 1)))

(defn find-sop [v n]
    (loop [i 0 m (transient {})]
        (cond
            (>= i (count v)) -1 ; off the end of the string - not found
            (= (count m) n) i ; found n unique characters in window
            :else (recur 
                    (inc i) 
                    (add-char 
                        (if (>= (- i n) 0) ; if window would be >n characters...
                            (remove-char m (get v (- i n))) ; remove last character
                            m) ; otherwise don't
                        (get v i)))))) ; add current character

; 6-1
(println (find-sop (vec (slurp "6.txt")) 4))

; 6-2
(println (find-sop (vec (slurp "6.txt")) 14))