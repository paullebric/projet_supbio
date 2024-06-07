from dataclasses import dataclass

@dataclass
class Car:
    # speed: float
    # remainning_dist: float

    def __init__(self,speed,remaining_dist):
        self.remaining_dist = remaining_dist
        self.speed = speed

    def get_arrival_time(self):
        print(self.remaining_dist/self.speed)


a = Car(100,200)
b = Car(300,400)

a.get_arrival_time()
b.get_arrival_time()