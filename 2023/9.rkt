#lang racket
(require "common.rkt")

; 9-1
(define (parse-nums line)
  (map string->number (string-split line " ")))

(define (reduce nums)
  (if (empty? (dropf nums zero?))
      0
      (+ (last nums)
         (reduce (map - (rest nums) (drop-right nums 1))))))

(apply + (map reduce
              (map parse-nums (read-lines "9.txt"))))

; 9-2
(apply + (map (lambda (i) (reduce (reverse i)))
              (map parse-nums (read-lines "9.txt"))))