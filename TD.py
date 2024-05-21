from dataclasses import dataclass

@dataclass
class Arbre:
    racine:str
    fg:"Arbre"=None
    fd:"Arbre"=None
    def size(self):
        x=1
        if self.fg is not None :
            x+=self.fg.size()
        if self.fd is not None :
            x+=self.fd.size()
        return x
    def __len__(self):
        return self.size()
    def __repr__(self):
        return "mon arbre"
    

t = Arbre("A",fd=Arbre("B"))
print(t)

