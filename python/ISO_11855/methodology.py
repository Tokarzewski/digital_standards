import functions as f
from dataclasses import dataclass, field


def q_ACHIJ(self):
    """Heat transfer coefficient for system types A, C, H, I, J."""
    if 0.05 <= self.psi <= 0.15:
        k_E = f.k_E_prim(self.psi, self.k_E, self.k_W)
    else:
        k_E = self.k_E
    if self.W <= 0.375:
        q = f.q6(
            a_B=f.a_B1(self.alfa, k_E, self.R_k_B),
            a_W=f.a_W1(self.R_k_B),
            a_U=f.a_U1(self.R_k_B, self.W),
            a_D=f.a_D(self.R_k_B, self.W),
            m_W=f.m_W(self.W),
            m_U=f.m_U(self.s_u),
            m_D=f.m_D(self.D),
            deltat_H=self.deltat_H,
        )
        return q
    else:
        q = f.q6(
            a_B=f.a_B1(self.alfa, k_E, R_k_B),
            a_W=f.a_W1(self.R_k_B),
            a_U=f.a_U1(self.R_k_B, W=0.375),
            a_D=f.a_D(self.R_k_B, W=0.375),
            m_W=f.m_W(W=0.375),
            m_U=f.m_U(self.s_u),
            m_D=f.m_D(self.D),
            deltat_H=self.deltat_H,
        )
        q = f.q8(q_0375=q, W=W)
        return q


def q_B(self):
    """Heat transfer coefficient for system type B."""
    a_U = f.a_U2(self.alfa, self.s_u, self.k_E)
    a_W = f.a_W2(self.s_u, self.k_E)
    b_u = f.b_u(self.W)
    a_K = f.a_K(self.W)
    K_WL = f.K_WL(self.s_WL, self.k_WL, b_u, self.s_u, self.k_E)
    m_W = f.m_W(self.R_k_B)

    if K_WL < 0.5:
        a_WL = f.a_WL2(K_WL, self.W, self.D)
    else:
        a_WL = f.a_WL3(K_WL, self.W, self.D)
    if self.L_WL < self.W:
        a_0 = f.a_WL2(0, self.W, self.D)
        a_WL = f.a_WL1(a_WL, a_0, self.L_WL, self.W)

    a_B = f.a_B2(a_U, a_W, m_W, a_WL, a_K, self.R_k_B, self.W)

    return f.q9(a_B, a_W, a_U, a_WL, a_K, m_W, self.deltat_H)


def q_D(self):
    """Heat transfer coefficient for system type D."""
    a_U = f.a_U2(self.alfa, self.s_u, self.k_E)
    a_B = f.a_B3(a_U, self.R_k_B)
    return f.q10(a_B, a_U, self.deltat_H)


def q(self):
    if self.system_type in "ACHIJ":
        return q_ACHIJ(self)
    elif self.system_type == "B":
        return q_B(self)
    elif self.system_type == "D":
        return q_D(self)
    else:
        return "There is no system type: ", self.system_type


@dataclass
class EmbeddedRadiantSystem:
    system_type: str = "A"  # System type (A, B, C, D, H, I, J)
    case_of_application: str = "Floor heating"

    D: float = 0.016  # External diameter of pipe, including sheating where used
    W: float = 0.10  # Pipe spacing [m]
    s_u: float = 0.02  # Thickness of layer above the pipe [m]
    R_k_B: float = 0.05  # Thermal resistance of the floor covering [m2K/W]
    k_E: float = 1.0  # Thermal conductivity of screed [W/mK]
    psi: float = 0.05  # Volume ratio of the attachement studs in the screed
    k_W: float = 0.5  # Thermal conductivity of the attachements studs
    s_WL: float = 0.002  # Thickness of the heat conducting material [m]
    k_WL: float = 0.35  # Thermal conductivity of the heat conducting material [W/mK]
    L_WL: float = 1.0  # Width of heat conducting device

    t_i: float = 20.0  # Design indoor temperature [*C]
    t_V: float = 40.0  # Supply temperature of heating or cooling medium [*C]
    t_R: float = 35.0  # Return temperature of heating or cooling medium [*C]
    deltat_H: float = field(init=False)  # Medium differential temperature
    alfa: float = field(init=False)
    q: float = field(init=False)

    def __post_init__(self) -> None:
        self.deltat_H = f.deltat_H(self.t_V, self.t_R, self.t_i)
        self.alfa = f.alfa(self.case_of_application)
        self.q = q(self)

UFH_A = EmbeddedRadiantSystem(system_type="A")
UFH_B = EmbeddedRadiantSystem(system_type="B")
UFH_D = EmbeddedRadiantSystem(system_type="D")

for UFH in [UFH_A, UFH_B, UFH_D]:
    print(UFH.system_type, round(UFH.q, 2), "W/m2")