
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
        if self.state == True:
            self.quantity *=1.105
        if self.state ==False:
            self.quantity *=0.9
        self.quantity -= self.quantity*self.death_rate

        

@dataclass
class EnzymeA :
    quantity : float = 0
    name : str = "Enzyme A"
    state:bool = False
    def update(self):
        if self.state == True:
            self.quantity *= 1.07
        if self.state == False:
            self.quantity *=0.98
    
        

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
        rate1 = self.rate * self.eA.quantity * self.subA.quantity

        if self.eA.state == True:
            self.subA.quantity /=rate1

        rate2 = self.rate * self.eA.quantity * self.subA.quantity

        self.pB.quantity += rate2

        if self.subA.quantity > activation_treshold:
                self.pY.state = True
        elif self.subA.quantity < inhibition_threshold:
                self.pY.state = False
        
        if self.eA.quantity > feedback_treshold:
            self.pY.state = False
        else:
            self.pY.state = True

        if self.pY.state == True:
            self.eA.state = True
        else:
            self.eA.state = False


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

eA = EnzymeA(quantity=10)
pY = ProteinY(quantity=10)
sA = SubstrateA(quantity=100)
pB =ProductB(quantity=0)

circuit = Circuit()
circuit.add(eA)
circuit.add(pY)
circuit.add(sA)
circuit.add(pB)
circuit.add_interactions(eA,pY,sA,pB,0.01)
circuit.simulate(steps=100)