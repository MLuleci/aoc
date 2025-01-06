(require '(clojure [set :as set] [string :as str]))

(def required-fields #{ "byr" "iyr" "eyr" "hgt" "hcl" "ecl" "pid" })

(def valid-eye-colors #{ "amb" "blu" "brn" "gry" "grn" "hzl" "oth" })

(def string-fields #{ "hgt" "pid" "hcl" "ecl" })

(defn to-map [x] 
    (apply hash-map 
        (mapcat 
            #(let [[k v] (str/split % #":")] 
                [k (if (contains? string-fields k) v (or (parse-long v) v))])
            x)))

(defn collect-by [coll pred]
    (let [inv-pred #(not (pred %))]
        (loop [groups [] items coll]
            (if (empty? items)
                groups
                (let [[head tail] (split-with inv-pred items)]
                    (recur (conj groups head) (rest tail)))))))

(defn valid-field? [key value]
    (case key
        "byr" (<= 1920 value 2002)
        "iyr" (<= 2010 value 2020)
        "eyr" (<= 2020 value 2030)
        "hgt" (when-let [match (re-matches #"(\d+)(cm|in)" value)]
                    (let [[_ i unit] match height (parse-long i)]
                        (if (= unit "cm")
                            (<= 150 height 193)
                            (<= 59 height 76))))
        "hcl" (re-matches #"#[a-f0-9]{6}" value)
        "ecl" (contains? valid-eye-colors value)
        "pid" (re-matches #"\d{9}" (str value))
        true))

(defn valid-passport? [p]
    (every? #(apply valid-field? %) p))

(def input 
    (map to-map 
        (collect-by 
            (->> "4.txt"
                (slurp)
                (str/split-lines)
                (mapcat #(str/split % #" ")))
            str/blank?)))

(def silver (filter #(set/subset? required-fields (set (keys %))) input))

(println (count silver))
(println (count (filter valid-passport? silver)))