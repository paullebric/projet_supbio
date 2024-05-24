#alicia et alice les grosses nulles elles verront jamais ce message
from dataclasses import dataclass


@dataclass
class Promoter :
    quantity : float = 0
@dataclass
class ProteinY :
    quantity : float = 0
@dataclass
class EnzymeA :
    quantity : float = 0
@dataclass
class SubstrateA :
    quantity : float = 0
@dataclass
class ProductB :
    quantity : float = 0
@dataclass
class Circuit :
    Cytoplasm : list = [object]
    Feedback : list = []
    def __init__(self):
        self.Enzymes = []
        self.Feedback = []
    def add(self,x):
        self.Cytoplasm.append(x)

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