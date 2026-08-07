# Create the Dual class
class Dual:
    """A number with both a real and hypercomplex component of the form a+bϵ.

    This class allows for the creation of dual numbers as well as aritmatic between dual numbers and other dual numbers, integers, or floating point values

    Attributes:
        real (int | float): the real portion of the dual number
        dual (int | float): the hypercomplex portion of the dual number
    """
    # Initializes a Dual object with a real and hypercomplex part
    def __init__(self, real: int | float, dual: int | float):
        """Initializes a dual number with a real and hypercomplex part

        This method is implimented when a Dual object is initiated

        Args:
            real (int | float): the real portion of the dual number
            dual (int | float): the hypercomplex portion of the dual number
        """
        # checks if both arguments are numeric
        if not isinstance(real, (int, float)) or not isinstance(dual, (int, float)): 
            raise TypeError("All argument must be numeric")
        # assigns input values
        self.real=real
        self.dual=dual

    # Method for turning int and float to dual
    @staticmethod
    def to_dual(other: int | float):
        """Converts int and float values to Dual objects

        Arges:
            other (int | float): the object to be converted to a Dual
        
        Returns:
            Dual: the Dual version of the int of float value
        """
        # if already Dual pass straight through
        if isinstance(other, Dual): 
            return other
        # if int or float set real portion to input value and hypercomplex portion to 0
        elif isinstance(other, (int, float)): 
            return Dual(real=other, dual=0)
        # throws error if non numeric or Dual value
        else: 
            raise TypeError("Only numeric values can be converted to Dual")

    # report magic method
    def __repr__(self):
        """Returns a string representation of the Dual number

        This method is implimented when the repr, print, or str function is used on a Dual

        Returns:
            str: the dual number formatted as "Dual(real={real}, dual={dual})"
        """
        return f"Dual(real={self.real}, dual={self.dual})"

    # equality magic method
    def __eq__(self, other: "int | float | Dual"):
        """Determines if the Dual is equal to an different Dual, int, or float

        This method is implimented when the binary operator (=) is used after a Dual

        Args:
            other (int | float | Dual): the other object being compaired to the Dual

        Returns:
            bool: The truth value of the equality
        
        """
        # returns False if input is not numeric or Dual
        try: 
            other = Dual.to_dual(other)
        except TypeError:
            return False
        # check both real and hypercomplex part for equality while accounting for floating point error
        return (abs(self.real - other.real) < 1e-12 and abs(self.dual - other.dual) < 1e-12) 

    # addition magic method
    def __add__(self, other: "int | float | Dual"):
        """Performs addition on Duals

        This method is implimented with the binary operator (+) is used after a Dual

        Args:
            other (int | float | Dual): the other object being added to the Dual
        
        Returns:
            Dual: thus sum of the Dual and other argument
        """
        # throws error if input is not numeric or Dual
        try: 
             other=Dual.to_dual(other)
        except TypeError:
            raise TypeError("Only numeric values can be added to Dual")
        # performs the addition
        return Dual(self.real+other.real, self.dual+other.dual) 

    # reverse addition magic method
    def __radd__(self, other: "int | float | Dual"):
        """Performs reverse addition on Duals

        This method is implimented when the binary operator (+) is used after a numeric value and before a Dual

        Args:
            other (int | float | Dual): the other object being added to the Dual
        
        Returns:
            Dual: thus sum of the Dual and other argument
        """
        # throws error if input is not numeric or Dual
        try: 
             other=Dual.to_dual(other)
        except TypeError:
            raise TypeError("Only numeric values can be added to Dual")
        # performs addition
        return Dual(self.real+other.real, self.dual+other.dual) 

    # subtraction magic method
    def __sub__(self,other: "int | float | Dual"):
        """Performs subtraction of Duals

        This method is implimented when the binary operator (-) is used after a Dual

        Args:
            other (int | float | Dual): the other object being subtracted from the Dual
        
        Returns:
            Dual: thus difference of the Dual and other argument
        """
        # throws error if input is not numeric or Dual
        try: 
             other=Dual.to_dual(other)
        except TypeError:
            raise TypeError("Only numeric values can be subtracted from Dual")
        # perform subtraction
        return Dual(self.real-other.real, self.dual-other.dual) 

    # reverse subtraction magic method
    def __rsub__(self,other: "int | float | Dual"):
        """Performs reverse subtraction of Duals

        This method is implimented when the binary operator (-) is used after a numeric value and before a Dual
        
        Args:
            other (int | float | Dual): the other object the Dual is being subtracted from
                
        Returns:
            Dual: thus difference of the Dual and other argument
        """
        # throws error if input is not numeric or Dual
        try: 
             other=Dual.to_dual(other)
        except TypeError:
            raise TypeError("Dual can only be subtracted from numeric values")
        # perform subtraction
        return Dual(other.real-self.real, other.dual-self.dual) 

    # negation magic method
    def __neg__(self):
        """Performs the negation function on a Dual

        This method is implimented when the unary operator (-) is used on a Dual

        Returns:
            Dual: The negation of the Doul
        """
        # flips sign of real and hypercomplex portion
        return Dual(-self.real, -self.dual) 

    # multiplication magic method
    def __mul__(self, other: "int | float | Dual"):
        """Performs multiplication on Duals

        This method is implimented when the binary operator (*) is used after a Dual

        Args:
            other (int | float | Dual): the other object being multiplied to the Dual

        Returns:
            Dual: the product of the Dual and the other argument
        """
        # throws error if input is not numeric or Dual
        try: 
             other=Dual.to_dual(other)
        except TypeError:
            raise TypeError("Only numeric values can be multiplied with Dual")
        # performs multiplication
        return Dual(self.real*other.real, self.dual*other.real+self.real*other.dual) 

    # reverse multiplication magic method
    def __rmul__(self, other: "int | float | Dual"):
        """Performs reverse multiplication on Duals
        
        This method is implimented when the binary operator (*) is used after a numeric value and before a Dual

        Args:
            other (int | float | Dual): the other object being multiplied to the Dual

        Returns:
            Dual: the product of the Dual and the other argument
        """
        # throws error if input is not numeric or Dual
        try: 
             other=Dual.to_dual(other)
        except TypeError:
            raise TypeError("Only numeric values can be multiplied with Dual")
        # performs multiplication
        return Dual(self.real*other.real, self.dual*other.real+self.real*other.dual) 

    # division magic method
    def __truediv__(self, other: "int | float | Dual"):
        """Performs division on Duals

        This method is implimented when the binary operation (/) is used after a Dual

        Args:
            other (int | float | Dual): the divisor of the operation

        Returns:
            Dual: the quotient of the Dual and other argument
        """
        # throws error if input is not numeric or Dual
        try: 
             other=Dual.to_dual(other)
        except TypeError:
            raise TypeError("Only numeric values can be divided with Dual")
        # throws error if division by zero
        if other.real==0: 
            raise ZeroDivisionError("Division by zero")
        # performs division
        return Dual(self.real/other.real, (self.dual*other.real-self.real*other.dual)/(other.real**2)) 

    # reverse division magic method
    def __rtruediv__(self, other: "int | float | Dual"):
        """Performs reverse division on Duals

        This method is implimented when the binary operator (/) is used after a numeric value and before a Dual

        Args:
            other (int | float | Dual): the dividend of the operation

        Returns:
            Dual: the quotient of the other argument and the Dual 
        """
        # throws error if input is not numeric or Dual
        try: 
             other=Dual.to_dual(other)
        except TypeError:
            raise TypeError("Only numeric values can be divided with Dual")
        # throws error if division by zero
        if self.real==0: 
            raise ZeroDivisionError("Division by zero")
        # performs division
        return Dual(other.real/self.real, (other.dual*self.real-other.real*self.dual)/(self.real**2)) 

    # power magic method
    def __pow__(self, other: "int | float | Dual"):
        """Performs exponentiation on Duals

        This method is implimented with the binary operator (**) is used after a Dual

        Args:
            other (int | float): the exponent

        Returns:
            Dual: the result of the exponentiation
        """
        # throws error if power is hypercomplex or not numeric
        if not isinstance(other, (int, float)): 
            raise TypeError("Exponent must be a real numeric value")
        # throws error if division by zero
        elif self.real==0 and other<=0: 
            raise ZeroDivisionError("Zero cannot be raised to a negative power")
        # performs power operation
        return Dual(self.real**other, other*self.real**(other-1)*self.dual) 

    # reverse power magic method
    def __rpow__(self, other: "int | float | Dual"):
        """Performs exponentiation of Duals
        
        This method is implimented when the binary operator (**) is used after a numeric value and before a Dual
        
        Args:
            other (int | float | Dual): the value being raised to the Dual power
        """
        # throws error for all inputs for hypercomplex power
        raise TypeError("Cannot have hypercomplex exponents") 

# only runs tests if file is ran directly
if __name__ == "__main__": 
    passed=0
    # define passed test
    def pass_test():
        global passed
        passed+=1
        print("\033[32mPass\033[0m")
        print()

    # define failed test
    def fail_test():
        print("\033[31mFail\033[0m")
        print()

    print("Running Tests on Dual class")
    
    # test init magic method
    print("Dual Test")
    try:
        # test all valid constructions
        for i in (1,1.1,0,-1): 
            for j in (1,1.1,0,-1):
                x=Dual(i,j)
                assert isinstance(x,Dual)
                assert x.real==i
                assert x.dual==j
        # tests invalid constructions
        for i in (1,1.1,0,-1): 
            for j in ("test", None, (1,2,3)):    
                try:
                    x=Dual(j,i)
                    assert False # fails test if no error or wrong error is thrown
                except TypeError:
                    pass
                try:
                    x=Dual(i,j)
                    assert False # fails test if no error or wrong error is thrown
                except TypeError:
                    pass
        for i in ("test", None, (1,2,3)):
            for j in ("test", None, (1,2,3)):
                try:
                    x=Dual(i,j)
                    assert False # fails test if no error or wrong error is thrown
                except TypeError:
                    pass
        pass_test()
    except Exception:
        fail_test()

    # test to_dual static method
    print("to_dual Test")
    try:
        # checks valid implimentations
        x=Dual.to_dual(Dual(1,1))
        assert isinstance(x,Dual)
        assert x.real==1
        assert x.dual==1
        for i in (1,1.1,0,-1):
            x=Dual.to_dual(i)
            assert isinstance(x,Dual)
            assert x.real==i
            assert x.dual==0
        # checks invalid implimentaions
        for i in ("test", None, (1,2,3)):
            try:
                x=Dual.to_dual(i)
                assert False # fails test if no error or wrong error is thrown
            except TypeError:
                pass
        pass_test()
    # fails if any unexpected errors are thrown
    except Exception:
        fail_test()

    # test repr magic method
    print("repr Test")
    x=Dual(1,1)
    try:
        # checks string output
        assert repr(x)=="Dual(real=1, dual=1)"
        pass_test()
    # fails if any unexpected errors are thrown
    except Exception:
        fail_test()

    # test eq magic method
    print("Equal test")
    x=Dual(1,1)
    y=Dual(1,1)
    z=Dual(2,2)
    try:
        # tests standard equal values
        assert x==y
        assert isinstance(x==y,bool)
        assert x!=z
        assert isinstance(x!=z,bool)
        assert x!=1
        assert x!=1.1
        assert x!="test"
        pass_test()
    # fails if any unexpected errors are thrown
    except Exception:
        fail_test()

    # test add and radd magic method
    print("Addition Test")
    x=Dual(1,1)
    y=Dual(1,1)
    try:
        # tests standard addition
        assert x+y==Dual(2,2)
        assert x+1==Dual(2,1)
        assert 1+x==Dual(2,1)
        assert x+1.1==Dual(2.1,1)
        assert 1.1+x==Dual(2.1,1)
        pass_test()
    # fails if any unexpected errors are thrown
    except Exception:
        fail_test()

    # test sub and rsub magic method
    print("Subtraction Test")
    x=Dual(2,2)
    y=Dual(1,1)
    try:
        #tests standard subtractions
        assert x-y==Dual(1,1)
        assert x-1==Dual(1,2)
        assert 1-x==Dual(-1,-2)
        assert x-1.1==Dual(0.9,2)
        assert 1.1-x==Dual(-0.9,-2)
        assert -x==Dual(-2,-2)
        pass_test()
    # fails if any unexpected errors are thrown
    except Exception:
        fail_test()

    # test mul and rmul magic method
    print("Multiplication Test")
    x=Dual(1,1)
    y=Dual(2,2)
    try:
        # tests standard multiplication
        assert x*y==Dual(2,4)
        assert x*2==Dual(2,2)
        assert 2*x==Dual(2,2)
        assert x*1.1==Dual(1.1,1.1)
        assert 1.1*x==Dual(1.1,1.1)
        pass_test()
    # fails if any unexpected errors are thrown
    except Exception:
        fail_test()

    # test truediv and rtruediv magic method
    print("Division Test")
    x=Dual(1,1)
    y=Dual(2,2)
    try:
        # tests standard division
        assert x/y==Dual(0.5,0)
        assert x/2==Dual(0.5,0.5)
        assert 2/x==Dual(2,-2)
        assert x/0.5==Dual(2,2)
        assert 0.5/x==Dual(0.5,-0.5)
        # tests division by zero
        try:
            x/Dual(0,1)
            assert False # fails test if no error or wrong error is thrown
        except ZeroDivisionError:
            pass
        try:
            x/0
            assert False # fails test if no error or wrong error is thrown
        except ZeroDivisionError:
            pass
        pass_test()
    # fails if any unexpected errors are thrown
    except Exception:
        fail_test()

    # test pow and rpow magic method
    print("Exponentiation Test")
    x=Dual(1,1)
    try:
        #tests standard exponent
        assert x**2==Dual(1,2)
        try:
            #tests hypercomplex power
            2**x
            assert False # fails test if no error or wrong error is thrown
        except TypeError:
            pass
        try:
            #tests division by zero
            Dual(0,0)**-1
            assert False # fails test if no error or wrong error is thrown
        except ZeroDivisionError:
            pass
        pass_test()
    # fails if any unexpected errors are thrown
    except Exception:
        fail_test()

    # opens help only if all 9 tests pass
    if passed==9:
        help(Dual)