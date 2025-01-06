#lang racket
(require "common.rkt")

(apply +
       (map (lambda (line)
              (let* ([parts (car (regexp-match* #px"Card\\s+\\d+: ([0-9 ]+) \\| ([0-9 ]+)" line #:match-select cdr))]
                     [win (list->set (string-split (first parts)))]
                     [got (string-split (second parts))]
                     [n (count (lambda (i) (set-member? win i)) got)])
                (if (= n 0) 0 (expt 2 (- n 1)))))
            (read-lines "4.txt")))