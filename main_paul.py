#alicia et alice les grosses nulles elles verront jamais ce message
from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt

k = 0.07
activation_treshold=40
feedback_treshold = 20
basal_rate=1.10 #a peut pres 1.115 pour enzyme A
@dataclass
class ProteinY :
    quantity : float = 0
    name : str = "Protein Y"
    state :bool = True
    prod_rate : float = basal_rate
    def update(self,Cytoplasm):
        if Cytoplasm["Enzyme A"].quantity < feedback_treshold :
            self.quantity *= self.prod_rate
        else :
            self.quantity -= 2#basal rate changeables
        if Cytoplasm["Substrate A"].quantity<activation_treshold:
            self.state =True
        else :
            self.state =False

@dataclass
class EnzymeA :
    quantity : float = 0
    name : str = "Enzyme A"
    prod_rate : float = 0.01
    def update(self,Cytoplasm):
        if Cytoplasm["Protein Y"].state ==True :
            self.quantity+=(Cytoplasm["Protein Y"].quantity-self.quantity)/10
        else :
            print("lala")
@dataclass
class SubstrateA :
    quantity : float = 0
    name : str = "Substrate A"
    def update(self,data):
        self.quantity += 0.7



@dataclass
class ProductB :
    quantity : float = 0
    name : str = "Product B"
    def update(self,Cytoplasm):
        # Rate = k* Cytoplasm["Enzyme A"].quantity * Cytoplasm["Substrate A"].quantity
        # Cytoplasm["Substrate A"].quantity /= Rate #ici je considère que 1 substrat A donne 1 produit B on pourra changer plus tard
        # self.quantity *= Rate
        pass
@dataclass
class Transformation:
    Substrate : object
    Product : object
    Enzyme : object
    rate: float = k
    def update(self):
        delta = self.rate * self.Substrate.quantity * self.Enzyme.quantity
        self.Substrate.quantity -= delta
        self.Product.quantity += delta/10


@dataclass
class Circuit :
    Cytoplasm : dict
    Transformations : list
    def __init__(self):
        self.Cytoplasm = {}
        self.Transformations =[]
    def add(self,name,objet):
        self.Cytoplasm[name]=objet
    def add_transformation(self):
        Substrate=self.Cytoplasm["Substrate A"]
        Product=self.Cytoplasm["Product B"]
        Enzyme = self.Cytoplasm["Enzyme A"]
        i = Transformation(Substrate=Substrate, Product=Product,Enzyme=Enzyme)
        self.Transformations.append(i)
    def simulate(self, steps):
        self.add_transformation()
        #data = { x.name : [] for x in self.Cytoplasm}
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


circuit = Circuit()
circuit.add("Enzyme A", EnzymeA(quantity=5))
circuit.add("Protein Y", ProteinY(quantity=5))
circuit.add("Substrate A", SubstrateA(quantity=50))
circuit.add("Product B", ProductB(quantity=0))
circuit.simulate(steps=100)