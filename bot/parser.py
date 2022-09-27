import enum
import math
import cmath
import sys
from typing import Dict, List, Tuple

class System(enum.Enum):
    CARTESIAN = 0
    POLAR = 1
    NONE = 2


class Function:
    f = None

    def __init__(self, f) -> None:
        self.f = f

    def apply(self, args):
        return self.f(args)


class Format:
    def __init__(self) -> None:
        pass

    def apply(self, v: float, decimals: int = 6) -> str:
        if (v == math.pi):
            return "\\pi"
        elif (v == 1.61803398875):
            return "\\phi"
        elif (v == math.e):
            return "e"
        elif (math.isinf(v)):
            res = ""
            if v > 0:
                res = "+"
            else:
                res = "-"
            return res.__add__("\\infty")
        elif (v == round(v)):
            return str(round(v))

        s = ""
        if(decimals > 0):
            s = str(round(v, -decimals))
        else:
            s = str(v)
        return s


class Expression:
    def evaluatef(self, x: float) -> float:
        pass

    def evaluate(self, z: complex) -> complex:
        pass

    def toLaTeX(self) -> str:
        pass

    def isTailExpression(self) -> bool:
        return False


class BinaryOperator(Expression):
    left: Expression = None
    right: Expression = None

    def __init__(self, left: Expression, right: Expression) -> None:
        super().__init__()
        self.left = left
        self.right = right

    def evaluatef(self, x: float) -> float:
        a = self.left.evaluatef(x)
        b = self.right.evaluatef(x)
        return self.applyf(a, b)

    def evaluate(self, z: complex) -> complex:
        a = complex(self.left.evaluate(z))
        b = complex(self.right.evaluate(z))
        return self.apply(a, b)

    def applyf(self, a: float, b: float) -> float:
        pass

    def apply(self, a: complex, b: complex) -> complex:
        pass


class Constant(Expression):

    def __init__(self, value: float) -> None:
        self.__init__(complex(value, 0.0))

    def __init__(self, value: complex) -> None:
        super().__init__()
        self.value = value

    def isTailExpression(self) -> bool:
        return True

    def evaluatef(self, x: float) -> float:
        return self.value.real

    def evaluate(self, z: complex) -> complex:
        return self.value

    def setValue(self, value: complex):
        self.value = value

    def toLaTeX(self) -> str:
        s = ""
        format = Format()

        if (self.value.real != 0.0):
            s += format.apply(self.value.real)
        if (self.value.imag != 0.0):
            s += format.apply(self.value.imag) + "i"
        if (self.value.real == 0.0 and self.value.imag == 0.0):
            s = "0"
        return s


class Divide(BinaryOperator):

    def __init__(self, left: Expression, right: Expression) -> None:
        super().__init__(left, right)

    def applyf(self, a: float, b: float) -> float:
        return a / b

    def apply(self, a: complex, b: complex) -> complex:
        return a.__truediv__(b)

    def toLaTeX(self) -> str:
        return "\\frac{" + self.left.toLaTeX() + "}{" + self.right.toLaTeX() + "}"

    # public Expression getNumerator() {
    #     return right
    # }

    # public Expression getDenominator() {
    #     return left
    # }


class FunctionOperator(Expression):
    @staticmethod
    def sign(x):
        return x and (1, -1)[x < 0]

    class Type(enum.Enum):
        class F():
            nargs = 0
            name = ""
            def __init__(self, nargs: int, name: str) -> None:
                self.nargs = nargs
                self.name = name

        COS = F(1, "cos")
        SIN = F(1, "sin")
        TAN = F(1, "tan")
        ACOS = F(1, "acos")
        ASIN = F(1, "asin")
        ATAN = F(1, "atan")
        ACOSH = F(1, "acosh")
        ASINH = F(1, "asinh")
        ATANH = F(1, "atanh")
        SQRT = F(1, "sqrt")
        CBRT = F(1, "cbrt")
        NTHRT = F(2, "nthrt")
        ABS = F(1, "abs")
        COSH = F(1, "cosh")
        SINH = F(1, "sinh")
        TANH = F(1, "tanh")
        LN = F(1, "ln")
        LOG = F(1, "log")
        EXP = F(1, "exp")
        SIGN = F(1, "sign")
        MOD = F(2, "mod")
        POW = F(2, "pow")
        MAX = F(2, "max")
        MIN = F(2, "min")
        BASE = F(2, "base")

    class TypeForReals(enum.Enum):

        COS = Function(lambda args: math.cos(args[0]))
        SIN = Function(lambda args: math.sin(args[0]))
        TAN = Function(lambda args: math.tan(args[0]))
        ACOS = Function(lambda args: math.acos(args[0]))
        ASIN = Function(lambda args: math.asin(args[0]))
        ATAN = Function(lambda args: math.atan(args[0]))
        ACOSH = Function(lambda args: math.acosh(args[0]))
        ASINH = Function(lambda args: math.asinh(args[0]))
        ATANH = Function(lambda args: math.atanh(args[0]))
        SQRT = Function(lambda args: math.sqrt(args[0]))
        CBRT = Function(lambda args: math.pow(float(args[0]), 1/3))
        NTHRT = Function(lambda args: math.pow(args[0], 1.0 / args[1]))
        ABS = Function(lambda args: abs(args[0]))
        COSH = Function(lambda args: math.cosh(args[0]))
        SINH = Function(lambda args: math.sinh(args[0]))
        TANH = Function(lambda args: math.tanh(args[0]))
        LN = Function(lambda args: math.log(args[0]))
        LOG = Function(lambda args: math.log(args[0]))
        EXP = Function(lambda args: math.exp(args[0]))
        SIGN = Function(lambda args: FunctionOperator.sign(args[0]))
        MOD = Function(lambda args: math.fmod(args[0], args[1]))
        POW = Function(lambda args: math.pow(args[0], args[1]))
        MAX = Function(lambda args: max(args[0], args[1]))
        MIN = Function(lambda args: min(args[0], args[1]))
        BASE = Function(
            lambda args: math.log(args[1]) / math.log(args[0]))

    class TypeForComplex(enum.Enum):

        COS = Function(lambda args: cmath.cos(args[0]))
        SIN = Function(lambda args: cmath.sin(args[0]))
        TAN = Function(lambda args: cmath.tan(args[0]))
        ACOS = Function(lambda args: cmath.acos(args[0]))
        ASIN = Function(lambda args: cmath.asin(args[0]))
        ATAN = Function(lambda args: cmath.atan(args[0]))
        ACOSH = Function(lambda args: cmath.acosh(args[0]))
        ASINH = Function(lambda args: cmath.asinh(args[0]))
        ATANH = Function(lambda args: cmath.atanh(args[0]))
        SQRT = Function(lambda args: cmath.sqrt(args[0]))
        CBRT = Function(lambda args: args[0]**complex(1.0/3.0))
        NTHRT = Function(
            lambda args: args[0]**(1.0 / args[1]))
        ABS = Function(lambda args: args[0].__abs__())
        COSH = Function(lambda args: cmath.cosh(args[0]))
        SINH = Function(lambda args: cmath.sinh(args[0]))
        TANH = Function(lambda args: cmath.tanh(args[0]))
        LN = Function(lambda args: cmath.log(args[0]))
        LOG = Function(lambda args: cmath.log(args[0]))
        EXP = Function(lambda args: cmath.exp(args[0]))
        SIGN = Function(lambda args: FunctionOperator.sign(args[0]))
        MOD = Function(lambda args: complex(
            math.fmod(args[0].real, args[1].real)))
        POW = Function(lambda args: args[0]**args[1])
        MAX = Function(lambda args: max(args[0], args[1]))
        MIN = Function(lambda args: min(args[0], args[1]))
        BASE = Function(
            lambda args: math.log(args[1]) / math.log(args[0]))

    class TypeForLatexRepresentation(enum.Enum):

        COS = Function(
            lambda exprs: "\\cos \\left(" + exprs[0].toLaTeX() + "\\right)")
        SIN = Function(
            lambda exprs: "\\sin \\left(" + exprs[0].toLaTeX() + "\\right)")
        TAN = Function(
            lambda exprs: "\\tan \\left(" + exprs[0].toLaTeX() + "\\right)")
        ACOS = Function(
            lambda exprs: "\\arccos \\left(" + exprs[0].toLaTeX() + "\\right)")
        ASIN = Function(
            lambda exprs: "\\arcsin \\left(" + exprs[0].toLaTeX() + "\\right)")
        ATAN = Function(
            lambda exprs: "\\arctan \\left(" + exprs[0].toLaTeX() + "\\right)")
        ACOSH = Function(
            lambda exprs: "\\textit{arccosh} \\left(" + exprs[0].toLaTeX() + "\\right)")
        ASINH = Function(
            lambda exprs: "\\textit{arcsinh} \\left(" + exprs[0].toLaTeX() + "\\right)")
        ATANH = Function(
            lambda exprs: "\\textit{arctanh} \\left(" + exprs[0].toLaTeX() + "\\right)")
        SQRT = Function(
            lambda exprs: "\\sqrt{" + exprs[0].toLaTeX() + "}")
        CBRT = Function(
            lambda exprs: "\\sqrt[3]{" + exprs[0].toLaTeX() + "}")
        NTHRT = Function(
            lambda exprs: "\\sqrt[" + exprs[1].toLaTeX() + "]{" + exprs[0].toLaTeX() + "}")
        ABS = Function(lambda exprs: "|" + exprs[0].toLaTeX() + "|")
        COSH = Function(
            lambda exprs: "\\cosh \\left(" + exprs[0].toLaTeX() + "\\right)")
        SINH = Function(
            lambda exprs: "\\sinh \\left(" + exprs[0].toLaTeX() + "\\right)")
        TANH = Function(
            lambda exprs: "\\tanh \\left(" + exprs[0].toLaTeX() + "\\right)")
        LN = Function(
            lambda exprs: "\\ln{ \\left(" + exprs[0].toLaTeX() + "\\right) }")
        LOG = Function(
            lambda exprs: "\\ln{ \\left(" + exprs[0].toLaTeX() + "\\right) }")
        EXP = Function(
            lambda exprs: "\\exp{ \\left(" + exprs[0].toLaTeX() + "\\right) }")
        SIGN = Function(
            lambda exprs: "\\textit{sign} \\left(" + exprs[0].toLaTeX() + "\\right)")
        MOD = Function(
            lambda exprs: "\\textit{mod} \\left(" + exprs[0].toLaTeX() + "," + exprs[1].toLaTeX() + "\\right)")
        POW = Function(
            lambda exprs: exprs[0].toLaTeX() + "^{" + exprs[1].toLaTeX() + "}")
        MAX = Function(
            lambda exprs: "\\textit{max} \\left(" + exprs[0].toLaTeX() + "," + exprs[1].toLaTeX() + "\\right)")
        MIN = Function(
            lambda exprs: "\\textit{min} \\left(" + exprs[0].toLaTeX() + "," + exprs[1].toLaTeX() + "\\right)")
        BASE = Function(
            lambda exprs: "\\textit{log}_{" + exprs[1].toLaTeX() + "} \\left(" + exprs[0].toLaTeX() + "\\right)")

    exprs: List[Expression] = []
    type: Type = None

    def __init__(self, type: Type, exprs: List[Expression]) -> None:
        super().__init__()
        self.type = type
        self.exprs = exprs

    def evaluatef(self, x: float) -> float:
        args = []
        for e in self.exprs:
            args.append(e.evaluatef(x))

        for _, t in self.TypeForReals.__members__.items():
            if(self.type.name == t.name):
                return t._value_.apply(args)

    def evaluate(self, z: complex) -> complex:
        args = []
        for e in self.exprs:
            args.append(e.evaluate(z))

        for _, t in self.TypeForComplex.__members__.items():
            if(self.type.name == t.name):
                return t._value_.apply(args)

    def toLaTeX(self) -> str:
        for _, t in self.TypeForLatexRepresentation.__members__.items():
            if(self.type.name.__eq__(t.name)):
                return t._value_.apply(self.exprs)


class Minus(BinaryOperator):
    def __init__(self, left: Expression, right: Expression) -> None:
        super().__init__(left, right)

    def applyf(self, a: float, b: float):
        return a - b

    def apply(self, a: complex, b: complex):
        return a.__sub__(b)

    def toLaTeX(self) -> str:
        return self.left.toLaTeX() + "-" + self.right.toLaTeX()


class UnaryOperator(Expression):

    right: Expression = None

    def __init__(self, right: Expression) -> None:
        super().__init__()
        self.right = right

    def evaluatef(self, x: float) -> float:
        a = self.right.evaluate(x)
        return self.applyf(a)

    def evaluate(self, z: complex) -> complex:
        a = complex(self.right.evaluate(z))
        return self.apply(a)

    def applyf(a: float) -> float:
        pass

    def apply(z: complex) -> complex:
        pass


class MinusUnary(UnaryOperator):

    def __init__(self, right: Expression) -> None:
        super().__init__(right)

    def applyf(self, a: float) -> float:
        return 0 - a

    def apply(self, z: complex) -> complex:
        return z.__neg__()

    def toLaTeX(self) -> str:
        return "{-" + self.right.toLaTeX() + "}"


class Multiply(BinaryOperator):

    def __init__(self, left: Expression, right: Expression) -> None:
        super().__init__(left, right)

    def applyf(self, a: float, b: float) -> float:
        return a * b

    def apply(self, a: complex, b: complex) -> complex:
        return a.__mul__(b)

    def toLaTeX(self) -> str:
        return self.left.toLaTeX() + "\\cdot" + self.right.toLaTeX()


class Plus(BinaryOperator):

    def __init__(self, left: Expression, right: Expression) -> None:
        super().__init__(left, right)

    def applyf(self, a: float, b: float) -> float:
        return a + b

    def apply(self, a: complex, b: complex) -> complex:
        return a.__add__(b)

    def toLaTeX(self) -> str:
        return self.left.toLaTeX() + "+" + self.right.toLaTeX()


class Power(BinaryOperator):

    def __init__(self, left: Expression, right: Expression) -> None:
        super().__init__(left, right)

    def applyf(self, a: float, b: float) -> float:
        return math.pow(a, b)

    def apply(self, a: complex, b: complex) -> complex:
        return a.__pow__(b)

    def toLaTeX(self) -> str:
        return self.left.toLaTeX() + "^{" + self.right.toLaTeX() + "}"


class Variable(Expression):
    def evaluatef(self, x: float) -> float:
        return x

    def evaluate(self, z: complex) -> complex:
        return z

    def isTailExpression(self) -> bool:
        return True


class VariableX(Variable):
    def toLaTeX(self) -> str:
        return " x"


class VariableTheta(Variable):
    def toLaTeX(self) -> str:
        return " \\theta"


class Parser:

    DEFAULTVARIABLES: Dict[str, Expression] = {"x": VariableX(),
                                               "t": VariableTheta(),
                                               "θ": VariableTheta(),
                                               "pi": Constant(math.pi),
                                               "PI": Constant(math.pi),
                                               "π": Constant(math.pi),
                                               # 1.61803398875
                                               "phi": Constant((1 + math.sqrt(5)) / 2),
                                               "e": Constant(math.e),
                                               "i": Constant(complex(0.0, 1.0)),
                                               "infinity": Constant(complex(cmath.infj)),
                                               "∞": Constant(complex(cmath.infj))}
    string = ""
    index = 0
    syst = System.CARTESIAN

    def __init__(self) -> None:
        pass

    def finishedParsing(self):
        return (self.index == self.string.__len__())

    def peekToken(self):
        return self.string.__getitem__(self.index)

    def consumeToken(self):
        res = self.string.__getitem__(self.index)
        self.index += 1
        return res

    def matchSequence(self, s: str) -> bool:
        if (self.index + s.__len__() >= self.string.__len__()):
            return False

        for i in range(s.__len__()):
            if (str.__getitem__(self.index + i) != s.__getitem__(i)):
                return False

        return True

    def consumeSequence(self, s: str):
        for i in range(s.__len__()):
            self.consumeAndCheckToken(s.__getitem__(i))

    def tokenError(self, token: str, expected: List[str]):
        s = ""

        for c in expected:
            s += "'" + c + "' "

        raise Exception("Problem while parsing string: " +
                        self.string + ", got '" + token + "' expected " + s)

    def consumeAndCheckToken(self, token: str):
        c = self.string.__getitem__(self.index)

        if (c != token):
            self.tokenError(c, token)
        self.index += 1

    def nextChar(self, c: str):
        if (self.index < self.string.__len__()):
            if (c == self.string.__getitem__(self.index)):
                self.index += 1
                return True
        return False

    def parseString(self, string: str) -> Expression:
        self.string = string.replace("E", "*10^")
        self.string = self.string.replace(" ", "")
        self.index = 0
        expr = None
        try:
            status = "success"
            expr = self.parseE()

            if (not self.finishedParsing()):
                status = "Mismatched closing bracket"
        except Exception as e:
            status = "Parsing error: " + str(e)
        return expr

    def parseE(self):
        return self.parseA()

    def parseA(self):
        expr = self.parseB()
        while (True):
            if (self.nextChar('+')):
                expr = Plus(expr, self.parseB())
            elif (self.nextChar('-')):
                expr = Minus(expr, self.parseB())
            else:
                return expr

    def parseB(self):
        expr = self.parseC()
        while (True):
            if (self.nextChar('*')):
                expr = Multiply(expr, self.parseC())
            elif (self.nextChar('/')):
                expr = Divide(expr, self.parseC())
            else:
                return expr

    def parseC(self):
        expr = self.parseD()
        while (self.nextChar('^')):
            expr = Power(expr, self.parseC())
        return expr

    def parseD(self):
        if (self.nextChar('-')):
            return MinusUnary(self.parseF())
        else:
            return self.parseF()

    def parseF(self):
        if (self.nextChar('(')):
            expr = self.parseE()
            if (not self.nextChar(')')):
                raise Exception("expected token: )")
            return expr

        token = self.peekToken()

        if (token.isdigit() or (token == '.' or token == ',')):
            return self.parseConstant()
        elif (token.isalpha()):
            s = self.parseWord()
            if (not self.finishedParsing()):
                token = self.peekToken()
                if (token == '('):
                    return self.parseFunction(s)

            return self.parseVariable(s)
        else:
            raise Exception("expected token: " + token)

    def parseConstant(self):
        value = 0.0
        decimalPower = -1.0
        decimalPoint = False

        while (not self.finishedParsing()):
            token = self.peekToken()

            if(token == 'p'):
                self.consumeToken()
                if (self.peekToken() == 'i'):
                    value = math.pi

            elif(token == '0'
                 or token == '1'
                 or token == '2'
                 or token == '3'
                 or token == '4'
                 or token == '5'
                 or token == '6'
                 or token == '7'
                 or token == '8'
                 or token == '9'):
                digit = int(token)
                if (decimalPoint):
                    value = value + digit * math.pow(10, decimalPower)
                    decimalPower -= 1
                else:
                    value = value * 10 + digit
            elif (token == '.' or token == ','):
                if (decimalPoint):
                    raise Exception("tow points in number")
                decimalPoint = True
            else:
                break
            self.consumeToken()

        return Constant(value)

    def parseFunction(self, name: str):
        for t in FunctionOperator.Type:
            if(t.name == name.upper()):
                exprs: List[Expression] = []
                self.consumeAndCheckToken('(')
                exprs.append(self.parseE())
                for i in range(1, t.value.nargs):
                    if(not self.nextChar(';')):
                        raise Exception(
                            "missing "+str(t.value.nargs-i)+" argument(s)")
                    exprs.append(self.parseE())
                self.consumeAndCheckToken(')')
                return FunctionOperator(t, exprs)

        return None

    def parseVariable(self, name: str):
        item = Parser.DEFAULTVARIABLES.get(name)
        if (item != None):
            # if(not self.syst.__eq__(System.CARTESIAN) and isinstance(item, VariableX)):
            #     raise Exception(
            #         "x not allowed in current system")

            # if(not self.syst.__eq__(System.POLAR) and isinstance(item, VariableTheta)):
            #     raise Exception(
            #         "theta not allowed in current system")

            # if(not self.syst.__eq__(System.NONE) and isinstance(item, Variable)):
            #     raise Exception(
            #         "x nor theta not allowed in current system")

            return item
        else:
            raise Exception("unknown variable name: " + name)

    def parseWord(self):
        s = ""
        while (not self.finishedParsing()):
            token = self.peekToken()
            if (token.isalnum()):
                s += self.consumeToken()
            else:
                break

        return s
#*************************************end of Parser**********************************#


def demo():
    p = Parser()
    while(True):
        print("type math expression : for exemple \n 7/5*asinh(tan(x-2))+pow(3;x)")
        rep = input(">>>")
        print("parsing string...")
        ex = p.parseString(rep)
        x = float(input("x = "))
        print(ex.evaluatef(x))

        if(not (input("exit ? o/n \n").lower() == "n")):
            break


# demo()
