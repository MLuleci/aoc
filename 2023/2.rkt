#lang racket
(require "common.rkt")

; 2-1
(define bag
  (make-hash '(("red" . 12) ("green" . 13) ("blue" . 14))))

(define (get-games s)
  (map
   (lambda (round)
     (let ([pulls (string-split round ",")])
       (map
        (lambda (pull)
          (let ([pair (string-split pull)])
            (list (string->number (first pair)) (last pair))))
        pulls)))
   (string-split (substring s (+ (string-index s #\:) 1)) ";" #:trim? #t)))

(define (game-possible? g)
  (for/and ([r g]) ; rounds
    (for/and ([p r]) ; pulls
      (>= (hash-ref bag (last p)) (first p)))))

(println
 (let ([lines (read-lines "2.txt")])
   (for/sum ([g (map get-games lines)]
             [i (range (length lines))]
             #:when (game-possible? g))
     (+ i 1))))

; 2-2
(println
 (apply +
        (map
         (lambda (ht) (apply * (hash-values ht))) ; power
         (let ([lines (read-lines "2.txt")])
           (for/list ([g (map get-games lines)]) ; games
             (let ([ht (make-hash '(("red" . 0) ("green" . 0) ("blue" . 0)))])
               (for ([r g]) ; rounds
                 (for ([p r]) ; pulls
                   (hash-set! ht
                              (last p)
                              (max (hash-ref ht (last p))
                                   (first p)))))
               ht))))))