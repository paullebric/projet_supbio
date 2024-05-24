#alicia et alice les grosses nulles elles verront jamais ce message
from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt
active = True
inactive = False
k = 0.0001
activation_treshold=50
@dataclass
class ProteinY :
    quantity : float = 0
    name : str = "Protein Y"
    state : bool = True
    def update(self,Cytoplasm):
        if Cytoplasm["Substrate A"].quantity > activation_treshold :
            self.quantity *=1.1 #ici l'augmentation de la prot Y est de 10% on peut changer et choisir comme on veut
@dataclass
class EnzymeA :
    quantity : float = 0
    name : str = "Enzyme A"
    def update(self,data):
        pass
        
@dataclass
class SubstrateA :
    quantity : float = 0
    name : str = "Substrate A"
    def update(self,data):
        pass
@dataclass
class ProductB :
    quantity : float = 0
    name : str = "Product B"
    def update(self,Cytoplasm):
        Rate = k* Cytoplasm["Enzyme A"].quantity * Cytoplasm["Substrate A"].quantity
        Cytoplasm["Substrate A"].quantity -=Cytoplasm["Substrate A"].quantity * Rate #ici je considère que 1 substrat A donne 1 produit B on pourra changer plus tard
        self.quantity +=Cytoplasm["Substrate A"].quantity * Rate

@dataclass
class Circuit :
    Cytoplasm : dict
    Feedback : list
    def __init__(self):
        self.Cytoplasm = {}
        self.Feedback = []
    def add(self,name,objet):
        self.Cytoplasm[name]=objet
    def simulate(self, steps):
        #data = { x.name : [] for x in self.Cytoplasm}
        data = {}
        for x in self.Cytoplasm.keys():
            data[x] = []
        for i in range(steps):
            for protein in self.Cytoplasm.values():
                protein.update(self.Cytoplasm)
            for protein in self.Cytoplasm.values():
                data[protein.name].append(protein.quantity)
        df = pd.DataFrame(data)
        df.plot()
        plt.show()


circuit = Circuit()
circuit.add("Enzyme A", EnzymeA(quantity=10))
circuit.add("Protein Y", ProteinY(quantity=10))
circuit.add("Substrate A", SubstrateA(quantity=100))
circuit.add("Product B", ProductB(quantity=0))
circuit.simulate(steps=100)