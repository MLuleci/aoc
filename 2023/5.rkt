#lang racket
(require "common.rkt")

; 5-1
(define (convert dicts num)
  (or (for/or ([d dicts]
               #:when (and (>= num (second d))
                           (< num (+ (second d) (last d)))))
        (+ (first d) (- num (second d))))
      num))

(define (string->number-list s)
  (map string->number (string-split s)))

(define (parse input)
  (define (iter acc tail)
    (if (empty? tail)
        acc
        (let-values ([(a b) (splitf-at (rest tail) non-empty-string?)])
          (iter (append acc (list (map string->number-list (rest a)))) b))))
  (iter empty input))

(println
 (let* ([input (read-lines "5.txt")]
        [seeds (string->number-list (substring (first input) 6))]
        [dicts (parse (drop input 1))])
   (apply min
          (map (lambda (seed)
                 (foldl (lambda (d i) (convert d i)) seed dicts))
               seeds))))

; 5-2
(define (seed-stream s [i 0])
  (let ([start (first s)]
        [count (second s)])
    (stream-cons (+ start i)
                 (if (>= i (- count 1))
                     (if (= (length s) 2)
                         empty-stream
                         (seed-stream (drop s 2) 0))
                     (seed-stream s (+ i 1))))))

(define (overlap? x y)
  (let-values ([(x1 x2) (apply values x)]
               [(y1 y2) (apply values y)])
    (not (or (< x2 y1) (> x1 y2)))))

(define (map-range x y z)
  (let-values ([(x1 x2) (apply values x)]
               [(y1 y2) (apply values y)]
               [(z1 z2) (apply values z)])
    (let* ([i1 (max x1 y1)]
           [i2 (min x2 y2)]
           [skip (- i1 y1)]
           [take (- i2 i1)])
      (list (+ skip z1) (+ take skip z1)))))

(define (diff-range x y)
  (let-values ([(x1 x2) (apply values x)]
               [(y1 y2) (apply values y)])
    (let* ([i1 (max x1 y1)]
           [i2 (min x2 y2)])
      (match (list i1 i2)
        [(list i1 i2) #:when (and (= i1 x1) (< i2 x2)) (list (list i2 x2))]
        [(list i1 i2) #:when (and (> i1 x1) (= i2 x2)) (list (list x1 i1))]
        [(list i1 i2) #:when (and (= i1 x1) (= i2 x2)) empty]
        [else (list (list x1 i1) (list i2 x2))]))))

(define (convert-range ht src)
  (define (iter sources acc keys)
    (if (empty? keys)
        (append acc sources)
        (let* ([k (first keys)]
               [s (first (filter (lambda (s) (overlap? k s)) sources))]
               [r (filter (lambda (s) (not (overlap? k s))) sources)])
          (iter (append r (diff-range s k))
                (append acc (list (map-range s k (hash-ref ht k))))
                (rest keys)))))
  (iter (list src)
        empty
        (filter (lambda (k) (overlap? k src)) (hash-keys ht))))

(define (dicts->ht dicts)
  (for/list ([dict dicts])
    (for/hash ([d dict])
      (values (list (second d) (+ (second d) (last d)))
              (list (first d) (+ (first d) (last d)))))))

(println
 (let* ([input (read-lines "5.txt")]
        [seeds (string->number-list (substring (first input) 6))]
        [sources (for/list ([i (range 0 (length seeds) 2)])
                   (list (list-ref seeds i) (+ (list-ref seeds i) (list-ref seeds (+ i 1)))))]
        [ranges (dicts->ht (parse (drop input 1)))])
   (apply min (map (lambda (s)
                     (apply min (map first
                                     (foldl (lambda (ht a)
                                              (foldl (lambda (i acc) (append acc (convert-range ht i))) empty a))
                                            (list s)
                                            ranges))))
                   sources))))