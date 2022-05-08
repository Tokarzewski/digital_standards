from math import log, sqrt, prod, e
from scipy.interpolate import CubicSpline, interp2d
import numpy as np

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
    """Function A.12 - Surface covering factor for system type B."""
    return 1 / (
        1 + B * a_U * a_W**m_W * a_WL * a_K * R_lambda_B * (1 + 0.44 * sqrt(W))
    )


def a_U(alfa, s_u, k_E, s_u_0=0.045, k_u_o=1):
    """Function A.13 - Covering factor for system type B."""
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


def a_WL1(a_W, a_0, L_WL, W):
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


def a_U(R_k_B, W):
    """Table A.3 - Covering factor for system types A, C, H, I, J."""

    x_R_k_B = [0, 0.05, 0.1, 0.15]
    y_W = [0.05, 0.075, 0.1, 0.15, 0.2, 0.225, 0.3, 0.375]
    z_a_U = [
        [1.069, 1.056, 1.043, 1.037],
        [1.066, 1.053, 1.041, 1.035],
        [1.063, 1.050, 1.039, 1.0335],
        [1.057, 1.046, 1.035, 1.0305],
        [1.051, 1.041, 1.0315, 1.0275],
        [1.048, 1.038, 1.0295, 1.026],
        [1.0395, 1.031, 1.024, 1.021],
        [1.03, 1.0221, 1.0181, 1.015]
    ]
    cs = interp2d(x_R_k_B, y_W, z_a_U, kind="cubic")
    return float(cs(R_k_B, W))


def a_D(R_k_B, W):
    """Table A.4 - Pipe external diameter factor for system types A, C, H, I, J."""

    x_R_k_B = [0, 0.05, 0.1, 0.15]
    y_W = [0.05, 0.075, 0.1, 0.15, 0.2, 0.225, 0.3, 0.375]
    z_a_D = [
        [1.013, 1.013, 1.012, 1.011],
        [1.021, 1.019, 1.016, 1.014],
        [1.029, 1.025, 1.022, 1.018],
        [1.040, 1.034, 1.029, 1.024],
        [1.046, 1.040, 1.035, 1.030],
        [1.049, 1.043, 1.038, 1.033],
        [1.053, 1.049, 1.044, 1.039],
        [1.056, 1.051, 1.046, 1.042]
    ]
    cs = interp2d(x_R_k_B, y_W, z_a_D, kind="cubic")
    return float(cs(R_k_B, W))


def B_G1(s_u, k_E, W):
    """Table A.5 - Coefficient for s_u/k <= 0.792 for system types A, C, H, I, J."""

    x_s_u_k_E = [0.01, 0.0208, 0.0292, 0.0375, 0.0458, 0.0542, 0.0625, 0.0708, 0.0792]
    y_W = [0.05, 0.075, 0.1, 0.15, 0.2, 0.225, 0.3, 0.375]
    z_B_G = [
        [85.0, 91.5, 96.8, 100, 100, 100, 100, 100, 100],
        [75.3, 83.5, 89.9, 96.3, 99.5, 100, 100, 100, 100],
        [66.0, 75.4, 82.9, 89.3, 95.5, 98.8, 100, 100, 100],
        [51.0, 61.1, 69.2, 76.3, 82.7, 87.5, 91.8, 95.1, 97.8],
        [38.5, 48.2, 56.2, 63.1, 69.1, 74.5, 81.3, 86.4, 90.0],
        [33.0, 42.5, 49.5, 56.5, 62.0, 67.5, 75.3, 81.6, 86.1],
        [20.5, 26.8, 31.6, 36.4, 51.5, 47.5, 57.5, 65.3, 72.4],
        [11.5, 13.7, 15.5, 18.2, 21.5, 27.5, 40.0, 49.1, 58.3]
    ]
    cs = interp2d(x_s_u_k_E, y_W, z_B_G, kind="cubic")
    return float(cs(s_u/k_E, W))


def B_G2(s_u, W):
    """Table A.6 - Coefficient for s_u/k > 0.792 for system types A, C, H, I, J."""
    x = s_u/W
    if x <= 0.7:
        x_s_u_W = [0.173, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
        y_B_G = [27.5, 40, 57.5, 69.5, 78.2, 84.5, 88.3, 91.6, 94, 96.3, 98.6, 99.8]
        cs = CubicSpline(x_s_u_W, y_B_G)
        return cs(x)
    else:
        return 100


def n_G1(s_u, k_E, W):
    """Table A.7 - Exponent for s_u/k <= 0.792 for system types A, C, H, I, J."""

    x_s_u_k_E = [0.01, 0.0208, 0.0292, 0.0375, 0.0458, 0.0542, 0.0625, 0.0708, 0.0792]
    y_W = [0.05, 0.075, 0.1, 0.15, 0.2, 0.225, 0.2625, 0.3, 0.3375, 0.375]
    z_n_G = [
        [0.008, 0.005, 0.002, 0, 0, 0, 0, 0, 0],
        [0.024, 0.021, 0.018, 0.011, 0.002, 0, 0, 0, 0],
        [0.046, 0.043, 0.041, 0.033, 0.014, 0.005, 0, 0, 0],
        [0.088, 0.085, 0.082, 0.076, 0.055, 0.038, 0.024, 0.014, 0.006],
        [0.131, 0.130, 0.129, 0.123, 0.105, 0.083, 0.057, 0.040, 0.028],
        [0.155, 0.154, 0.153, 0.146, 0.130, 0.110, 0.077, 0.056, 0.041],
        [0.197, 0.196, 0.196, 0.190, 0.173, 0.150, 0.110, 0.083, 0.062],
        [0.254, 0.253, 0.253, 0.245, 0.228, 0.195, 0.145, 0.114, 0.086],
        [0.322, 0.321, 0.321, 0.310, 0.293, 0.260, 0.187, 0.148, 0.115],
        [0.422, 0.421, 0.421, 0.405, 0.385, 0.325, 0.230, 0.183, 0.142]
    ]
    cs = interp2d(x_s_u_k_E, y_W, z_n_G, kind="cubic")
    return float(cs(s_u/k_E, W))


def n_G2(s_u, W):
    """Table A.8 - Exponent for s_u/k > 0.792 for system types A, C, H, I, J."""
    x = s_u/W
    if x <= 0.7:
        x_s_u_W = [0.173, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
        y_n_G = [0.32, 0.23, 0.145, 0.097, 0.067, 0.048, 0.033, 0.023, 0.015, 0.009, 0.005, 0.002]
        cs = CubicSpline(x_s_u_W, y_n_G)
        return cs(x)
    else:
        return 0


def a_W(s_u, k_E):
    """Table A.9 - Pipe spacing factor for system type B."""
    x_s_u_k_E = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1, 0.15, 0.18]
    y_a_W = [1.103, 1.1, 1.097, 1.094, 1.091, 1.088, 1.082, 1.075, 1.064, 1.059]
    cs = CubicSpline(x_s_u_k_E, y_a_W)
    return cs(s_u / k_E)


def b_u(W):
    """Table A.10 - Pipe spacing factor for system type B."""
    if W <= 0.1:
        return 1.0
    elif W < 0.45:
            x_W = [0.1, 0.15, 0.2, 0.225, 0.3, 0.375, 0.45]
            y_b_u = [1, 0.7, 0.5, 0.43, 0.25, 0.1, 0]
            cs = CubicSpline(x_W, y_b_u)
            return cs(W)
    else:
        return 0.0


def a_WL2(s_u, k_E, W):
    """Table A.7 - Exponent for s_u/k <= 0.792 for system types A, C, H, I, J."""

    x_s_u_k_E = [0.01, 0.0208, 0.0292, 0.0375, 0.0458, 0.0542, 0.0625, 0.0708, 0.0792]
    y_W = [0.05, 0.075, 0.1, 0.15, 0.2, 0.225, 0.2625, 0.3, 0.3375, 0.375]
    z_n_G = [
        [0.008, 0.005, 0.002, 0, 0, 0, 0, 0, 0],
        [0.024, 0.021, 0.018, 0.011, 0.002, 0, 0, 0, 0],
        [0.046, 0.043, 0.041, 0.033, 0.014, 0.005, 0, 0, 0],
        [0.088, 0.085, 0.082, 0.076, 0.055, 0.038, 0.024, 0.014, 0.006],
        [0.131, 0.130, 0.129, 0.123, 0.105, 0.083, 0.057, 0.040, 0.028],
        [0.155, 0.154, 0.153, 0.146, 0.130, 0.110, 0.077, 0.056, 0.041],
        [0.197, 0.196, 0.196, 0.190, 0.173, 0.150, 0.110, 0.083, 0.062],
        [0.254, 0.253, 0.253, 0.245, 0.228, 0.195, 0.145, 0.114, 0.086],
        [0.322, 0.321, 0.321, 0.310, 0.293, 0.260, 0.187, 0.148, 0.115],
        [0.422, 0.421, 0.421, 0.405, 0.385, 0.325, 0.230, 0.183, 0.142]
    ]
    cs = interp2d(x_s_u_k_E, y_W, z_n_G, kind="cubic")
    return float(cs(s_u/k_E, W))


def a_WL3(K_WL, D, W):
    """Tables A.11 - A.15 - Heat conduction device factor for system type B."""
    x_D = [0.014, 0.016, 0.018, 0.020, 0.022]
    y_W = [0.05, 0.075, 0.1, 0.15, 0.2, 0.225, 0.3, 0.375, 0.45]
    z_K_WL = [0, 0.1, 0.2, 0.3, 0.4]
    a_WL = [
        [ # Table A.11 for K_WL = 0.0
            [0.82, 0.86, 0.9, 0.93, 0.96],
            [0.59, 0.644, 0.7, 0.754, 0.8],
            [0.488, 0.533, 0.576, 0.617, 0.658],
            [0.387, 0.415, 0.444, 0.47, 0.505],
            [0.337, 0.357, 0.379, 0.4, 0.422],
            [0.32, 0.34, 0.357, 0.376, 0.396],
            [0.288, 0.3, 0.315, 0.33, 0.344],
            [0.266, 0.278, 0.29, 0.3, 0.312],
            [0.25, 0.264, 0.28, 0.29, 0.3]
        ],
        [ # Table A.12 for K_WL = 0.1
            [0.88, 0.905, 0.93, 0.955, 0.975],
            [0.74, 0.776, 0.812, 0.836, 0.859],
            [0.66, 0.693, 0.726, 0.76, 0.77],
            [0.561, 0.58, 0.6, 0.621, 0.642],
            [0.49, 0.51, 0.53, 0.55, 0.57],
            [0.467, 0.485, 0.504, 0.522, 0.54],
            [0.435, 0.444, 0.453, 0.462, 0.472],
            [0.411, 0.421, 0.434, 0.446, 0.46],
            [0.41, 0.42, 0.43, 0.44, 0.45]
        ],
        [ # Table A.13 for K_WL = 0.2
            [0.92, 0.937, 0.955, 0.97, 0.985],
            [0.845, 0.865, 0.885, 0.893, 0.902],
            [0.81, 0.821, 0.832, 0.843, 0.855],
            [0.735, 0.745, 0.755, 0.765, 0.775],
            [0.68, 0.688, 0.695, 0.703, 0.71],
            [0.655, 0.663, 0.67, 0.678, 0.685],
            [0.585, 0.592, 0.6, 0.608, 0.615],
            [0.55, 0.558, 0.565, 0.573, 0.58],
            [0.55, 0.555, 0.56, 0.565, 0.57],
        ],
        [ # Table A.14 for K_WL = 0.3
            [0.95, 0.96, 0.97, 0.98, 0.99],
            [0.92, 0.925, 0.93, 0.935, 0.94],
            [0.9, 0.905, 0.91, 0.915, 0.92],
            [0.855, 0.855, 0.855, 0.855, 0.855],
            [0.8, 0.8, 0.8, 0.8, 0.8],
            [0.79, 0.79, 0.79, 0.79, 0.79],
            [0.72, 0.72, 0.72, 0.72, 0.72],
            [0.69, 0.69, 0.69, 0.69, 0.69],
            [0.68, 0.68, 0.68, 0.68, 0.68],
        ],
        [ # Table A.15 for K_WL = 0.4
            [0.97, 0.978, 0.985, 0.99, 0.995],
            [0.965, 0.964, 0.963, 0.962, 0.96],
            [0.94, 0.94, 0.94, 0.94, 0.94],
            [0.895, 0.895, 0.895, 0.895, 0.895],
            [0.86, 0.86, 0.86, 0.86, 0.86], 
            [0.84, 0.84, 0.84, 0.84, 0.84], 
            [0.78, 0.78, 0.78, 0.78, 0.78], 
            [0.76, 0.76, 0.76, 0.76, 0.76], 
            [0.75, 0.75, 0.75, 0.75, 0.75], 
        ]
    ]
    return 1


def a_WL4(D, W):
    """Table A.11 - Heat conduction device factor for system type B, K_WL=0."""
    x_D = [0.014, 0.016, 0.018, 0.020, 0.022]
    y_W = [0.05, 0.075, 0.1, 0.15, 0.2, 0.225, 0.3, 0.375, 0.45]
    z_n_G = [
        [0.82, 0.86, 0.9, 0.93, 0.96],
        [0.59, 0.644, 0.7, 0.754, 0.8],
        [0.488, 0.533, 0.576, 0.617, 0.658],
        [0.387, 0.415, 0.444, 0.47, 0.505],
        [0.337, 0.357, 0.379, 0.4, 0.422],
        [0.32, 0.34, 0.357, 0.376, 0.396],
        [0.288, 0.3, 0.315, 0.33, 0.344],
        [0.266, 0.278, 0.29, 0.3, 0.312],
        [0.25, 0.264, 0.28, 0.29, 0.3]
    ]
    cs = interp2d(x_D, y_W, z_n_G, kind="cubic")
    return float(cs(D, W))


# ISO 11855-3:2021 FUNCTIONS