
from dataclasses import dataclass
import pandas as pd
from typing import List
import matplotlib.pyplot as plt


k = 0.001
activation_treshold=40
feedback_treshold = 20
inhibition_threshold = 1
@dataclass
class ProteinY :
    quantity : float = 0
    name : str = "Protein Y"
    state :bool = False
    death_rate:float = 0.05    
    def update(self):
        # if self.state == True:
        #     self.quantity *=1.2
        # if self.state ==False:
        #     self.quantity *=0.99
        # self.quantity -= self.quantity*self.death_rate
        pass

        

@dataclass
class EnzymeA :
    quantity : float = 0
    name : str = "Enzyme A"
    state:bool = False
    def update(self):
        pass
    
        

@dataclass
class SubstrateA :
    quantity : float = 0
    name : str = "Substrate A"
    def update(self):
        pass

@dataclass
class ProductB :
    quantity : float = 0
    name : str = "Product B"
    def update(self):
        pass

@dataclass
class Interaction:
    eA: object 
    pY: object
    subA: object
    pB:object
    rate: float

    def update(self):
        delta = self.rate * self.eA.quantity * self.subA.quantity
        self.pB.quantity += delta/10
        self.subA.quantity -= delta

        if self.subA.quantity > inhibition_threshold:
                self.pY.state = True
        elif self.subA.quantity < inhibition_threshold:
                self.pY.state = False
        

        if self.pY.state == True:
            self.eA.state = True
        else:
            self.eA.state = False

        if self.pY.state ==True:
            self.pY.quantity +=self.eA.quantity/10
        else:
            self.pY.quantity -=self.eA.quantity/10
        self.eA.quantity += (self.pY.quantity-self.eA.quantity)/10
        self.subA.quantity +=0.5


@dataclass
class Circuit :
    Cytoplasm : List[object]
    Feedback : List[Interaction]

    def __init__(self):
        self.Cytoplasm = []
        self.Feedback = []

    def add(self,objet):
        self.Cytoplasm.append(objet)

    def add_interactions(self,eA,pY,subA,pB,rate):
        i = Interaction(eA,pY,subA,pB,rate)
        self.Feedback.append(i)


    def simulate(self, steps):
        #data = { x.name : [] for x in self.Cytoplasm}
        data = {}
        for x in self.Cytoplasm:
            data[x.name] = []
        for k in range(steps):
            for protein in self.Cytoplasm:
                protein.update()
            for inter in self.Feedback:
                inter.update()
            for protein in self.Cytoplasm:
                data[protein.name].append(protein.quantity)

        df = pd.DataFrame(data)  
        df.plot()
        plt.show()

eA = EnzymeA(quantity=5)
pY = ProteinY(quantity=5)
sA = SubstrateA(quantity=50)
pB =ProductB(quantity=0)

circuit = Circuit()
circuit.add(eA)
circuit.add(pY)
circuit.add(sA)
circuit.add(pB)
circuit.add_interactions(eA,pY,sA,pB,0.01)
circuit.simulate(steps=100)