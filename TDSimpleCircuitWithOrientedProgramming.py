from dataclasses import dataclass
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
@dataclass
class Wolf:
    population: float
    death_rate: float
    name: str = "Wolf"

    def update(self):
        self.population -= self.population * self.death_rate

@dataclass
class Rabbit:
    population: float
    birth_rate: float
    name: str = "Rabbit"

    def update(self):
        self.population += self.population * self.birth_rate

@dataclass
class Interaction:
    prey: object
    predator: object
    rate: float

    def update(self):
        delta = self.rate * self.prey.population * self.predator.population
        self.prey.population -= delta
        self.predator.population += delta




@dataclass
class Circuit:
    animals: List[object] # = []
    interactions: List[Interaction]

    def __init__(self):
        self.animals = []
        self.interactions = []

    def add_animal(self, x):
        self.animals.append(x)

    def add_interaction(self, prey, predator, rate):
        i = Interaction(prey, predator, rate)
        self.interactions.append(i)

    def simulate(self, n):
        #data = { x.name : [] for x in self.animals}
        data = {}
        for x in self.animals:
            data[x.name] = []
        for k in range(n):
            for animal in self.animals:
                animal.update()
            for interation in self.interactions:
                interation.update()
            for animal in self.animals:
                data[animal.name].append(animal.population)
        return data
    
    def plot(self, n):
        data = self.simulate(n)
        df = pd.DataFrame(data)
        df.plot()
    
lapins= Rabbit(100,0.03)
loups= Wolf(100,0.05)


c= Circuit()
c.add_animal(lapins)
c.add_animal(loups)
c.add_interaction(lapins, loups, 0.0005)
c.plot(600)
plt.show()


