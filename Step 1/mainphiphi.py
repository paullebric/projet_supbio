
from dataclasses import dataclass
import pandas as pd
from typing import List
import matplotlib.pyplot as plt
import matplotlib.animation as ani

activation_treshold=40
feedback_treshold = 20
inhibition_threshold = 1
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
        self.pB.quantity += delta/30 #we consider that 10 sA == 1 pB
        self.subA.quantity -= delta

        if self.subA.quantity > inhibition_threshold: #activation threshold not used to avoid a weird middle part
                self.pY.state = True
        elif self.subA.quantity < inhibition_threshold:
                self.pY.state = False

        if self.eA.quantity > feedback_treshold: 
            self.pY.state = False
        else:
            self.pY.state = True
        
        if self.pY.state == True: #the state of eA is always the same as pY
            self.eA.state = True
        else:
            self.eA.state = False

        if self.pY.state ==True:
            self.pY.quantity +=self.eA.quantity/10
        else:
            self.pY.quantity -=self.eA.quantity/10
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

    def animate(self):
        fig, ax = plt.subplots()
        lines = {name: ax.plot([], [], label=name)[0] for name in self.df.columns}

        def init():
            ax.set_xlim(0, len(self.df))
            ax.set_ylim(self.df.min().min(), self.df.max().max())
            return lines.values()

        def update(frame):
            for name, line in lines.items():
                line.set_data(range(frame), self.df[name][:frame])
            return lines.values()
        animation = ani.FuncAnimation(fig, update, frames=len(self.df), init_func=init, blit=True, interval=10,repeat=False)
        ax.legend()
        plt.show()

eA = Components(name = "Enzyme A",quantity=5)
pY = Components(name = "Protein Y",quantity=5)
sA = Components(name = "Substrate A",quantity=50)
pB = Components(name = "Product B",quantity=0)

circuit = Circuit()
circuit.add(eA)
circuit.add(pY)
circuit.add(sA)
circuit.add(pB)
circuit.add_interactions(eA,pY,sA,pB,0.05)
circuit.simulate(steps=500)
# circuit.animate()