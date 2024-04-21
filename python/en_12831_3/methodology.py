import functions as f
from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class Water:
    temperature: float # *C
    density: float = field(init=False) # kg/m3
    specific_heat_capacity = 4200 # J/kgK

    def __post_init__(self):
        self.density = f.density_of_water(self.temperature) 



@dataclass
class ChargingStorageSystem:
    name: str


@dataclass
class MixedStorageSystem:
    name: str

water = Water(temperature=20)

print(water)