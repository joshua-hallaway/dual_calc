import numpy as np
import dual as d
from abc import abstractmethod
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
        pass

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
            case "+"|"*"|"**"|"/"|"^":
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
            case "**"|"^":
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
            case "**"|"^":
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
                if children[1]==0:
                    raise ZeroDivisionError("cannot divide by zero")
                return children[0]/children[1]
            case "**"|"^":
                if children[0]==0 and children[1]<0:
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

