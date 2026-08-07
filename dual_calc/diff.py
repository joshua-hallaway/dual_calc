import dual as d
import numpy as np

class Poly:
    def __init__(self, coef: np.ndarray | list | int | float | d.Dual, deg: np.ndarray | list | int | float): 
        if isinstance(coef, (int,float,d.Dual)):
            coef=[coef]
            coef=np.array(coef, dtype=object)
        else:
            if not all(isinstance(i, (int,float,d.Dual)) for i in coef):
                raise TypeError("elements of coef must be numeric")
            coef=np.array(coef, dtype=object)
        if isinstance(deg, (int, float)):
            deg=[deg]
            deg=np.array(deg, dtype=object)
        else:
            if not all(isinstance(i, (int,float)) for i in deg):
                raise TypeError("elements of deg must be real numbers")
            deg=np.array(deg, dtype=object)
        if not isinstance(coef,np.ndarray) or not isinstance(deg,np.ndarray):
            raise TypeError("coef and deg must be numeric or lists and arrays of numerics")
        self._coef=coef
        self._deg=deg

    def __call__(self,x: int | float | d.Dual):
        return np.sum(self._coef*(x**self._deg))