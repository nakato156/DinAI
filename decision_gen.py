import random

class Gen():
    def  __init__(self, vel: int, dist: int = None) -> None:
        self.score:int = None
        self.velocidad = vel
        self.distance = dist or random.randint(1, 10)
    
    def fitnes(self) -> int:
        return self.score
    
    def compara_fit(self, other):
        return self if self.fitnes() > other.fitnes() else other
    
    def hijo(self, other):
        return Gen(self.velocidad, (self.distance + other.distance) // 2).mutar()
    
    def mutar(self):
        return Gen(self.velocidad, self.distance + random.random().__round__(1))
    
    def play(self, distancia_juego) -> bool:
        return self.distance - .5 >= distancia_juego <= self.distance
    
    def __repr__(self) -> str:
        return f"Gen(velocidad={self.velocidad}, distance={self.distance})"
