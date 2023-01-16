from dataclasses import dataclass


@dataclass #this is called a python decorator
class Coord:
    x: int = 0
    y: int = 0
    z: int = 0

    def __add__(self, c):
        return Coord(self.x + c.x, self.y + c.y, self.z + c.z)



newcoord = Coord(12,14,15)

secondcoord = Coord(12,14,15)


print(newcoord.x)
print(newcoord.y)
print(newcoord)
print([newcoord, secondcoord])
print(newcoord is secondcoord)