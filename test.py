from dataclasses import dataclass
from typing import List
import pandas as pd
import matplotlib.pyplot as plt

@dataclass
class SubA:
    quantity: float
    threshold: float
    name: str = "SubA"

@dataclass
class SubB:
    quantity: float
    name: str = "SubB"
    
@dataclass
class EnzA:
    quantity: float
    threshold: float
    name: str = "EnzA"

@dataclass
class Y:
    quantity: float
    threshold: float
    name: str = "Y"
    
@dataclass
class Interaction:
    SubA: object
    SubB: object
    EnzA: object
    Y: object
    rate: float
    
    def update_1(self):
        x = self.rate * self.SubA.quantity * self.EnzA.quantity
        self.SubA.quantity -= self.SubA.quantity*x
        self.SubB.quantity += self.SubA.quantity*x/2
        self.EnzA.quantity -= self.SubA.quantity*x
        self.SubA.quantity += 0.1
    
    def update_2a(self):
        if self.SubA.quantity > self.SubA.threshold:
            self.Y.quantity -= 1
        else:
            pass
    
    def update_2b(self):
        if self.Y.quantity >= self.Y.threshold:
            self.EnzA.quantity += 1
        else:
            self.EnzA.quantity -= 1
    
    def update_2c(self):
        if self.EnzA.quantity > self.EnzA.threshold:
            self.Y.quantity -= 0.9
        else:
            self.Y.quantity += 0.9
    
    
@dataclass
class Circuit:
    compo: List[object]
    interactions: List[Interaction]
    
    def __init__(self):
        self.compo = []
        self.interactions = []
    
    def add_compo(self, x):
        self.compo.append(x)
    
    def add_interaction(self, sub1, sub2, enz1, ft1, rate):
        i = Interaction(sub1, sub2, enz1, ft1, rate)
        self.interactions.append(i)
    
    def simulate(self, t):
        data = {}
        for comp in self.compo:
            data[comp.name] = []
        for k in range(t):
            for comp in self.compo:
                data[comp.name].append(comp.quantity)
            for interaction in self.interactions:
                interaction.update_1()
                interaction.update_2a()
                interaction.update_2b()
                interaction.update_2c()

        return data
    
    def plot(self, t):
        data = self.simulate(t)
        df = pd.DataFrame(data)
        df.plot()
        plt.show()

SubstrateA = SubA(quantity=40, threshold=25)
ProductB = SubB(quantity=0)
EnzymeA = EnzA(quantity=20, threshold=15)
ProteinY = Y(quantity=5, threshold=10)
c = Circuit()
c.add_compo(SubstrateA)
c.add_compo(ProductB)
c.add_compo(EnzymeA)
c.add_compo(ProteinY)
c.add_interaction(SubstrateA, ProductB, EnzymeA, ProteinY, rate=0.001)
c.plot(100)