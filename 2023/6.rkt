#lang racket

; 6-1
(define times '(48 98 90 83))
(define records '(390 1103 1112 1360))

(define (count-ways time record)
  (count (lambda (t) (> (* (- time t) t) record))
         (range 1 time)))

(println (apply * (map count-ways times records)))

; 6-2
(println
 (let ([time 48989083]
       [record 390110311121360])
   (for/or ([t (range 1 time)]
            #:when (> (* (- time t) t) record))
     (+ (- time (* t 2)) 1))))
