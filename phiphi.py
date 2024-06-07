from dataclasses import dataclass
from typing import List
import pandas as pd
import matplotlib.pyplot as plt

@dataclass
class Component:
    name: str
    quantity: float=0
    def update(self):
        pass

@dataclass
class Substrate_A(Component):
    quantity : float = 0
    name: str = "Substrate_A"
    def update(self):
        self.quantity += 1

@dataclass
class Product_B(Component):
    quantity: float
    name: str = "Product_B"
    pass

@dataclass
class Enzyme_A(Component):
    quantity: float
    state: bool=True
    name: str = "Enzyme_A"
    rate: float=10
    def update(self):
        if self.state== True:
            self.quantity += self.quantity * self.rate
        self.rate = self.rate-0.1

@dataclass
class Protein_Y(Component):
    quantity: float
    name: str = "Protein_Y"
    rate: float=1
    state: bool=True
    pass

@dataclass
class Interaction:
    Product_B: object
    Substrate_A: object
    Enzyme_A: object
    Protein_Y: object
    rate: float= 1 
    activation_threshold=5
    inhibition_threshold=20
    feedback_threshold=15

    def update(self):
        delta = self.rate * self.Substrate_A.quantity * self.Enzyme_A.quantity
        if self.Substrate_A.quantity> self.activation_threshold:
            self.Enzyme_A.quantity += 1
            self.Protein_Y.state=True
        if self.Substrate_A.quantity > self.inhibition_threshold:
            self.Enzyme_A.quantity -= 1
            self.Protein_Y.state=False

        if self.Enzyme_A.quantity> self.feedback_threshold:
            self.Protein_Y.state= False


        self.Substrate_A.quantity -= delta
        self.Product_B.quantity += delta


        if self.Protein_Y.state== True:
            self.Enzyme_A.state=True
        else:
            self.Enzyme_A.state=False

@dataclass
class Circuit:
    components: List[Component] # = []
    interactions: List[Interaction]

   # def add(self):
    #    self.append(Interaction)

    def _init_(self,components: List[Component],interactions: List[Interaction]):
        self.component = components
        self.Interaction = interactions

    def add_component(self,name:str, component: Component):
        self.components.append(component)
        self.name=name

    def add_interaction(self, eA, pY, subA,pB):
        i=Interaction(eA, pY, subA,pB)
        self.interactions.append(i)

    def simulate(self, steps):
        data = {m.name: [] for m in self.components}
    #    for x in self.components:
     #       data[x.name] = []
        for k in range(steps):
           # for component in self.components:
            #    component.update()
            for interaction in self.interactions:
                interaction.update()
            for component in self.components:
                component.update()
                data[component.name].append(component.quantity)
        return data

    def plot(self, steps):
        data = self.simulate(steps)
        df = pd.DataFrame(data)
        df.plot()

circuit = Circuit(components=[],interactions=[])
circuit.add_component("Enzyme_A", Enzyme_A(quantity=10))
circuit.add_component("Protein_Y", Protein_Y(quantity=10))
circuit.add_component("Substrate_A", Substrate_A(quantity=100))
circuit.add_component("Product_B", Product_B(quantity=0))
circuit.add_interaction(Product_B, Substrate_A, Protein_Y, Enzyme_A)
circuit.simulate(steps=100)
circuit.plot(100)
plt.show()