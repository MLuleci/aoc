#lang racket

(define (read-lines path)
  (call-with-input-file path
    (lambda (in)
      (define (iter lines)
        (let ([line (read-line in 'any)])
          (if (eof-object? line)
              (reverse lines)
              (iter (cons line lines)))))
      (iter empty))))

(define (read-file path)
  (call-with-input-file path
    (lambda (in)
      (port->string in))))

(define (zip/cons . lists)
  (apply map cons lists))

(define (zip/list . lists)
  (apply map list lists))

(define (digit->number ch)
  (- (char->integer ch) 48))

(define (string-index s ch)
  (index-of (string->list s) ch))

(define (1+ x) (+ x 1))

(define (1- x) (- x 1))

(define (stream-string s [i 0])
    (stream-cons (string-ref s i)
                 (if (< (1+ i) (string-length s))
                     (stream-string s (1+ i))
                     empty-stream)))

(provide (all-defined-out))