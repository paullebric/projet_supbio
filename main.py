#alicia et alice les grosses nulles elles verront jamais ce message
from dataclasses import dataclass
import pandas as pd

@dataclass
class ProteinY :
    quantity : float = 0
    name : str = "Protein Y"
@dataclass
class EnzymeA :
    quantity : float = 0
    name : str = "Enzyme A"
@dataclass
class SubstrateA :
    quantity : float = 0
    name : str = "Substrate A"
@dataclass
class ProductB :
    quantity : float = 0
    name : str = "Product B"
@dataclass
class Circuit :
    Cytoplasm : list
    Feedback : list
    def __init__(self):
        self.Cytoplasm = []
        self.Feedback = []
    def add(self,name,objet):
        self.Cytoplasm.append([name,objet])
    def simulate(self, n):
        #data = { x.name : [] for x in self.animals}
        data = {}
        for x in self.Cytoplasm:
            data[x.name] = []
        for k in range(n):
            for animal in self.animals:
                animal.update()
            for interation in self.interactions:
                interation.update()
            for animal in self.animals:
                data[animal.name].append(animal.population)
        return data
    
    def plot(self, n):
        data = self.simulate(n)
        df = pd.DataFrame(data)
        df.plot()

circuit = Circuit()
circuit.add("Enzyme A"
, EnzymeA(quantity=10))
circuit.add("Protein Y"
, ProteinY(quantity=10))
circuit.add("Substrate A"
, SubstrateA(quantity=100))
circuit.add("Product B"
, ProductB(quantity=0))
circuit.simulate(steps=100)