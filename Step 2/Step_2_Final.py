from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt

#
dico_rate ={"Renard_Pluvier" : 0.00005,
            "Fuite_Renard" : 0.0004,
            "Pluvier_Vison" : 0.0004,
            "Renard_Vison" : 0.00007
}
@dataclass
class Choses :
    pop : float
    Birth_rate : float = 0
    Death_rate : float = 0
@dataclass
class Renard(Choses):
    name : str = "Renard"
    def update(self):
        if self.pop<=0:
            self.pop = 1
        else:
            self.pop -= self.pop*self.Death_rate
@dataclass
class Pluvier(Choses):
    name : str = "Pluvier"
    def update(self):
        self.pop += self.Birth_rate * self.pop

@dataclass
class Cage(Choses):
    name : str = "Cage"
    state : bool = False
    active : bool = True
    def update(self):
        if self.active :
            if self.state :
                self.pop +=0.5
            elif self.pop != 0 :
                self.pop -= 0.6
@dataclass
class Vison(Choses):
    name : str = "Vison"
    def update(self):
        if self.pop <=0:
            self.pop = 1
        # self.pop -= self.pop * self.Death_rate

@dataclass
class Interaction :
    cage : Cage
    vison : Vison
    renard : Renard
    pluvier : Pluvier
    def __init__(self,ETRES):
        self.cage = ETRES["Cage"]
        self.vison = ETRES["Vison"]
        self.renard = ETRES["Renard"]
        self.pluvier = ETRES["Pluvier"]
    def update(self):
        #RENARDS CHASSENT LES PLUVIERS
        delta1 = dico_rate["Renard_Pluvier"] * (self.pluvier.pop-self.cage.pop)* self.renard.pop
        self.pluvier.pop -= delta1
        self.renard.pop += delta1
        #Apparition/disparition des cages
        if self.pluvier.pop <20 :
            self.cage.state = True
        if self.pluvier.pop < self.cage.pop or self.pluvier.pop > 300:
            self.cage.state = False
        #Fuite des renards par les cages
        
        self.renard.pop -= self.cage.pop*dico_rate["Fuite_Renard"]*self.renard.pop
        
        delta2 = dico_rate["Pluvier_Vison"] * self.pluvier.pop * self.vison.pop
        self.pluvier.pop -= delta2
        self.vison.pop += delta2/2
        delta3 = dico_rate["Renard_Vison"] * self.vison.pop * self.renard.pop
        self.vison.pop -= delta3
        self.renard.pop += delta3
        
@dataclass
class Circuit :
    ETREVIVANT: list[Choses]
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
circuit.add(Renard(Death_rate=0.0003,Birth_rate=0.05,pop=15))
circuit.add(Pluvier(pop=100,Birth_rate=0.04))
circuit.add(Vison(Death_rate=0.05,pop=15))
circuit.add(Cage(pop=0,active=True))
circuit.simulate(steps=10000)
