from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt

rate = {"rate":0
}
@dataclass
class Metabolite :
    name : str
    qty : float
    def update(self):
        pass
@dataclass
class Interaction :
    METABOLITES : list[Metabolite]
    rate : dict
    def __init__(self):
        self.METABOLITES=[]
        self.rate={}
    def update(self):
        
@dataclass
class Circuit :
    METABOLITES: list[Metabolite]
    INTERACTIONS : Interaction
    def __init__(self):
        self.METABOLITES = []
    def add(self,objet):
        self.METABOLITES.append(objet)
    def add_interaction(self,rate):
        self.INTERACTIONS.append(Interaction(self.METABOLITES,rate))
    def simulate(self, steps):
        self.add(Interaction)
        data = {}
        for x in self.Cytoplasm.keys():
            data[x] = []
        for i in range(steps):
            for protein in self.Cytoplasm.values():
                data[protein.name].append(protein.quantity)
            for transfo in self.Transformations:
                transfo.update()
            for protein in self.Cytoplasm.values():
                protein.update(self.Cytoplasm)
            df = pd.DataFrame(data)
        df.plot()
        plt.show()


circuit = circuit()
circuit.simulate(steps=300)