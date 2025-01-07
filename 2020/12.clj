(require '[clojure.string :as str])

(def instructions
  (->> "12.txt"
    (slurp)
    (str/split-lines)
    (map #(if-let [[_ a n] (re-matches #"(.)(\d+)" %)] 
            [(first a) (parse-long n)]))))

(defn turn [facing direction degrees]
  (let [index ({ \N 0 \E 1 \S 2 \W 3 } facing)
        delta ((if (= direction \L) 
                { 90 -1 180 -2 270 -3} 
                { 90 +1 180 +2 270 +3}) degrees)
        new-index (mod (+ index delta) 4)]
    ({ 0 \N 1 \E 2 \S 3 \W} new-index)))

(defn step [direction n x y]
  (case direction
    \N [x (- y n)]
    \E [(+ x n) y]
    \S [x (+ y n)]
    \W [(- x n) y]))

(defn rotate [direction degrees x y]
  (case [direction degrees]
    [\L 90] [y (- x)]
    [\L 180] [(- x) (- y)]
    [\L 270] [(- y) x]
    [\R 90]  [(- y) x]
    [\R 180] [(- x) (- y)]
    [\R 270] [y (- x)]))

(println 
  (loop [facing \E x 0 y 0 [instr & rest] instructions]
    (if (nil? instr)
      (+ x y)
      (let [[action n] instr]
        (cond
          (= action \L) (recur (turn facing \L n) x y rest)
          (= action \R) (recur (turn facing \R n) x y rest)
          :else (let [direction (if (= action \F) facing action)
                      [xx yy] (step direction n x y)]
                  (recur facing xx yy rest)))))))

(loop [wx 10 wy -1 sx 0 sy 0 [instr & rest] instructions]
  (if (nil? instr)
    (+ (abs sx) (abs sy))
    (let [[action n] instr]
      (if (#{ \L \R } action)
        (let [[nwx nwy] (rotate action n wx wy)]
          (recur nwx nwy sx sy rest))
        (case action
          \N (recur wx (- wy n) sx sy rest)
          \E (recur (+ wx n) wy sx sy rest)
          \S (recur wx (+ wy n) sx sy rest)
          \W (recur (- wx n) wy sx sy rest)
          \F (recur wx wy (+ sx (* n wx)) (+ sy (* n wy)) rest))))))