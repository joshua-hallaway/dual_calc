import numpy as np
import dual as d
class Node:
    def __init__(self, value):
        self.children=[]
        self.value=value

    def preorder(self):
        print(self, end=' ')
        for i in self.children:
            i.preorder()

    def __repr__(self):
        return self.value

class Variable(Node):
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be str")
        super().__init__(name)
        self.priority=10

    def __repr__(self):
        return self.value


class Operator(Node):
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
            case "sin"|"cos"|"tan":
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


class Constant(Node):
    def __init__(self, value):
        if not isinstance(value, (int,float, np.number)):
            raise TypeError("value must be numeric")
        super().__init__(value)
        self.priority=10

    def __repr__(self):
        return str(self.value)
