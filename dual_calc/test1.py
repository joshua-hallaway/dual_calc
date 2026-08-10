import dual as d
import equation as eq

while True:
    f=input("f(x) = ")
    if f in ("quit",""):
        break
    point=float(input("at x = "))
    f=eq.Parser(eq.tokenize(f)).parse()
    print(f'f({point})={f.eval({"x":point})}')
    print(f"f'({point})={eq.deriv(f,point)}")