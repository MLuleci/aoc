(require '[clojure.string :as str])

(defrecord Bag [name contains])

(defn parse [s]
    (let [[name tail] (str/split s #" bags contain (no other bags.)?")]
        (->Bag
            name
            (->> (or tail "")
                (#(str/split % #" bags?.{1,2}"))
                (keep #(when-let [m (re-matches #"(\d+) (.+)" %)] (rest m)))
                (map (fn [[i n]] [n (parse-long i)]))
                (into {})))))

(def bags
    (->> "7.txt"
        (slurp)
        (str/split-lines)
        (map parse)))

(defn get-bag [name]
    (first (filter #(= (:name %) name) bags)))

(def m-contains 
    (memoize (fn [bag]
        (let [children (:contains bag)]
            (if (empty? children)
                children
                (->> children
                    (map (fn [[name mul]] 
                            (reduce-kv (fn [a k v] (assoc a k (* v mul))) {}
                                        (m-contains (get-bag name)))))
                    (apply merge-with + children)))))))

(println (->> bags
            (map m-contains)
            (filter #(contains? % "shiny gold"))
            (count)))

(println (->> (get-bag "shiny gold")
            (m-contains)
            (reduce-kv (fn [a k v] (+ a v)) 0)))