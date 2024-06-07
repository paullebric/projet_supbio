from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt

@dataclass
class Metabolite :
    name : str
    qty : float
@dataclass
class GnRH(Metabolite):
    rateG : float = 1
    def update(self):
        self.qty += self.rateG
@dataclass
class Interaction :
    METABOLITES : list[Metabolite]
    rate : dict
    # def __init__(self):
    #     self.METABOLITES=[]
    #     self.rate={}
    def update(self):
        pass

@dataclass
class Circuit :
    METABOLITES: list[Metabolite]
    INTERACTIONS : Interaction
    def __init__(self):
        self.METABOLITES = []
    def add(self,objet):
        self.METABOLITES.append(objet)
    def add_interaction(self,rate):
        self.INTERACTIONS = Interaction(METABOLITES=self.METABOLITES,rate=rate)
    def simulate(self, steps):
        data = {}
        for x in self.METABOLITES:
            data[x.name] = []
        for i in range(steps):
            for x in self.METABOLITES:
                data[x.name].append(x.qty)
            self.INTERACTIONS.update()
            for m in self.METABOLITES:
                m.update()
            df = pd.DataFrame(data)
        df.plot()
        plt.show()

rate = {"rate":0
}
circuit = Circuit()
circuit.add(GnRH("GnRH",0))
circuit.add_interaction(rate)
circuit.simulate(steps=300)
