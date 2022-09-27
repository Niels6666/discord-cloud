from typing import List
from matplotlib import pyplot as plt
import numpy as np
from parser import Constant, Multiply, VariableX, Parser, Expression


class Graph:
    plot = None
    figure = None

    def __init__(self, title, minX, maxX, minY, maxY) -> None:
        fig, ax = plt.subplots()
        ax.set_title(title)
        ax.set_xlim(minX, maxX)
        ax.set_ylim(minY, maxY)
        self.plot = ax
        self.figure = fig

    def resize(self, minX, maxX, minY, maxY):
        self.plot.set_xlim(minX, maxX)
        self.plot.set_ylim(minY, maxY)

    def draw(self):
        x1, x2 = self.plot.get_xlim()
        y2, y1 = self.plot.get_ylim()
        self.plot.axline((x1, 0), (x2, 0), color='black')
        self.plot.axline((0, y1), (0, y2), color='black')

    def clear(self):
        title = self.plot.get_title()
        xlim = self.plot.get_xlim()
        ylim = self.plot.get_ylim()
        self.plot.clear()
        self.plot.set_title(title)
        self.plot.set_xlim(xlim)
        self.plot.set_ylim(ylim)



class Element:
    def draw(self, graph: Graph):
        pass


class Function(Element):
    name: str = ""
    expr: Expression = None

    def __init__(self, name:str, expr: Expression) -> None:
        self.name = name
        self.expr = expr

    def draw(self, graph: Graph):
        reellist = []
        imlist = []
        minX, maxX = graph.plot.get_xlim()
        xlist = np.linspace(minX, maxX, 500)
        for x in xlist:
            z = complex(x, 0)
            res = self.expr.evaluate(z)
            reellist.append(res.real)
            imlist.append(res.imag)

        graph.plot.plot(xlist, reellist, "blue", label=self.name+"(x) réelle")
        graph.plot.plot(xlist, imlist, "orange",
                        label=self.name+"(x) imaginaire")
        graph.plot.legend()


class Graphics:
    graph: Graph = None
    elements: List[Element] = []

    def __init__(self):
        self.graph = Graph("plot", -1.0, 1.0, -1.0, 1.0)

    def resize(self, minX, maxX, minY, maxY):
        self.graph.resize(minX, maxX, minY, maxY)

    def title(self, title):
        self.graph.plot.set_title(label=title, loc='center')

    def function(self, name:str, expr:Expression):
        self.elements.append(Function(name, expr))

    def point(self):
        pass

    def visualize(self):
        self.graph.clear()
        self.graph.draw()
        for e in self.elements:
            e.draw(self.graph)

        plt.savefig("bot/temp/plot.png", format="png")
    
    def clear(self):
        self.graph.clear()
        self.resize( -1.0, 1.0, -1.0, 1.0)
        self.title("plot")
        self.elements.clear()