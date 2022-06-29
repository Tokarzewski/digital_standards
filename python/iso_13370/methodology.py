import iso_13370.functions as f
from iso_6946.methodology import Construction
from dataclasses import dataclass, field


@dataclass
class Ground:
    name: str
    k_g: float


@dataclass
class SlabOnGroundFloor:
    name: str
    A: float
    P: float
    ground: Ground
    construction: Construction
    B: float = field(init=False)
    d_w_e: float
    R_f_sog: float
    d_f: float = field(init=False)
    U_fg_sog: float = field(init=False)

    def __post_init__(self) -> None:
        self.B = f.B(A=self.A, P=self.P)
        self.d_f = f.d_f(
            d_w_e=self.d_w_e,
            k_g=self.ground.k_g,
            R_si=0.1,
            R_f_sog=self.R_f_sog,
            R_se=0,
        )
        self.U_fg_sog = f.U_fg_sog(
            k_g=self.ground.k_g, 
            B=self.B, 
            d_f=self.d_f)

@dataclass
class SuspendedFloor:
    name: str
    A: float
    P: float
    ground: Ground
    B: float = field(init=False)

    def __post_init__(self) -> None:
        self.B: float = f.B(A=self.A, P=self.P)


@dataclass
class HeatedBasement:
    name: str
    A: float
    P: float
    ground: Ground
    B: float = field(init=False)

    def __post_init__(self) -> None:
        self.B: float = f.B(A=self.A, P=self.P)


@dataclass
class UnheatedBasement:
    name: str
    A: float
    P: float
    ground: Ground
    B: float = field(init=False)

    def __post_init__(self) -> None:
        self.B: float = f.B(A=self.A, P=self.P)
