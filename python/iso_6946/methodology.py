from iso_6946.functions import U1, R_tot1
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
    R_c_op: float = field(init=False)

    def __post_init__(self) -> None:
        self.R_c_op = sum([material.R for material in self.materials])


@dataclass
class SurfaceResistance:
    name: str
    boundary: str
    direction: str
    material: Material


@dataclass
class Transmittance:
    name: str
    construction: Construction
    R_n: float = field(init=False)
    R_si: SurfaceResistance
    R_se: SurfaceResistance

    def __post_init__(self) -> None:
        self.R_n = Construction.R_c_op
        self.R_tot = R_tot1(R_si=self.R_si, R_n=self.R_n, R_se=self.R_se)
        self.U = U1(self.R_tot)
