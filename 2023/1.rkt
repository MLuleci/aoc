#lang racket
(require "common.rkt")

; 1-1
(println
  (apply + (map
            (lambda (line)
              (let ([nums (filter char-numeric? (string->list line))])
                (string->number (string (first nums) (last nums)))))
            (read-lines "1.txt"))))

; 1-2
(define digits
  '(
    "zero"
    "one"
    "two"
    "three"
    "four"
    "five"
    "six"
    "seven"
    "eight"
    "nine"))

(define (number-prefix? s)
  (or (for/first ([d digits]
                  [i (range 10)]
                  #:when (string-prefix? s d))
        i)
      empty))

(define (replace-digits line)
  (filter-not
   empty?
   (for/list ([i (range (string-length line))]
              [n line])
     (if (char-numeric? n)
         (digit->number n)
         (number-prefix? (substring line i))))))

(println
 (apply + (map
           (lambda (line)
             (let ([nums (replace-digits line)])
               (+ (* 10 (first nums)) (last nums))))
     (read-lines "1.txt"))))