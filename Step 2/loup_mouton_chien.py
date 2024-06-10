from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt

@dataclass
class Etre_vivant :
    pop : float
    Birth_rate : float = 1

@dataclass
class Loup(Etre_vivant):
    name : str = "Loup"
    max_loup : float = 100
    def update(self):
        self.pop *= self.Birth_rate

@dataclass
class Mouton(Etre_vivant):
    name : str = "Mouton"
    mouton_killed : float = 0
    def update(self):
        self.pop *= self.Birth_rate

@dataclass
class Chien(Etre_vivant):
    name : str = "Chien"
    def update(self):
        self.pop *= self.Birth_rate

@dataclass
class Interaction :
    chien : Chien
    loup : Loup
    mouton : Mouton
    def __init__(self,ETRES):
        self.chien = ETRES["Chien"]
        self.loup = ETRES["Loup"]
        self.mouton = ETRES["Mouton"]
    def update(self):
        #chaque chien fait peur a 5 loups
        delta = (self.loup.pop - self.chien.pop*5)/3
        if delta <= 0 :
            self.chien.pop -= 1
            self.loup.pop -= 3
        else :
            self.mouton.pop -= delta
            if self.loup.max_loup > self.loup.pop :
                self.loup.pop += delta
            else :
                self.loup.pop -= delta
            self.mouton.mouton_killed+=delta
        if self.mouton.mouton_killed > 10 :
            self.mouton.mouton_killed = 0
            self.chien.pop += 1

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
circuit.add(Mouton(pop = 40, Birth_rate= 1.05))
circuit.add(Loup(pop = 10, max_loup = 20))
circuit.add(Chien(pop = 0))
circuit.simulate(steps=100)
