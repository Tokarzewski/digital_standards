from math import log, sqrt, prod, e
from re import X

# ISO 11855-2:2021 FUNCTIONS


def q1(t_S_m, t_i):
    """Function 1 - Heat flux for floor heating and ceiling cooling."""
    return 8.92 * (t_S_m - t_i) ^ 1.1


def q2(t_S_m, t_i):
    """Function 2 - Heat flux for wall heating and cooling."""
    return 8 * abs(t_S_m - t_i)


def q3(t_S_m, t_i):
    """Function 3 - Heat flux for ceiling heating."""
    return 6 * abs(t_S_m - t_i)


def q4(t_S_m, t_i):
    """Function 4 - Heat flux for floor cooling."""
    return 7 * abs(t_S_m - t_i)


def power_product(list_a, list_m):
    return prod([a**m for a, m in zip(list_a, list_m)])


def q5(B, a_i, m_i, deltat_H):
    """Function 5 - Universal single power heat flux function."""
    return B * power_product(a_i, m_i) * deltat_H


def q_des(h_t, t_S_m, t_i):
    """Function 6 - Heat flux for heating and cooling."""
    return h_t * abs(t_S_m - t_i)


# Annex A - Calculation of the heat flux


def deltat_H(t_V, t_R, t_i):
    """Function A.1 - Temperature difference
    between heating fluid and room."""
    return t_V - t_R / log((t_V - t_i) / (t_R - t_i))


# Function A.2 = Function 5


def q6(B, a_B, a_W, a_U, a_D, m_W, m_U, m_D, deltat_H):
    """Function A.3 - Heat flux for system types A, C, H, I, J."""
    a_i = [a_B, a_W, a_U, a_D]
    m_i = [1, m_W, m_U, m_D]
    return q5(B, a_i, m_i, deltat_H)


def a_B1(alfa, lambda_E, R_lambda_B):
    """Function A.4 - Surface covering factor for function A.3."""
    s_u_0 = 0.045
    lambda_u_0 = 1
    return (1 / alfa + s_u_0 / lambda_u_0) / (1 / alfa + s_u_0 / lambda_E + R_lambda_B)


def m_W(W):
    """Function A.5 - Exponent m_W."""
    return 1 - W / 0.075


def m_U(s_u):
    """Function A.6 - Exponent m_U."""
    return 100 * (0.045 - s_u)


def m_D(D):
    """Function A.7 - Exponent m_D."""
    return 250 * (D - 0.020)


def K_H1(a_i, m_i, s_u, s_u_star, lambda_E):
    """Function A.8 - Heat transfer coefficient."""
    return 1 / (1 / power_product(a_i, m_i) + (s_u - s_u_star) / lambda_E)


def q7(K_H, deltat_H):
    """Function A.9 - Heat flux."""
    return K_H * deltat_H


def q8(q_0375, W):
    """Function A.10 - Heat flux for pipe spacing W > 0.375 m for system types A, C, H, I, J."""
    return q_0375 * 0.375 / W


def q9(B, a_B, a_W, a_U, a_WL, a_K, m_W, deltat_H):
    """Function A.11 - Heat flux for system type B."""
    a_i = [a_B, a_W, a_U, a_WL, a_K]
    m_i = [1, m_W, 1, 1, 1]
    return q5(B, a_i, m_i, deltat_H)


def a_B1(B, a_U, a_W, m_W, a_WL, a_K, R_lambda_B, W):
    """Function A.12 - Surface covering factor for function A.11."""
    return 1 / (
        1 + B * a_U * a_W**m_W * a_WL * a_K * R_lambda_B * (1 + 0.44 * sqrt(W))
    )


def a_U(alfa, s_u, k_E, s_u_0=0.045, k_u_o=1):
    """Function A.13 - Covering factor for function A.11."""
    return (1 / alfa + s_u_0 / k_u_o) / (1 / alfa + s_u / k_E)


# Function A.14 = A.5


def K_WL(s_WL, k_WL, b_u, s_u, k_E):
    """
    Function A.15 - Characteristic value for heat conducting device.
    Arguments:
    s_WL - thickness of the heat conducting material,
    k_WL - thermal conductivity of the heat conducting material,
    b_u - correction factor depending on the pipe spacing from table A.17,
    s_u - thickness of the screed,
    k_E - thermal conductivity of the screed.
    """
    return (s_WL * k_WL + b_u * s_u * k_E) * 8


def a_WL1():
    """Tables A.11 - A.16 - Heat conduction device factor."""
    return 1


def a_WL2(a_W, a_0, L_WL, W):
    """Function A.16 - Corrected heat conduction device factor"""
    x = L_WL / W
    return a_W - (a_W - a_0) * (1 - 3.2 * x + 3.4 * x * x - 1.2 * x * x * x)


def q10(a_B, a_U, deltat_H, B=6.5):
    """Function A.17 - Heat flux for system type D."""
    return B * a_B * 1.06 * a_U * deltat_H


def a_B(B, a_U, a_T, m_T, R_k_B):
    """Function A.18 - Surface covering factor"""
    return 1 / (1 + B * a_U * a_T**m_T * R_k_B)


def q_G1(fi, B_G, deltat_H, n_G):
    """Function A.19 - Limit curve of heat flux."""
    return fi * B_G * (deltat_H / fi) ** n_G


def fi(t_F_max, t_i, deltat_o=9):
    """Function A.20 - Factor for conversion to any values."""
    return ((t_F_max - t_i) / deltat_o) ** 1.1


def deltat_H_G(fi, B_G, B, a_i, m_i, n_G):
    """Function A.21 - The intersection of the characteristic curve with the limit curve."""
    return fi * (B_G / (B * power_product(a_i, m_i))) ** (1 / (1 - n_G))


def q_G2(q_G_0375, W, f_G):
    """Function A.22 - Limit curve of heat flux for type A and C system types where W > 0.375 m."""
    return q_G_0375 * 0.375 / W * f_G


def deltat_H_G(t_H_G_0375, f_G):
    """Function A.23 - The limit tempertature difference between the heating medium and the room."""
    return t_H_G_0375 * f_G


def f_G(s_u, W, q_G_max, q_G_0375):
    """Function A.24 -"""
    if s_u / W > 0.173:
        x = q_G_0375 * 0.375 / W
        return (q_G_max - (q_G_max - x) * e ** (-20 * (s_u / W - 0.173) ** 2)) / x
    else:
        return 1


# Functions A.25 - A.27


def k_E_prim(psi, k_E, k_W):
    """Function A.28 - Thermal conductivity of screed with fixing inserts."""
    return (1 - psi) * k_E + psi * k_W


def q_U1(R_u, R_o, q, t_i, t_u):
    """Function A.29 - Downward heat loss."""
    return 1 / R_u * (R_o * q + t_i - t_u)


def R_o(R_k_B, s_u, k_u, alfa=10.8):
    """Function A.30 - Upwards partial heat transmission
    resistance of the floor structure."""
    return 1 / alfa + R_k_B + s_u / k_u


def R_u(R_k_ins, R_k_construction, R_k_plaster, R_alfa):
    """Function A.31 - Downwards partial heat transmission
    resistance of the floor structure."""
    return R_k_ins + R_k_construction + R_k_plaster + R_alfa


def q_U2(q, R_o, R_u):
    """Function A.32 - Downward heat loss when t_i == t_u."""
    return q * R_o / R_u


def K_H2(K_H_Floor, deltaR_alfa, R_k_B, K_H_Floor_star, R_k_B_star=0.15):
    """Function A.33 - Equivalent heat transmission coefficient"""
    return K_H_Floor / (
        1 + ((deltaR_alfa + R_k_B) / R_k_B_star) * (K_H_Floor / K_H_Floor_star - 1)
    )


# Function A.34 = A.9


def deltaR_h(alfa):
    """Function A.35 - Additional thermal transfer resistance."""
    return 1 / alfa - 1 / 10.8


from scipy.interpolate import CubicSpline, interp2d


def a_W(R_k_B):
    """Table A.2 - Pipe spacing factor for system types A, C, H, I, J."""
    x_R_k_B = [0, 0.05, 0.1, 0.15]
    y_a_W = [1.23, 1.188, 1.156, 1.134]
    cs = CubicSpline(x_R_k_B, y_a_W)

    """
    import matplotlib.pyplot as plt
    import numpy as np
    xs = np.arange(0, 0.15, 0.01)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(xs, cs(xs), label="CubicSpline")
    ax.legend(loc='lower left', ncol=2)
    plt.show()
    """
    return cs(R_k_B)


def a_u(R_k_B, T):
    """Table A.3 - Covering factor for system types A, C, H, I, J."""

    x_R_k_B = (0, 0.05, 0.1, 0.15)
    y_T = (0.05, 0.075, 0.1, 0.15, 0.2, 0.225, 0.3, 0.375)
    a_u_table = [
        [1.069, 1.056, 1.043, 1.037],
        [1.066, 1.053, 1.041, 1.035],
        [1.063, 1.050, 1.039, 1.0335],
        [1.057, 1.046, 1.035, 1.0305],
        [1.051, 1.041, 1.0315, 1.0275],
        [1.048, 1.038, 1.0295, 1.026],
        [1.0395, 1.031, 1.024, 1.021],
        [1.03, 1.0221, 1.0181, 1.015],
    ]
    cs = interp2d(x_R_k_B, y_T, a_u_table, kind="cubic")
    return float(cs(R_k_B, T))


# ISO 11855-3:2021 FUNCTIONS
