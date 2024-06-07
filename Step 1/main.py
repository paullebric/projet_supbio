#alicia et alice les grosses nulles elles verront jamais ce message
from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt
k = 0.001
activation_treshold=90
feedback_treshold = 20
@dataclass
class ProteinY :
    quantity : float = 0
    name : str = "Protein Y"
    state :bool = True
    def update(self,Cytoplasm):
        if Cytoplasm["Enzyme A"].quantity < feedback_treshold :
            self.quantity +=1 #basal rate changeable
        elif self.quantity > 0 :
            self.quantity /=2
        if Cytoplasm["Substrate A"].quantity<activation_treshold:
            self.state =True
        else :
            self.state =False
@dataclass
class EnzymeA :
    quantity : float = 0
    name : str = "Enzyme A"
    def update(self,Cytoplasm):
        if Cytoplasm["Protein Y"].state ==True :
            print('la')
            self.quantity+=0.1*Cytoplasm["Protein Y"].quantity #ici pour chaque 10 promoteur (prot y) une enz A est creer encore une fois on peut changer cette valeur
        else :
            self.quantity-=0.05*Cytoplasm["Protein Y"].quantity
@dataclass
class SubstrateA :
    quantity : float = 0
    name : str = "Substrate A"
    def update(self,data):
        self.quantity+=0.1
        print("self.quantity",self.quantity)
@dataclass
class ProductB :
    quantity : float = 0
    name : str = "Product B"
    def update(self,Cytoplasm):
        Rate = k* Cytoplasm["Enzyme A"].quantity* Cytoplasm["Substrate A"].quantity
        print("rate",Rate)
        Cytoplasm["Substrate A"].quantity /= Rate #ici je considère que 1 substrat A donne 1 produit B on pourra changer plus tard
        self.quantity *= Rate

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
            print(self.Cytoplasm)
            for protein in self.Cytoplasm.values():
                data[protein.name].append(protein.quantity)
            for protein in self.Cytoplasm.values():
                protein.update(self.Cytoplasm)

        df = pd.DataFrame(data)
        df.plot()
        plt.show()


circuit = Circuit()
circuit.add("Enzyme A", EnzymeA(quantity=10))
circuit.add("Protein Y", ProteinY(quantity=10))
circuit.add("Substrate A", SubstrateA(quantity=100))
circuit.add("Product B", ProductB(quantity=0))
circuit.simulate(steps=100)