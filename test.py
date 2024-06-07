# %%
from dataclasses import dataclass
from typing import List
import pandas as pd
import matplotlib.pyplot as plt

#rate à déterminer :
#treshold à déterminer :

@dataclass
class Component:
    name: str
    quantity: float=0
    def update(self):
        pass
   
@dataclass
class Substrate_A(Component):
    name: str = "Substrate_A"
    pass
       
@dataclass
class Product_B(Component):
    quantity: float
    name: str = "Product_B"
    def update(self, delta):
        self.concentration += delta

@dataclass
class Enzyme_A(Component):
    quantity: float
    state: bool=True
    name: str = "Enzyme_A"
    rate: float=0.1
    def update(self):
        if self.state:
            self.quantity += self.quantity * self.rate
        self.rate = self.rate-1
       
@dataclass
class Protein_Y(Component):
    quantity: float
    name: str = "Protein_Y"
    rate: float=0.2
    state: bool=True
    pass
   

@dataclass
class Interaction:
    Product_B: object
    Substrate_A: object
    Enzyme_A: object
    Protein_Y: object
    rate: float
    delta:float
   
    def update(self, activation_threshold=5,inhibition_threshold=20,feedback_threshold=15):
        if self.Substrate_A.quantity> activation_threshold:
            self.Enzyme_A.quantity += 1
            self.Protein_Y.state=True
        if self.Substrate_A.quantity > inhibition_threshold:
            self.Enzyme_A.quantity -= 1
            self.Protein_Y.state=False
           
        if self.Enzyme_A.quantity> feedback_threshold:
            self.Protein_Y.state= False
           
        delta = self.rate * self.Substrate_A.quantity * self.Enzyme_A.quantity
        self.Substrate_A.quantity -= delta
        self.Product_B.quantity += delta
       
        if self.Protein_Y.state:
            self.Enzyme_A.state=True
        else:
            self.Enzyme_A.state=False
       
       

@dataclass
class Circuit:
    components: List[Component] # = []
    interactions: List[Interaction]
   
   # def add(self):
    #    self.append(Interaction)

    def __init__(self,components: List[Component],interactions: List[Interaction]):
        self.Component = components
        self.Interaction = interactions
       
    def add_component(self,name:str, component: Component):
        self.Component.append(component)
        self.name=name

    def add_interaction(self, interaction: Interaction):
        self.interactions.append(interaction)

    def simulate(self, steps):
        data = {m.name: [] for m in self.Component}
    #    for x in self.components:
     #       data[x.name] = []
        for k in range(steps):
           # for component in self.components:
            #    component.update()
            for interaction in self.Interaction:
                interaction.update()
            for component in self.Component:
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
circuit.simulate(steps=100)