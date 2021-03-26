import sympy as sym
from sympy.core.expr import Expr

def tupleConv(l):
    return tuple(map(tupleConv, l)) if isinstance(l, (list, tuple)) else l

class WE3j(Expr):
    def __new__(cls, c1, c2, c3):
        for coef in [c1,c2,c3]:
            coef
        c1 = sym.sympify(tupleConv(c1))
        c2 = sym.sympify(tupleConv(c2))
        c3 = sym.sympify(tupleConv(c3))

        obj = Expr.__new__(cls, c1, c2, c3)
        return obj


class WE6j(Expr):
    def __new__(cls, c1, c2, c3, c4, c5, c6):
        for coef in [c1,c2,c3]:
            coef
        c1 = sym.sympify(tupleConv(c1))
        c2 = sym.sympify(tupleConv(c2))
        c3 = sym.sympify(tupleConv(c3))
        c4 = sym.sympify(tupleConv(c4))
        c5 = sym.sympify(tupleConv(c5))
        c6 = sym.sympify(tupleConv(c6))

        obj = Expr.__new__(cls, c1, c2, c3, c4, c5, c6)
        return obj
