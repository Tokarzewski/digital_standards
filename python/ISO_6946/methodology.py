import iso_6946.functions as f
from dataclasses import dataclass, field


@dataclass
class Material:
    name: str
    thickness: float
    conductivity: float
    resistance: float = field(init=False)

    def __post_init__(self) -> None:
        self.resistance = f.R(self.thickness, self.conductivity)


@dataclass
class Construction:
    name: str
    materials: list
