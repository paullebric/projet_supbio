from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt
#constantes
k = 0.07
activation_treshold=5
basal_rate=1.10 #Of substrate A
rapport_Substrate_Product=100
basal_rate_A=10

@dataclass
class ProteinY :
    quantity : float = 0
    name : str = "Protein Y"
    state :bool = True
    prod_rate : float = basal_rate
    def update(self,Cytoplasm):
        if Cytoplasm["Substrate A"].quantity>activation_treshold: # Activation treshold change the quantity of Protein Y 
            self.quantity *= self.prod_rate
        self.quantity -= Cytoplasm["Enzyme A"].quantity/100 # The quantity of protein Y is relative to the quantity of Enzyme A

@dataclass
class EnzymeA :
    quantity : float = 0
    name : str = "Enzyme A"
    def update(self,Cytoplasm):
        #The enzyme A quantity depend of the quantity of prot Y
        if Cytoplasm["Protein Y"].state ==True :
            self.quantity+=(Cytoplasm["Protein Y"].quantity-self.quantity)/10

@dataclass
class SubstrateA :
    quantity : float = 0
    name : str = "Substrate A"
    def update(self,Cytoplasm):
        #The substrate A have a basal rate that depend on a constante (arbitrary)
        self.quantity += basal_rate_A

@dataclass
class ProductB :
    quantity : float = 0
    name : str = "Product B"
    def update(self,Cytoplasm):
        pass
    
@dataclass
class Transformation:
    Substrate : object
    Product : object
    Enzyme : object
    Substrate : SubstrateA
    Product : ProductB
    Enzyme : EnzymeA
    rate: float = k
    def update(self):
        #Enzyme A catalyzes the chemical reaction: Substrate A →Product B. The rate of this reaction depends on the concentration of available Enzyme A and Substrate A.
        delta = self.rate * self.Substrate.quantity * self.Enzyme.quantity
        self.Substrate.quantity -= delta
        self.Product.quantity += delta/rapport_Substrate_Product #for 10 substrate formation of 1 produit (arbitrary)

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
circuit.simulate(steps=300)