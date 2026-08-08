import numpy as np
class Dual:
    def __init__(self, real, dual):
        self.real=real
        self.dual=dual

    @staticmethod
    def to_dual(other):
        if isinstance(other, Dual): 
            return other
        else: 
            return Dual(real=other, dual=0)

    def __repr__(self):
        return f"Dual(real={self.real}, dual={self.dual})"

    def __eq__(self, other):
        try: 
            other = Dual.to_dual(other)
        except TypeError:
            return False
        return (abs(self.real - other.real) < 1e-12 and abs(self.dual - other.dual) < 1e-12) 

    def __add__(self, other):
        try: 
             other=Dual.to_dual(other)
        except TypeError:
            raise TypeError("Only numeric values can be added to Dual")
        a=self.real
        b=self.dual
        c=other.real
        d=other.dual
        return Dual(a+c,b+d)

    def __radd__(self, other: "int | float | Dual"):
        return self+other

    def __sub__(self,other: "int | float | Dual"):
        try: 
             other=Dual.to_dual(other)
        except TypeError:
            raise TypeError("Only numeric values can be subtracted from Dual")
        a=self.real
        b=self.dual
        c=other.real
        d=other.dual
        return Dual(a-c,b-d) 

    def __rsub__(self,other: "int | float | Dual"):
        try: 
             other=Dual.to_dual(other)
        except TypeError:
            raise TypeError("Dual can only be subtracted from numeric values")
        a=self.real
        b=self.dual
        c=other.real
        d=other.dual
        return Dual(c-a,d-b) 

    def __neg__(self):
        return Dual(-self.real, -self.dual) 

    def __mul__(self, other: "int | float | Dual"):
        try: 
             other=Dual.to_dual(other)
        except TypeError:
            raise TypeError("Only numeric values can be multiplied with Dual")
        a=self.real
        b=self.dual
        c=other.real
        d=other.dual
        return Dual(a*c,a*d+b*c)

    def __rmul__(self, other: "int | float | Dual"):
        return self*other

    def __truediv__(self, other: "int | float | Dual"):
        try: 
             other=Dual.to_dual(other)
        except TypeError:
            raise TypeError("Only numeric values can be divided with Dual")
        if other.real==0: 
            raise ZeroDivisionError("Division by zero")
        a=self.real
        b=self.dual
        c=other.real
        d=other.dual
        return Dual(a/c,(b*c-a*d)/c**2)

    def __rtruediv__(self, other):
        try: 
             other=Dual.to_dual(other)
        except TypeError:
            raise TypeError("Only numeric values can be divided with Dual")
        if self.real==0: 
            raise ZeroDivisionError("Division by zero")
        a=self.real
        b=self.dual
        c=other.real
        d=other.dual
        return Dual(c/a,(d*a-c*b)/a**2)

    def __pow__(self, other):
        try:
           other=Dual.to_dual(other)
        except TypeError:
           raise TypeError("Power must be numeric")
        a=self.real
        b=self.dual
        c=other.real
        d=other.dual
        if a<=0:
            raise ValueError("Power requires a positive base")
        return Dual(a**c,a**c*(d*np.log(a)+(b*c)/a))

    def __rpow__(self, other):
        try:
           other=Dual.to_dual(other)
        except TypeError:
           raise TypeError("Power must be numeric")
        a=self.real
        b=self.dual
        c=other.real
        d=other.dual
        if c<=0:
            raise ValueError("Power requires a positive base")
        return Dual(c**a,c**a*(b*np.log(c)+(d*a)/c))

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        if method!="__call__":
            return NotImplemented
        if kwargs.get("out") is not None:
            return NotImplemented
        if not any(isinstance(x, Dual) for x in inputs):
            return NotImplemented
        x=next(i for i in inputs if isinstance(i,Dual))
        a=x.real
        b=x.dual
        if ufunc is np.sin:
            return Dual(np.sin(a),b*np.cos(a))
        if ufunc is np.cos:
            return Dual(np.cos(a),-b*np.sin(a))
        if ufunc is np.tan:
            return Dual(np.tan(a),b/np.cos(a)**2)
        return NotImplemented
