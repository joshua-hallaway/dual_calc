import numpy as np
from abc import abstractmethod
import re
class Node:
    """Parent class for nodes in an expression tree
    """
    def __init__(self, value):
        self.children=[]
        self.value=value

    def __repr__(self):
        return str(self.value)

    @abstractmethod
    def eval(self,values:dict):
        raise NotImplementedError

    def __eq__(self,other):
        if not isinstance(other,Node):
            return False
        if type(self) is not type(other):
            return False
        if self.value!=other.value:
            return False
        return self.children==other.children

    def __add__(self,other: "int | float | Node"):
        if isinstance(other, (int, float)):
            other=Constant(other)
        elif not isinstance(other,Node):
            return NotImplemented
        return Operator("+",[self,other])

    def __radd__(self,other: "int | float | Node"):
        if isinstance(other, (int, float)):
            other=Constant(other)
        elif not isinstance(other,Node):
            return NotImplemented
        return Operator("+",[other,self])

    def __sub__(self,other: "int | float | Node"):
        if isinstance(other, (int, float)):
            other=Constant(other)
        elif not isinstance(other,Node):
            return NotImplemented
        return Operator("-",[self,other])

    def __rsub__(self,other: "int | float | Node"):
        if isinstance(other, (int, float)):
            other=Constant(other)
        elif not isinstance(other,Node):
            return NotImplemented
        return Operator("-",[other,self])

    def __neg__(self):
        return Operator("-",[self])

    def __mul__(self,other:"int | float | Node"):
        if isinstance(other, (int, float)):
            other=Constant(other)
        elif not isinstance(other,Node):
            return NotImplemented
        return Operator("*",[self,other])

    def __rmul__(self,other:"int | float | Node"):
        if isinstance(other, (int, float)):
            other=Constant(other)
        elif not isinstance(other,Node):
            return NotImplemented
        return Operator("*",[other,self])

    def __truediv__(self,other:"int | float | Node"):
        if isinstance(other, (int, float)):
            other=Constant(other)
        elif not isinstance(other,Node):
            return NotImplemented
        return Operator("/",[self,other])

    def __rtruediv__(self,other:"int | float | Node"):
        if isinstance(other, (int, float)):
            other=Constant(other)
        elif not isinstance(other,Node):
            return NotImplemented
        return Operator("/",[other,self])

    def __pow__(self,other:"int | float | Node"):
        if isinstance(other, (int, float)):
            other=Constant(other)
        elif not isinstance(other,Node):
            return NotImplemented
        return Operator("**",[self,other])

    def __rpow__(self,other:"int | float | Node"):
        if isinstance(other, (int, float)):
            other=Constant(other)
        elif not isinstance(other,Node):
            return NotImplemented
        return Operator("**",[other,self])

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        if method!="__call__":
            return NotImplemented
        if kwargs.get("out") is not None:
            return NotImplemented
        if ufunc is np.sin:
            return Operator("sin",[self])
        if ufunc is np.cos:
            return Operator("cos",[self])
        if ufunc is np.tan:
            return Operator("tan",[self])
        if ufunc is np.log:
            return Operator("ln",[self])
        if ufunc is np.exp:
            return Operator("exp",[self])
        if ufunc is np.sqrt:
            return Operator("sqrt",[self])
        if ufunc is np.asin:
            return Operator("asin",[self])
        if ufunc is np.acos:
            return Operator("acos",[self])
        if ufunc is np.atan:
            return Operator("atan",[self])
        
class Variable(Node):
    """Represents a variable like x or y
    """
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be str")
        super().__init__(name)
        self.priority=10

    def __repr__(self):
        return self.value

    def eval(self,values:dict):
        import dual as d
        if not isinstance(values,dict):
            raise TypeError("Values must be a dictionary")
        if self.value not in values:
            raise ValueError("Variable not in dictionary")
        if not isinstance(values.get(self.value),(int,float,d.Dual)):
            raise TypeError("Values must be numeric")
        return values[self.value]


class Operator(Node):
    """Represents an operation and it operand children
    """
    def __init__(self, name, children):
        if not isinstance(name, str):
            raise TypeError("name must be str")
        match name:
            case "+"|"*"|"**"|"/":
                if len(children)!=2:
                    raise ValueError(f"{name} needs 2 children")
            case "-":
                if len(children)!=2 and len(children)!=1:
                    raise ValueError("- needs either 1 or 2 children")
            case "sin"|"cos"|"tan"|"ln"|"exp"|"sqrt"|"asin"|"acos"|"atan":
                if len(children)!=1:
                    raise ValueError(f"{name} needs only 1 children")
            case _:
                raise ValueError("Invalid operation")
        match name:
            case "+":
                self.priority=1
            case "*"|"/":
                self.priority=2
            case "**":
                self.priority=4
            case "-":
                if len(children)==1:
                    self.priority=3
                else:
                    self.priority=1
            case "sin"|"cos"|"tan"|"ln"|"exp"|"sqrt"|"asin"|"acos"|"atan":
                self.priority=5
        super().__init__(name)
        self.children=children

    def __repr__(self):
        match self.value:
            case "+"|"*":
                childstr=["",""]
                for i in [0,1]:
                    if self.children[i].priority<self.priority:
                        childstr[i]=f"({self.children[i]})"
                    else:
                        childstr[i]=f"{self.children[i]}"
                return f"{childstr[0]}{self.value}{childstr[1]}"
            case "-":
                if len(self.children)==1:
                    childstr=[""]
                    if self.children[0].priority<self.priority:
                        childstr[0]=f"-({self.children[0]})"
                    else:
                        childstr[0]=f"-{self.children[0]}"
                    return childstr[0]
                else:
                    childstr=["",""]
                    if self.children[0].priority<self.priority:
                        childstr[0]=f"({self.children[0]})"
                    else:
                        childstr[0]=f"{self.children[0]}"
                    if self.children[1].priority<=self.priority:
                        childstr[1]=f"({self.children[1]})"
                    else:
                        childstr[1]=f"{self.children[1]}"
                    return f"{childstr[0]}{self.value}{childstr[1]}"
            case "/":
                    childstr=["",""]
                    if self.children[0].priority<self.priority:
                        childstr[0]=f"({self.children[0]})"
                    else:
                        childstr[0]=f"{self.children[0]}"
                    if self.children[1].priority<=self.priority:
                        childstr[1]=f"({self.children[1]})"
                    else:
                        childstr[1]=f"{self.children[1]}"
                    return f"{childstr[0]}{self.value}{childstr[1]}"
            case "**":
                    childstr=["",""]
                    if self.children[0].priority<=self.priority:
                        childstr[0]=f"({self.children[0]})"
                    else:
                        childstr[0]=f"{self.children[0]}"
                    if self.children[1].priority<self.priority:
                        childstr[1]=f"({self.children[1]})"
                    else:
                        childstr[1]=f"{self.children[1]}"
                    return f"{childstr[0]}{self.value}{childstr[1]}"
            case "sin"|"cos"|"tan"|"ln"|"exp"|"sqrt"|"asin"|"acos"|"atan":
                return f"{self.value}({self.children[0]})"

    def eval(self,values:dict):
        children=[child.eval(values) for child in self.children]
        match self.value:
            case "+":
                return children[0]+children[1]
            case "-":
                if len(children)==1:
                    return -children[0]
                else:
                    return children[0]-children[1]
            case "*":
                return children[0]*children[1]
            case "/":
                if isinstance(children[1], (int, float)) and children[1] == 0:
                    raise ZeroDivisionError("cannot divide by zero")
                return children[0] / children[1]
            case "**":
                if isinstance(children[1], (int, float)) and isinstance(children[0], (int, float)) and children[0]==0 and children[1]<0:
                    raise ZeroDivisionError("cannot divide by zero")
                return children[0]**children[1]
            case "sin":
                return np.sin(children[0])
            case "cos":
                return np.cos(children[0])
            case "tan":
                return np.tan(children[0])
            case "ln":
                return np.log(children[0])
            case "exp":
                return np.exp(children[0])
            case "sqrt":
                return np.sqrt(children[0])
            case "asin":
                return np.asin(children[0])
            case "acos":
                return np.acos(children[0])
            case "atan":
                return np.atan(children[0])
            
class Constant(Node):
    """Represents a numerical constant
    """
    def __init__(self, value):
        if not isinstance(value, (int,float, np.number)):
            raise TypeError("value must be numeric")
        super().__init__(value)
        self.priority=10

    def __repr__(self):
        return str(self.value)

    def eval(self,values:dict):
        return self.value

def deriv(function:Operator,point:int|float|Node):
    import dual as d
    if isinstance(point,Node):
        value=function.eval({"x":d.Dual(point,Constant(1))})
    else:
        value=function.eval({"x":d.Dual(point,1)})
    if isinstance(value,d.Dual):
        return value.dual
    return 0

def tokenize(equation:str):
    pattern=r'\d+(?:\.\d*)?|\.\d+|[a-zA-Z_]\w*|\*\*|[+\-*/^()]'
    return re.findall(pattern,equation)

class Parser:
    def __init__(self, tokens: list[str]):
        self.tokens=iter(tokens)
        self.advance()

    def advance(self):
        try:
            self.current_token=next(self.tokens)
        except StopIteration:
            self.current_token=None

    def parse(self):
        if self.current_token is None:
            raise ValueError("Cannot parse empty expression")
        result=self.parse_add()

        if self.current_token is not None:
            raise ValueError("Invalid syntax")

        return result

    def parse_add(self):
        result=self.parse_mult()
        while self.current_token is not None and self.current_token in ("+","-"):
            operator=self.current_token
            self.advance()
            right=self.parse_mult()
            result=Operator(operator,[result, right])
        return result

    def parse_mult(self):
        result=self.parse_unary()
        while self.current_token is not None and self.current_token in ("*","/"):
            operator=self.current_token
            self.advance()
            right=self.parse_unary()
            result=Operator(operator,[result, right])
        return result

    def parse_unary(self):
        if self.current_token=="-":
            self.advance()
            return Operator("-",[self.parse_unary()])
        return self.parse_pow()

    def parse_pow(self):
        result=self.parse_func()
        if self.current_token is not None and self.current_token in ("**","^"):
            self.advance()
            right=self.parse_unary()
            result=Operator("**",[result, right])
        return result

    def parse_func(self):
        if self.current_token in ("sin","cos","tan","exp","sqrt","asin","acos","atan","ln"):
            function=self.current_token
            self.advance()
            if self.current_token!="(":
                raise ValueError(f"{function} need parentheses")
            self.advance()
            child=self.parse_add()
            if self.current_token!=")":
                raise ValueError("Missing)")
            self.advance()
            return Operator(function,[child])
        return self.parse_primary()

    def parse_primary(self):
        token=self.current_token
        if token is None:
            raise ValueError("Unexpected end of expression")
        if token=="(":
            self.advance()
            result=self.parse_add()
            if self.current_token!=")":
                raise ValueError("Missing )")
            self.advance()
            return result
        if token is not None and len(token)==1 and token.isalpha():
            self.advance()
            return Variable(token)
        if "." in token:
            try:
                value=float(token)
            except (ValueError, TypeError):
                raise ValueError(f"Invalid syntax: {token}")
            self.advance()
            return Constant(value)
        try:
            value=int(token)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid syntax")
        self.advance()
        return Constant(value)

