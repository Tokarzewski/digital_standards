from math import log
from numpy import iterable


def U1(R_tot):
    """Function 1 - Thermal transmittance."""
    return 1 / R_tot


def R_c_op(U, R_si, R_se):
    """Fuctnion 2 - Thermal resistance of the component."""
    return 1 / U - R_si - R_se


def R(d, k):
    """Function 3 - Thermal resistance of homogenous layer."""
    return d / k


def R_tot1(R_si, R_n, R_se):
    """Function 4 -
    Total thermal resistance of a building component
    of homogeneous layers."""
    if iterable(R_n):
        R_n = sum(R_n)
    return R_si + R_n + R_se


def R_tot2(R_tot_upper, R_tot_lower):
    """Function 5 -
    Total thermal resistance of a building component
    of inhomogeneous layers."""
    return (R_tot_upper + R_tot_lower) / 2


def R_tot_upper(f_q, R_tot_q):
    """Function 6 - Upper limit of the total thermal resistance."""
    return 1 / sum([f / R for f, R in zip(f_q, R_tot_q)])


def R_j1(f_q, R_qj):
    """Function 7 - Equivalent thermal resistance."""
    return 1 / sum([f / R for f, R in zip(f_q, R_qj)])


def R_j2(d_j, k_eq_j):
    """Function 8 - Alternative method of an equivalent thermal resistance."""
    return d_j / k_eq_j


def k_eq_j(k_qj, f_q):
    """Function 9 - Equivalent thermal conductivity."""
    return sum([k * f for k, f in zip(k_qj, f_q)])


def e(R_tot_upper, R_tot_lower):
    """Function 10 - Maximum relative error."""
    R_tot = R_tot2(R_tot_upper, R_tot_lower)
    return (R_tot_upper + R_tot_lower) * 50 / R_tot


def R_tot3(A_ve, R_tot_nve, R_tot_ve):
    """Function 11 -
    Total thermal resistance of a component with
    a slightly ventilated air layer."""
    return (1500 - A_ve) * R_tot_nve / 1000 + (A_ve - 500) * R_tot_ve / 1000


def R_u(A_i, A_e_k, U_e_k, n, V):
    """Function 12 - Thermal resistance of unheated space."""
    if iterable(A_e_k):
        Sum_k = sum([A * U for A, U in zip(A_e_k, U_e_k)])
    else:
        Sum_k = A_e_k * U_e_k
    return A_i / (Sum_k + 0.33 * n * V)


# Annex C - Surface Resistance


def R_s_c(environment="in", direction="horizontal"):
    """Surface resistance conventional"""
    if environment == "in":
        switcher = {"upwards": 0.1, "horizontal": 0.13, "downwards": 0.17}
        return switcher.get(direction.lower())
    elif environment == "ext":
        return 0.04


def R_s(h_c, h_r):
    """Function C.1 - Surface resistance."""
    return 1 / (h_c + h_r)


def h_r(epsilon, h_r0):
    """Function C.2 - Radiative coefficient."""
    return epsilon * h_r0


def h_r0(T_mn):
    """Function C.3 - Radiative coefficient for a black-body surface."""
    return 4 * 5.67 * 10e-8 * T_mn**3


def h_ci(direction):
    """Function C.4 - Convective surface coefficient for internal surface."""
    switcher = {"upwards": 5.0, "horizontal": 2.5, "downwards": 0.7}
    return switcher.get(direction.lower())


def h_ce(v):
    """Function C.6 - Convective surface coefficient for external surface."""
    return 4 + 4 * v


def R_sp(R_s, A_p, A):
    """Function C.7 -
    Surface resistance over the projected area of the protruding part."""
    return R_s * A_p / A


# Annex D - Thermal resistance of airspaces


def R_a1(h_a, h_r):
    """Function D.1 -
    Thermal resistance of the unventiled airspaces with length and width
    both more than 10 times thickness."""
    return 1 / (h_a + h_r)


def h_a(deltaT, d, alfa):
    """Function D.2 - Conduction/convection coefficient."""
    if deltaT <= 5:
        # Table D.1
        h_a_90 = 1.25
        h_a_0 = 1.95
    else:
        # Table D.2
        h_a_90 = 0.73 * deltaT ** (1 / 3)
        h_a_0 = 1.14 * deltaT ** (1 / 3)
    return max(h_a_90 + (h_a_90 - h_a_0) * (alfa - 90) / 90, 0.025 / d)


def h_r1(E, h_r0):
    """Function D.3 - Radiative coefficient."""
    return E * h_r0


def E(ε_1, ε_2):
    """Function D.4 - Intersurface emittance."""
    return 1 / (1 / ε_1 + 1 / ε_2 - 1)


def R_a2(h_a, h_r):
    """Function D.5 - Thermal resistance of the small or divided airspaces."""
    return 1 / (h_a + h_r)


def h_r2(h_r0, epsilon_1, epsilon_2, d, b):
    """Function D.6 -
    Radiative coefficient of the small or divided airspaces."""
    return h_r0 / (
        (1 / epsilon_1 + 1 / epsilon_2 - 2)
        + 2 / (1 - d / b + (1 + d**2 / b**2) ** 0.5)
    )


# Annex E - Calculation of the thermal transmittance
# of components with tapered layers


def U2(R_0, R_2):
    """Function E.1 -
    Thermal transmittance for rectangular area."""
    return 1 / R_2 * log(1 + R_2 / R_0)


def U3(R_0, R_2):
    """Function E.2 -
    Thermal transmittance for traingular area, thickest at apex."""
    return 2 / R_2 * ((1 + R_0 / R_2) * log(1 + R_2 / R_0) - 1)


def U4(R_0, R_2):
    """Function E.3 -
    Thermal transmittance for traingular area, thinnest at apex."""
    return 2 / R_2 * (1 - R_0 / R_2 * log(1 + R_2 / R_0))


def U5(R_0, R_1, R_2):
    """Function E.4 -
    Thermal transmittance for traingular area,
    different thickness at each vertex."""
    return (
        2
        * (
            R_0 * R_1 * log(1 + R_2 / R_0)
            - R_0 * R_2 * log(1 + R_1 / R_0)
            + R_1 * R_2 * log((R_0 + R_2) / (R_0 + R_1))
        )
        / (R_1 * R_2 * (R_2 - R_1))
    )


def U6(U_i, A_i):
    """Function E.7 -
    Overall thermal transmittance for the whole area."""
    if iterable(U_i):
        Sum_U_A = sum([U * A for U, A in zip(U_i, A_i)])
        Sum_A = sum(A_i)
        return Sum_U_A / Sum_A
    else:
        return U_i


# Annex F - Correction to thermal transmittance


def U_c(U, deltaU):
    """Function F.1 - Corrected thermal transmittance."""
    return U + deltaU


def deltaU(deltaU_g, deltaU_f, deltaU_r):
    """Function F.2 - Correction term."""
    return deltaU_g + deltaU_f + deltaU_r


def deltaU_g(deltaU_bis, R_1, R_tot):
    """Function F.3 - Correction for air voids."""
    return deltaU_bis * (R_1 / R_tot) ** 2


def deltaU_f1(n_f, X):
    """Function F.4 - Correction for mechanical fasteners, X from ISO 10211."""
    return n_f * X


def deltaU_f2(k_f, A_f, n_f, R_1, R_tot, d_1, d_0=0):
    """
    Function F.5 -
    Approximate procedure for correction for mechanical fasteners.
    """
    if d_0 == 0:
        alfa = 0.8
    else:
        alfa = 0.8 * d_1 / d_0
    return alfa * k_f * A_f * n_f / d_1 * (R_1 / R_tot) ** 2


def deltaU_r(p, f, x, R_1, R_tot):
    """Function F.6 -
    Correction due to water flowing between the insulation
    and the waterproofing membrane."""
    return p * f * x * (R_1 / R_tot) ** 2