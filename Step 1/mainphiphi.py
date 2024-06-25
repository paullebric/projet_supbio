
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
    state :bool
    def update(self):
        pass

@dataclass
class SubstrateA(Components):
    basal_rate: int

    def update(self):
        self.quantity +=self.basal_rate


#Where things happens; since we know how many diff components there are we can put everything here

@dataclass  
class Interaction:
    eA: Components
    pY: Components
    subA: Components
    pB: Components
    rate: float

    def update(self):
        Production_reaction.update(self)
        Substrate_feedback.update(self)
        Negative_Feedback.update(self)
        Gene_express.update(self)
        Enzyme_Inhib.update(self)
        Enzyme_Regulation.update(self)
        # self.subA.update

@dataclass
class Production_reaction(Interaction):
    def update(self):
        delta = self.rate * self.eA.quantity * self.subA.quantity    #based on the given formula
        self.pB.quantity += delta/30 #we consider that 30 sA == 1 pB or else pB grows too fast and the graph is not watchable
        self.subA.quantity -= delta

@dataclass
class Substrate_feedback(Interaction):
    def update(self):
        if self.subA.quantity > inhibition_threshold: #substrate feedback implementation
                self.pY.state = True
        elif self.subA.quantity < inhibition_threshold:
                self.pY.state = False
            
@dataclass
class Negative_Feedback(Interaction):
    def update(self):
        if self.eA.quantity > feedback_treshold: #negative feedback implementation
            self.pY.state = False
        else:
            self.pY.state = True

@dataclass
class Gene_express(Interaction):
    def update(self):
        if self.pY.state == True: #the state of eA is always the same as pY
            self.eA.state = True
        else:
            self.eA.state = False

@dataclass
class Enzyme_Inhib(Interaction):
    def update(self):
        if self.pY.state ==True:
            self.pY.quantity +=self.eA.quantity/10#since eA catalyses pY, we add based on the qty of eA
        else:
            self.pY.quantity -=self.eA.quantity/10#pY gets reduced because it stops being synthetised and qty diminish

@dataclass
class Enzyme_Regulation(Interaction):
    def update(self):
        self.eA.quantity += (self.pY.quantity-self.eA.quantity)/10

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
            for protein in self.Cytoplasm:
                data[protein.name].append(protein.quantity)
            for inter in self.Feedback:
                inter.update()
            for protein in self.Cytoplasm:
                protein.update()
            self.df = pd.DataFrame(data)
        self.df.plot()
        plt.show()

eA = Components(name = "Enzyme A",quantity=5,state=False)
pY = Components(name = "Protein Y",quantity=5,state = False)
sA = SubstrateA(name = "Substrate A",quantity=50,basal_rate=0.5,state=False)
pB = Components(name = "Product B",quantity=0,state=False)

circuit = Circuit()
circuit.add(eA),circuit.add(pY),circuit.add(sA),circuit.add(pB) 
circuit.add_interactions(eA,pY,sA,pB,0.05)
circuit.simulate(steps=500)
