(defun fizzbuzz (n)
  "Print numbers from 1 to N with Fizz, Buzz, or FizzBuzz substitutions."
  (loop for i from 1 to n do
       (cond
         ((and (zerop (mod i 3)) (zerop (mod i 5)))
          (format t "FizzBuzz~%"))
         ((zerop (mod i 3))
          (format t "Fizz~%"))
         ((zerop (mod i 5))
          (format t "Buzz~%"))
         (t
          (format t "~D~%" i))))
  (values))


