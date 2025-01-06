#lang racket
(require "common.rkt")

; 3-1
(define input (read-lines "3.txt"))
(define width (string-length (first input)))
(define height (length input))

(define (is-symbol? ch)
  (not (or (char-numeric? ch) (eq? ch #\.))))

(define (get-char in x y)
  (string-ref (list-ref in y) x))

(define (used? in x y n)
  (let ([xrange (range (max (1- x) 0) (min (+ x n 1) width))]
        [yrange (range (max (1- y) 0) (min (+ y 2) height))])
    (foldl (lambda (yy i)
             (or (foldl (lambda (xx j)
                          (or (is-symbol? (get-char in xx yy)) j))
                        #f
                        xrange)
                 i))
           #f
           yrange)))

(define (do-line in y)
  (let ([line (list-ref in y)])
    (define (iter x acc)
      (let ([pos (regexp-match-positions #px"\\d+" line x)])
        (if (not pos)
            acc
            (let ([start (caar pos)]
                  [stop (cdar pos)])
              (if (used? in start y (- stop start))
                  (iter stop (+ acc (string->number (substring line start stop))))
                  (iter stop acc))))))
    (iter 0 0)))

(println
 (foldl (lambda (y acc) (+ acc (do-line input y))) 0 (range height)))

; 3-2
(define (touch seen x y)
  (if (char-numeric? (get-char input x y))
      (string->number
       (apply string
              (append
               (reverse
                (for/list ([i (range (1- x) -1 -1)]
                           #:break (not (char-numeric? (get-char input i y))))
                  (set-add! seen (list i y))
                  (get-char input i y)))
               (for/list ([i (range x width)]
                          #:break (not (char-numeric? (get-char input i y))))
                 (set-add! seen (list i y))
                 (get-char input i y)))))
      #f))

(define (around x y)
  (let ([seen (mutable-set)]
        [xrange (range (max (1- x) 0) (min (+ x 2) width))]
        [yrange (range (max (1- y) 0) (min (+ y 2) height))])
    (filter identity
            (flatten (map (lambda (yy)
                            (for/list ([xx xrange] #:when (not (or (and (= xx x) (= yy y)) (set-member? seen (list xx yy)))))
                              (touch seen xx yy)))
                          yrange)))))
               
(println
 (for/sum ([y (range height)])
   (let ([p (or (regexp-match-positions* "\\*" (list-ref input y) #:match-select caar) '())])
     (foldl (lambda (x a)
              (let ([n (around x y)])
                (if (= (length n) 2)
                    (+ a (apply * n))
                    a)))
            0 p))))