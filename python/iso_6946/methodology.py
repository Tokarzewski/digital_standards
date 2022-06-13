import iso_6946.functions as f
from dataclasses import dataclass, field


@dataclass
class Material:
    name: str
    d: float
    k: float
    R: float = field(init=False)

    def __post_init__(self) -> None:
        self.R = f.R(self.d, self.k)


@dataclass
class Construction:
    name: str
    materials: list[Material]
    R_cond: float = field(init=False)

    def __post_init__(self) -> None:
        self.R = f.R_cond(self.materials.R)


