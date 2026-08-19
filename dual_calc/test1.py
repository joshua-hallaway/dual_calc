import dual as d
import equation as eq
import numpy as np

while True:
    f=input("f(x) = ")
    if f == "":
        break
    point=input("at x=")
    if point == "x":
        print(eq.deriv(eq.Parser(eq.tokenize(f)).parse(),eq.Variable("x")))
    else:
        print(eq.deriv(eq.Parser(eq.tokenize(f)).parse(),float(point)))