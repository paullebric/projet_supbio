from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as ani

k = 0.07
activation_treshold = 20
feedback_treshold = 20
basal_rate = 1.10  # a peut pres 1.115 pour enzyme A

k = 0.07
activation_treshold=5
feedback_treshold = 10
basal_rate=1.10 #a peut pres 1.115 pour enzyme A*
rapport_Substrate_Product=100
basal_rate_A=10
@dataclass
class ProteinY :
    quantity : float = 0
    name : str = "Protein Y"
    state :bool = True
    prod_rate : float = basal_rate
    def update(self,Cytoplasm):
        """
        if Cytoplasm["Enzyme A"].quantity < feedback_treshold :
            self.quantity *= self.prod_rate
        else :
            self.quantity -= Cytoplasm["Enzyme A"].quantity/10#basal rate changeables
        """
        if Cytoplasm["Substrate A"].quantity>activation_treshold:
            self.quantity *= self.prod_rate
        self.quantity -= Cytoplasm["Enzyme A"].quantity/100
        """"""
@dataclass
class EnzymeA :
    quantity : float = 0
    name : str = "Enzyme A"
    def update(self,Cytoplasm):
        '''
        If Y is active: production of Enzyme A is activated.
        If Y is inactive: production of Enzyme A is inhibited.
        '''
        if Cytoplasm["Protein Y"].state ==True :
            self.quantity+=(Cytoplasm["Protein Y"].quantity-self.quantity)/10

@dataclass
class SubstrateA :
    quantity : float = 0
    name : str = "Substrate A"
    def update(self,data):
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
    rate: float = k
    def update(self):
#Enzyme A catalyzes the chemical reaction: Substrate A →Product B. The rate of this reaction depends on the concentration of available Enzyme A and Substrate A.
        delta = self.rate * self.Substrate.quantity * self.Enzyme.quantity
        self.Substrate.quantity -= delta
        self.Product.quantity += delta/rapport_Substrate_Product #pour 10 substrat formation de 1 produit (arbitraire)


@dataclass
class Circuit :
    Cytoplasm : dict
    Transformations : list
    df: list
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
            self.df = pd.DataFrame(data)
            
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
        frames=len(self.df)
        interval = 3
        print(frames)
        animation = ani.FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, interval=interval,repeat=False)
        ax.legend()
        plt.show()

circuit = Circuit()
circuit.add("Enzyme A", EnzymeA(quantity=5))
circuit.add("Protein Y", ProteinY(quantity=5))
circuit.add("Substrate A", SubstrateA(quantity=50))
circuit.add("Product B", ProductB(quantity=0))
circuit.simulate(steps=300)
circuit.animate()
