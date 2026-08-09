import numpy as np
class Dual:
    """A number with both a real and dual component of the form a+bϵ.

    This class allows for the creation of dual numbers as well as arithmetic between dual numbers and numeric values

    Attributes:
        real (int | float): the real portion of the dual number
        dual (int | float): the dual portion of the dual number
    """
    def __init__(self, real: int | float, dual: int | float):
        """Initializes a dual number with a real and dual part

        Initializes a dual number with a real and dual component

        Args:
            real (int | float): the real portion of the dual number
            dual (int | float): the dual portion of the dual number
        """
        if not isinstance(real, (int,float)) or not isinstance(dual,(int,float)):
            raise TypeError("All arguments must be numeric")
        self.real=real
        self.dual=dual

    @staticmethod
    def to_dual(other: "int | float | Dual"):
        """Converts int and float values to Dual objects

        Args:
            other (int | float | Dual): the object to be converted to a Dual
        
        Returns:
            Dual: the Dual version of the int, float, or Dual value
        """
        if not isinstance(other,(int,float,Dual)):
            raise TypeError("Only numeric values can be converted to Duals")
        if isinstance(other, Dual): 
            return other
        else: 
            return Dual(real=other, dual=0)

    def __repr__(self):
        """Returns a string representation of the Dual number

        This method is implemented when the repr, print, or str function is used on a Dual

        Returns:
            str: the dual number formatted as "Dual(real={real}, dual={dual})"
        """
        return f"Dual(real={self.real}, dual={self.dual})"

    def __eq__(self, other: "int  | float | Dual"):
        """Determines if the Dual is equal to a different Dual, int, or float

        This method is implemented when the binary operator (==) is used after a Dual

        Args:
            other (int | float | Dual): the other object being compared to the Dual

        Returns:
            bool: The truth value of the equality
        """
        try: 
            other = Dual.to_dual(other)
        except TypeError:
            return False
        return (abs(self.real - other.real) < 1e-12 and abs(self.dual - other.dual) < 1e-12) 

    def __add__(self, other: "int | float | Dual"):
        """Performs addition on Duals

        This method is implemented with the binary operator (+) is used after a Dual

        Args:
            other (int | float | Dual): the other object being added to the Dual
        
        Returns:
            Dual: the sum of the Dual and other argument
        """
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
        """Performs reverse addition on Duals

        This method is implemented when the binary operator (+) is used after a numeric value and before a Dual

        Args:
            other (int | float | Dual): the other object being added to the Dual
        
        Returns:
            Dual: the sum of the Dual and other argument
        """
        return self+other

    def __sub__(self, other: "int | float | Dual"):
        """Performs subtraction of Duals

        This method is implemented when the binary operator (-) is used after a Dual

        Args:
            other (int | float | Dual): the other object being subtracted from the Dual
        
        Returns:
            Dual: the difference of the Dual and other argument
        """
        try: 
             other=Dual.to_dual(other)
        except TypeError:
            raise TypeError("Only numeric values can be subtracted from Dual")
        a=self.real
        b=self.dual
        c=other.real
        d=other.dual
        return Dual(a-c,b-d) 

    def __rsub__(self, other: "int | float | Dual"):
        """Performs reverse subtraction of Duals

        This method is implemented when the binary operator (-) is used after a numeric value and before a Dual
        
        Args:
            other (int | float | Dual): the other object the Dual is being subtracted from
                
        Returns:
            Dual: the difference of the Dual and other argument
        """
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
        """Performs the negation function on a Dual

        This method is implemented when the unary operator (-) is used on a Dual

        Returns:
            Dual: The negation of the Dual
        """
        return Dual(-self.real, -self.dual) 

    def __mul__(self, other: "int | float | Dual"):
        """Performs multiplication on Duals

        This method is implemented when the binary operator (*) is used after a Dual

        Args:
            other (int | float | Dual): the other object being multiplied to the Dual

        Returns:
            Dual: the product of the Dual and the other argument
        """
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
        """Performs reverse multiplication on Duals
        
        This method is implemented when the binary operator (*) is used after a numeric value and before a Dual

        Args:
            other (int | float | Dual): the other object being multiplied to the Dual

        Returns:
            Dual: the product of the Dual and the other argument
        """
        return self*other

    def __truediv__(self, other: "int | float | Dual"):
        """Performs division on Duals

        This method is implemented when the binary operation (/) is used after a Dual

        Args:
            other (int | float | Dual): the divisor of the operation

        Returns:
            Dual: the quotient of the Dual and the other argument
        """
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

    def __rtruediv__(self, other: "int | float | Dual"):
        """Performs reverse division on Duals

        This method is implemented when the binary operator (/) is used after a numeric value and before a Dual

        Args:
            other (int | float | Dual): the dividend of the operation

        Returns:
            Dual: the quotient of the other argument and the Dual 
        """
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

    def __pow__(self, other: "int | float |Dual"):
        """Performs powers of Duals

        This method is implemented with the binary operator (**) is used after a Dual

        Args:
            other (int | float | Dual): the exponent

        Returns:
            Dual: the result of the powers
        """
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

    def __rpow__(self, other: "int | float | Dual"):
        """Performs reverse power of Duals

        This method is implemented with the binary operator (**) is used after a Dual

        Args:
            other (int | float | Dual): the base

        Returns:
            Dual: the result of the powers
        """
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
        """Performs NumPy trigonometric functions on Duals

        This method is implemented when the NumPy ufuncs (np.sin | np.cos |np.tan) are used on a Dual

        Returns:
            Dual: the result of the trigonometric fuction
        """
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
