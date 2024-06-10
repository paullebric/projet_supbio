from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt
dico_rate ={"temperature":1,
            "eat":0.0005,
            "big_mammals_threshold":10
}
@dataclass
class Etre_vivant :
    pop : float
    Birth_rate : float = 0
    Death_rate : float = 0
@dataclass
class Tree(Etre_vivant):
    name : str = "Tree"
    saturation_threshold : float =0
    def update(self):
        #Ici si il y a trop d'arbres il n'y en a plus qui naissent
        # self.Birth_rate = 1+(self.saturation_threshold/self.pop)/(100+(dico_rate["temperature"]*2)**2)
        self.pop *= self.Birth_rate/self.Death_rate


@dataclass
class Liane(Etre_vivant):
    name : str = "Liane"
    def update(self):
        self.pop /= self.Death_rate

@dataclass
class Big_mammals(Etre_vivant):
    name : str = "Big_mammals"
    def update(self):
        self.pop += self.Birth_rate*self.pop-self.Death_rate*self.pop

@dataclass
class Small_mammals(Etre_vivant):
    name : str = "Small_mammals"
    def update(self):
        self.pop += self.Birth_rate*self.pop-self.Death_rate*self.pop


@dataclass
class Interaction :
    big_mammals : Big_mammals
    small_mammals : Small_mammals
    tree : Tree
    liane : Liane
    def __init__(self,ETRES):
        self.big_mammals = ETRES["Big_mammals"]
        self.small_mammals = ETRES["Small_mammals"]
        self.tree = ETRES["Tree"]
        self.liane = ETRES["Liane"]
    def update(self):
        #1)les arbres permettent au liane de grandir (les lianes grandissent tant qu'il y a moins de 2 lianes par arbres)
        self.liane.pop += (self.tree.pop - self.liane.pop/3)/(8-dico_rate["temperature"])
        #2)les lianes tuent les arbres (les lianes détruisent les arbres quand il y en a plus de 2 par arbres)
        if self.tree.pop < self.liane.pop/2:
            self.tree.pop -= (self.liane.pop - self.tree.pop/2)/(500+dico_rate["temperature"])
        #3)les lianes permettent au petits animaux de survivrent
        self.small_mammals.pop = (1+self.liane.pop/1000)*self.small_mammals.pop
        #4)les gros animaux mangent les petits
        delta = dico_rate["eat"] * self.big_mammals.pop * self.small_mammals.pop
        self.big_mammals.pop += delta/10
        self.small_mammals.pop -= delta
        #5)les gros animaux rependent les graines des arbres
        self.tree.Birth_rate *= 1 + (self.big_mammals.pop-dico_rate["big_mammals_threshold"])/100
@dataclass
class Circuit :
    ETREVIVANT: list[Etre_vivant]
    INTERACTIONS : Interaction
    def __init__(self):
        self.ETREVIVANT = []
    def add(self,objet):
        self.ETREVIVANT.append(objet)
    def add_interaction(self):
        dico={}
        for x in self.ETREVIVANT :
            dico[x.name]=x
        self.INTERACTIONS = Interaction(dico)
    def simulate(self, steps):
        self.add_interaction()
        data = {}
        for x in self.ETREVIVANT:
            data[x.name] = []
        for i in range(steps):
            for x in self.ETREVIVANT:
                data[x.name].append(x.pop)
            self.INTERACTIONS.update()
            for m in self.ETREVIVANT:
                m.update()
        df = pd.DataFrame(data)
        df.plot()
        plt.show()

circuit = Circuit()
circuit.add(Tree(Death_rate=1.03,Birth_rate=1.05,pop=100,saturation_threshold=400))
circuit.add(Liane(Death_rate=1.1,pop=100))
circuit.add(Small_mammals(Death_rate=1.05,Birth_rate=1.05,pop=10))
circuit.add(Big_mammals(Death_rate=1.05,Birth_rate=1.05,pop=10))
circuit.simulate(steps=10)
