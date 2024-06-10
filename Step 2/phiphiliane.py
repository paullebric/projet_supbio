from dataclasses import dataclass
import pandas as pd
from typing import List
import matplotlib.pyplot as plt


protection_threshold = 20
hunt_rate = 0.0005

@dataclass
class Animals:
    population:float
    name:str

@dataclass
class Pluvier(Animals):
    birth_rate:int

    def update(self):
        self.population += self.population*self.birth_rate



@dataclass
class Cages(Animals):
    placing_rate:int
    state:bool = False

    def update(self):
        if self.state ==True :
            self.population += self.placing_rate
        elif self.population > 0:
            self.population -=self.placing_rate

@dataclass
class Interactions:
    renards:Animals
    birds:Pluvier
    furet: Animals
    cage:Cages
    
    def update(self):

        if self.birds.population < self.cage.population or self.birds.population > 200:
            self.cage.state = False
        elif self.birds.population < protection_threshold:
            self.cage.state = True


            
        if self.cage.state == False:
            delta = hunt_rate * self.renards.population * self.birds.population
            self.birds.population -= delta
            self.renards.population += delta/5

        if self.renards.population - self.cage.population > 0:
            self.renards.population -= self.cage.population
        
        if self.renards.population < self.cage.population:
            delta = 1+ hunt_rate *self.furet.population* self.birds.population
            self.birds.population -= delta
            self.furet.population += delta/5        

        if self.renards.population * 2 > self.cage.population:
            self.furet.population *=0.7
        self.birds.population += self.birds.population*self.birds.birth_rate

    
        self.cage.update()


@dataclass
class Circuit:
    Ecosysteme : List[Animals]
    Feedback : List[Interactions]
    df: list

    def __init__(self):
        self.Ecosysteme = []
        self.Feedback = []
        

    def add(self,objet):
        self.Ecosysteme.append(objet)

    def add_interactions(self,renard,bird,furet,cage):
        i = Interactions(renard,bird,furet,cage)
        self.Feedback.append(i)


    def simulate(self, steps):
        data = {}
        for x in self.Ecosysteme:
            data[x.name] = []
        for k in range(steps):
            for inter in self.Feedback:
                inter.update()
            for protein in self.Ecosysteme:
                data[protein.name].append(protein.population)
            self.df = pd.DataFrame(data)
        return data
    
    def plot(self, n):
        data = self.simulate(n)
        df = pd.DataFrame(data)
        df.plot()




fox = Animals(15,"fox")
bird = Pluvier(60,"bird",0.03)
vison = Animals(0,"vison")
cage = Cages(0,"cage",placing_rate=0.09)

circuit = Circuit()
circuit.add(fox)
circuit.add(bird)
circuit.add(vison)
circuit.add(cage)

circuit.add_interactions(fox,bird,vison,cage)
circuit.plot(10000)
plt.show()
