from dataclasses import dataclass
from typing import List
import pandas as pd
import matplotlib.pyplot as plt

@dataclass
class Component:
    name: str
    quantity: float 
    def update(self):
        pass

@dataclass
class Substrate_A(Component):
    quantity: float
    name: str = "Substrate_A"
    def update(self):
        pass

@dataclass
class Product_B(Component):
    production_rate:0.8
    quantity: 0
    name: str = "Product_B"
    def update(self, reaction_rate:float):
        self.quantity+= reaction_rate*self.production_rate

@dataclass
class Enzyme_A(Component):
    quantity: float
    rate:float
    name: str = "Enzyme_A"
    def update(self, Protein_Y_active: bool, product: Product_B):
        if Protein_Y_active:
            self.concentration += self.rate
        self.concentration -= self.concentration * self.rate
        self.concentration = max(self.concentration, product.concentration)

@dataclass
class Protein_Y(Component):
    quantity: float
    rate: float
    active: bool = False
    name: str = "Transcription Factor"
    name: str = "Protein_Y"

    def update(self, substrate: Substrate_A, enzyme: Enzyme_A, feedback_threshold: float):
        if substrate.concentration > self.activation_threshold:
            self.active = True
        elif substrate.concentration < self.inhibition_threshold or enzyme.concentration > feedback_threshold:
            self.active = False

@dataclass
class Interaction:
    Substrate_A: Substrate_A
    Product_B: Product_B
    Enzyme_A: Enzyme_A
    Protein_Y: Protein_Y
    rate: float
    delta: float = 0
    
    def update(self, activation_threshold=5, inhibition_threshold=20, feedback_threshold=15):
        if self.Substrate_A.quantity > activation_threshold:
            self.Enzyme_A.quantity += 1
            self.Protein_Y.state = True
        if self.Substrate_A.quantity > inhibition_threshold:
            self.Enzyme_A.quantity -= 1
            self.Protein_Y.state = False
            
        if self.Enzyme_A.quantity > feedback_threshold:
            self.Protein_Y.state = False
            
        self.delta = self.rate * self.Substrate_A.quantity * self.Enzyme_A.quantity
        self.Substrate_A.quantity -= self.delta
        self.Product_B.quantity += self.delta
        
        if self.Protein_Y.state:
            self.Enzyme_A.state = True
        else:
            self.Enzyme_A.state = False

@dataclass
class Circuit:
    components: List[Component]
    interactions: List[Interaction]
    
    def init(self, components: List[Component], interactions: List[Interaction]):
        self.Component = components
        self.Interaction = interactions
        
    def add_component(self, component: Component):
        self.Component.append(component)

    def add_interaction(self, Substrate_A, Product_B, Enzyme_A, Protein_Y, rate):
        i = Interaction(Substrate_A=Substrate_A, Product_B=Product_B, Enzyme_A=Enzyme_A, Protein_Y=Protein_Y, rate=rate)
        self.Interaction.append(i)

    def simulate(self, steps):
        data = {m.name: [] for m in self.Component}
        for k in range(steps):
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
        plt.show()

circuit = Circuit(components=[], interactions=[])
enzyme_a = Enzyme_A(quantity=19)
protein_y = Protein_Y(quantity=40)
substrate_a = Substrate_A(quantity=10)
product_b = Product_B()

circuit.add_component(enzyme_a)
circuit.add_component(protein_y)
circuit.add_component(substrate_a)
circuit.add_component(product_b)
circuit.add_interaction(substrate_a, product_b, enzyme_a, protein_y, rate=0.1)
circuit.plot(30)