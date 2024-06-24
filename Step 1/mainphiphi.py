
from dataclasses import dataclass
import pandas as pd
from typing import List
import matplotlib.pyplot as plt
import matplotlib.animation as ani


feedback_treshold = 20 #negative feedback
inhibition_threshold = 1 #substrate feedback
@dataclass       

#Since everything is done in the "Interaction" Class, the "Component" Class doesnt need to have updates
@dataclass 
class Components:
    quantity : float
    name: str
    state :bool = True

#Where things happens; since we know how many diff components there are we can put everything here

@dataclass  
class Interaction:
    eA: Components
    pY: Components
    subA: Components
    pB: Components
    rate: float

    def update(self):
        delta = self.rate * self.eA.quantity * self.subA.quantity    #based on the given formula
        self.pB.quantity += delta/30 #we consider that 30 sA == 1 pB or else pB grows too fast and the graph is not watchable
        self.subA.quantity -= delta

        if self.subA.quantity > inhibition_threshold: #substrate feedback implementation
                self.pY.state = True
        elif self.subA.quantity < inhibition_threshold:
                self.pY.state = False

        if self.eA.quantity > feedback_treshold: #negative feedback implementation
            self.pY.state = False
        else:
            self.pY.state = True
        
        if self.pY.state == True: #the state of eA is always the same as pY
            self.eA.state = True
        else:
            self.eA.state = False

        if self.pY.state ==True:
            self.pY.quantity +=self.eA.quantity/10#since eA catalyses pY, we add based on the qty of eA
        else:
            self.pY.quantity -=self.eA.quantity/10#pY gets reduced because it stops being synthetised and qty diminish
        self.eA.quantity += (self.pY.quantity-self.eA.quantity)/10 #it works
        self.subA.quantity +=0.5 #basal rate of substrate A 


@dataclass
class Circuit :
    Cytoplasm : List[Components]
    Feedback : List[Interaction]
    df: list

    def __init__(self):
        self.Cytoplasm = []
        self.Feedback = []
        

    def add(self,objet):
        self.Cytoplasm.append(objet)

    def add_interactions(self,eA,pY,subA,pB,rate):
        i = Interaction(eA,pY,subA,pB,rate)
        self.Feedback.append(i)


    def simulate(self, steps):
        data = {}
        for x in self.Cytoplasm:
            data[x.name] = []
        for k in range(steps):
            for inter in self.Feedback:
                inter.update()
            for protein in self.Cytoplasm:
                data[protein.name].append(protein.quantity)
            self.df = pd.DataFrame(data)
        self.df.plot()
        plt.show()

eA = Components(name = "Enzyme A",quantity=5)
pY = Components(name = "Protein Y",quantity=5)
sA = Components(name = "Substrate A",quantity=50)
pB = Components(name = "Product B",quantity=0)

circuit = Circuit()
circuit.add(eA),circuit.add(pY),circuit.add(sA),circuit.add(pB)
circuit.add_interactions(eA,pY,sA,pB,0.05)
circuit.simulate(steps=500)
