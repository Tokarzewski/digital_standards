import iso_6946.functions as f
from dataclasses import dataclass, field
from numpy import iterable


@dataclass
class Material:
    name: str
    thickness: float
    conductivity: float
    surface_emissivity: float = 0.9
    R: float = field(init=False)

    def __post_init__(self) -> None:
        self.R = f.R(self.thickness, self.conductivity)


@dataclass
class Construction:
    name: str
    materials: list[Material]
    R_c_op: float = field(init=False)

    def __post_init__(self) -> None:
        if iterable(self.materials):
            self.R_c_op = sum([material.R for material in self.materials])
        else:
            self.R_c_op = self.materials.R


@dataclass
class SurfaceResistance:
    boundary: str
    direction: str
    material: Material
    mean_temperature: float = 10
    wind_speed: float = 4
    R_s: float = field(init=False)

    def __post_init__(self) -> None:

        if self.boundary == "in":
            self.h_c = f.h_ci(self.direction)
        elif self.boundary == "ext":
            self.h_c = f.h_ce(v=self.wind_speed)

        self.h_r0 = f.h_r0(T_mn=self.mean_temperature)
        self.h_r = f.h_r(epsilon=self.material.surface_emissivity, h_r0=self.h_r0)

        self.R_s = f.R_s(self.h_c, self.h_r)


@dataclass
class Transmittance:
    name: str
    construction: Construction
    direction: str
    R_n: float = field(init=False)
    R_si: float = field(init=False)
    R_se: float = field(init=False)
    R_tot: float = field(init=False)
    U: float = field(init=False)

    def __post_init__(self) -> None:
        self.R_n = self.construction.R_c_op

        internal_material = self.construction.materials[-1]
        external_material = self.construction.materials[0]

        self.R_si = SurfaceResistance(
            boundary="in", direction=self.direction, material=internal_material
        )

        self.R_se = SurfaceResistance(
            boundary="ext", direction=self.direction, material=external_material
        )

        self.R_tot = f.R_tot1(R_si=self.R_si.R_s, R_n=self.R_n, R_se=self.R_se.R_s)
        self.U = f.U1(self.R_tot)
