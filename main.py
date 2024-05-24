#alicia et alice les grosses nulles elles verront jamais ce message
from dataclasses import dataclass
import pandas as pd
active = True
inactive = False
@dataclass
class ProteinY :
    quantity : float = 0
    name : str = "Protein Y"
    state : bool = True
@dataclass
class EnzymeA :
    quantity : float = 0
    name : str = "Enzyme A"
    def update(self):
        pass
        
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
    def simulate(self, steps):
        #data = { x.name : [] for x in self.Cytoplasm}
        data = {}
        for x in self.Cytoplasm:
            data[x[1].name] = []
        for k in range(steps):
            for protein in self.Cytoplasm:
                protein[1].update()
            for protein in self.Cytoplasm:
                data[protein[1].name].append(protein[1].population)
        df = pd.DataFrame(data)
        df.plot()

        

circuit = Circuit()
circuit.add("Enzyme A", EnzymeA(quantity=10))
circuit.add("Protein Y", ProteinY(quantity=10))
circuit.add("Substrate A", SubstrateA(quantity=100))
circuit.add("Product B", ProductB(quantity=0))
circuit.simulate(steps=100)