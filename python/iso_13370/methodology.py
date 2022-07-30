import iso_13370.functions as f
from iso_6946.methodology import Construction
from dataclasses import dataclass, field


@dataclass
class Ground:
    name: str
    conductivity: float


@dataclass
class SlabOnGroundFloor:
    name: str
    area: float
    perimeter: float
    ground: Ground
    construction: Construction
    d_w_e: float
    R_f_sog: float

    B: float = field(init=False)
    d_f: float = field(init=False)
    U_fg_sog: float = field(init=False)

    def __post_init__(self) -> None:
        self.B = f.B(A=self.area, P=self.perimeter)
        self.d_f = f.d_f(
            d_w_e=self.d_w_e,
            k_g=self.ground.conductivity,
            R_si=0.1,
            R_f_sog=self.R_f_sog,
            R_se=0,
        )
        self.U_fg_sog = f.U_fg_sog(k_g=self.ground.conductivity, B=self.B, d_f=self.d_f)


@dataclass
class SuspendedFloor:
    name: str
    area: float
    perimeter: float
    ground: Ground

    B: float = field(init=False)

    def __post_init__(self) -> None:
        self.B: float = f.B(A=self.area, P=self.perimeter)


@dataclass
class HeatedBasement:
    name: str
    area: float
    perimeter: float
    ground: Ground

    B: float = field(init=False)

    def __post_init__(self) -> None:
        self.B: float = f.B(A=self.area, P=self.perimeter)


@dataclass
class UnheatedBasement:
    name: str
    area: float
    perimeter: float
    ground: Ground

    B: float = field(init=False)

    def __post_init__(self) -> None:
        self.B: float = f.B(A=self.area, P=self.perimeter)
