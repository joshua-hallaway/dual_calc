import numpy as np
class Node:
    def __init__(self, value):
        self.children=[]
        self.value=value

    def preorder(self):
        print(self.value, end=' ')
        for i in self.children:
            i.preorder()

class Variable(Node):
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be str")
        super().__init__(name)


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
        super().__init__(name)
        self.children=children

class Constant(Node):
    def __init__(self, value):
        if not isinstance(value, (int,float, np.number)):
            raise TypeError("value must be numeric")
        super().__init__(value)