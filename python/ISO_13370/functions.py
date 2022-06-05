from math import log, cos, sin, sqrt, pi, e


def H_g1(A, U, P, Psi_wf):
    """Function 1 - Steady state ground heat transfer."""
    return A * U + P * Psi_wf


def B(A, P):
    """Function 2 - Characteristic dimension of floor."""
    return 2 * A / P


def d_f(d_w_e, k_g, R_si, R_f_sog, R_se):
    """Function 3 - Total equivalent thickness."""
    return d_w_e + k_g * (R_si + R_f_sog + R_se)


def U_fg_sog1(k_g, B, d_f):
    """Function 4 - Hard core thermal transmittance."""
    return 2 * k_g / (pi * B + d_f) * log(pi * B / d_f + 1)


def U_fg_sog2(k_g, B, d_f):
    """Function 5 - Hard core thermal transmittance."""
    return k_g / (0.457 * B + d_f)


# Functions 6-7 are alternative functions to function 5.


def U_fg_sus(U_f_sus, U_g, U_x):
    """Function 8 - Thermal transmittance of suspended floor."""
    return 1 / (1 / U_f_sus + 1 / (U_g + U_x))


def d_g(d_w_e, k_g, R_si, R_f_ins, R_se):
    """Function 9 - Equivalent thickness for the ground below the suspended floor."""
    return d_w_e + k_g * (R_si + R_f_ins + R_se)


def U_g(k_g, B, d_g):
    """Function 10 - Thermal transmittance of ground."""
    return 2 * k_g / (pi * B + d_g) * log(pi * B / d_g + 1)


def U_x(h, U_w, B, epsilon, v, f_w):
    """Function 11 - Thermal transmittance x."""
    return 2 * h * U_w / B + 1450 * epsilon * v * f_w / B


def f_w(location):
    """Table 8 - Wind shielding factor."""
    switcher = {"sheltered": 0.02, "horizontal": 0.05, "downwards": 0.1}
    return switcher.get(location.lower())


# Function 12 = Function 3


def U_fg_b1(k_g, B, d_f, z):
    """Function 13 - Hard core thermal transmittance."""
    return 2 * k_g / (pi * B + d_f + 0.5 * z) * log(pi * B / (d_f + 0.5 * z) + 1)


def U_fg_b2(k_g, B, d_f, z):
    """Function 14 - Hard core thermal transmittance."""
    return k_g / (0.457 * B + d_f + 0.5 * z)


def d_w_b(k_g, R_si, R_w_b, R_se):
    """Function 15 - Total equivalent thickness for the basement walls."""
    return k_g * (R_si + R_w_b, R_se)


def U_wg_b(k_g, z, d_f, d_w_b):
    """Function 16 - Thermal transmittance of the basement walls."""
    return 2 * k_g / (pi * z) * (1 + 0.5 * d_f / (d_f + z)) * log(z / d_w_b + 1)


def U_bg_eff(A, U_f_b, z, P, U_w_b):
    """Function 17 - Effective thermal transmittance characterizing basement."""
    return (A * U_f_b + z * P * U_w_b) / (A + z * P)


def H_g2(A, U_fg_b, z, P, U_wg_b, Psi_w_f):
    """Function 18 - Steady state ground heat transfer with basements."""
    return A * U_fg_b + z * P * U_wg_b + P * Psi_w_f


def U_ub(U_f_sus, A, U_fg_b, z, P, U_wg_b, h, U_w, c_p, rho, n, V):
    """Function 19 - Thermal transmittance of unheated ventilated basement."""
    return 1 / (
        1 / U_f_sus
        + A / ((A * U_fg_b) + (z * P * U_wg_b) + (h * P * U_w) + (c_p * rho * n * V))
    )


def R_f_eff(U, R_si):
    """Function 20 - Effective thermal resistance of floor construction."""
    return 1 / U - R_si


def t_int_m(t_int_ann_ave, t_int_amp, m, tau):
    """Function C.1 - Monthly mean internal temperature for month m."""
    return t_int_ann_ave - t_int_amp * cos(pi * (m - tau) / 6)


def t_e_m(t_e_ann_ave, t_e_amp, m, tau):
    """Function C.2 - Monthly mean external temperature for month m."""
    return t_e_ann_ave - t_e_amp * cos(pi * (m - tau) / 6)


def Phi_m1(
    H_g, H_pi, H_pe, t_int_ann_ave, t_int_amp, t_e_ann_ave, t_e_amp, alfa, beta, tau, m
):
    """
    Function C.3 - Averate heat flow rate for month m.
    Arguments:
    H_g - steady-state ground heat transfer coefficient,
    H_pi -  internal periodic heat transfer coefficient,
    H_pe - external periodic heat transfer coefficient.
    """
    return (
        H_g * (t_int_ann_ave - t_e_ann_ave)
        - H_pi * t_int_amp * cos(pi * (m - tau + alfa) / 6)
        + H_pe * t_e_amp * cos(pi * (m - tau - beta) / 6)
    )


def Phi_m2(U, A, P, Psi_wf, H_pi, H_pe, t_int_ann_ave, t_e_ann_ave, t_int_m, t_e_m):
    """
    Function C.4 - Averate heat flow rate for month m.
    """
    return (
        U * A * (t_int_ann_ave - t_e_ann_ave)
        + P * Psi_wf * (t_int_m - t_e_m)
        - H_pi * (t_int_ann_ave - t_int_m)
        + H_pe * (t_e_ann_ave - t_e_m)
    )


def Phi_s_h(H_g, H_pi, H_pe, t_int_ann_ave, t_int_amp, t_e_ann_ave, t_e_amp, gamma):
    """Function C.5 - Average heat flor rate over heating season."""
    return H_g * (t_int_ann_ave - t_e_ann_ave) - gamma * (
        H_pi * t_int_amp - H_pe * t_e_amp
    )


def gamma(n):
    """Function C.6 - Gamma.
    Arguments:
    n - number of months in the season.
    """
    x = 12 / (n * pi)
    return x * sin(1 / x)


def Phi_s_c(H_g, H_pi, H_pe, t_int_ann_ave, t_int_amp, t_e_ann_ave, t_e_amp, gamma):
    """Function C.7 - Average heat flor rate over cooling season."""
    return H_g * (t_int_ann_ave - t_e_ann_ave) - gamma * (
        H_pi * t_int_amp - H_pe * t_e_amp
    )


def Phi_ann(H_g, t_int_ann_ave, t_e_ann_ave):
    """Function C.8 - Annual average ground heat flow rate."""
    return H_g * (t_int_ann_ave - t_e_ann_ave)


def Phi_max(H_g, H_pe, t_int_ann_ave, t_e_ann_ave, t_e_amp):
    """Function C.9 - Maximum monthly heat flow rate."""
    return H_g * (t_int_ann_ave - t_e_ann_ave) + H_pe * t_e_amp


def H_g_ann_m(Phi_m, t_int_ann_ave, t_e_ann_ave):
    """Function C.10 - Monthly ground heat transfer coefficient."""
    return Phi_m / (t_int_ann_ave - t_e_ann_ave)


def d(R, k):
    """Function D.1 - Equivalent thickness resulting from the edge insulation."""
    return R * k


def R(R_n, d_n, k):
    """Function D.2 - Additional thermal resistance."""
    return R_n - d_n / k


def H_g(A, U, P, Psi_wf, Psi_g_ed):
    """Function D.3 - Steady state ground heat transfer with edge insulation."""
    return A * U + P * (Psi_wf + Psi_g_ed)


def U_fg_sog(U_fg_sog_0, Psi_g_ed, B):
    """Function D.4 - Thermal transmittance of the floor with edge insulation."""
    return U_fg_sog_0 + 2 * Psi_g_ed / B


def Psi_g_ed(k, D, d_f, d):
    """Function D.5 - Linear thermal transmittance for horizontal edge insulation."""
    return -k / pi * (log(D / d_f + 1) - log(D / (d_f + d) + 1))


def Psi_w_f(k, D, d_f, d):
    """Function D.6 - Linear thermal transmittance for vertical edge insulation"""
    return -k / pi * (log(2 * D / d_f + 1) - log(2 * D / (d_f + d) + 1))


def Phi_e(Phi_t, A_e, A_m, b, d_f_tot, B):
    """Function E.1 - Heat flow rate for the edge region."""
    return Phi_t * A_e / (A_m * ((b + d_f_tot) / (0.5 * B + d_f_tot)) + A_e)


def Phi_m(Phi_t, Phi_e):
    """Function E.2 - Heat flow rate for the central region."""
    return Phi_t - Phi_e


def q_e(Phi_e, A_e):
    """Function E.3 - Density of heat flow rate for rooms at the edge of the building."""
    return Phi_e / A_e


def q_m(Phi_m, A_m):
    """Function E.4 - Density of heat flow rate for rooms in the middle of the building."""
    return Phi_m / A_m


def R_vi(U, R_si, R_f, R_g):
    """Function F.1 - Thermal resistance of the virtual layer."""
    return 1 / U - R_si - R_f - R_g


def t_vi_m(t_int_m, Phi_m, P, Psi_wf, t_int_ann_ave, t_e_ann_ave, A, U):
    """Function F.2 - Virtual temperature (approximate)."""
    return t_int_m - (Phi_m - P * Psi_wf * (t_int_ann_ave - t_e_ann_ave)) / (A * U)


def t_vi_t(t_int_m, Phi_t, A, U):
    """Function F.3 - Virtual temperature (numerical)."""
    return t_int_m - Phi_t / (A * U)


def t_us_ann_ave(
    U_f_sus, A, U_g, h, P, U_w, V, c_p, rho, t_ve_ann_ave, t_int_ann_ave, t_e_ann_ave
):
    """Function G.1 - Annual average temperature in underfloor space."""
    x = A * U_f_sus
    y = V * c_p * rho
    z = A * U_g + h * P * U_w
    numerator = x * t_int_ann_ave + y * t_ve_ann_ave + z * t_e_ann_ave
    denominator = x + y + z
    return numerator / denominator


def U_g(U_fg_b, z, P, U_wg_b, A):
    """Function G.2 - Thermal transmitance of the ground."""
    return U_fg_b + z * P * U_wg_b / A


def U_fg_sus_be(
    U_f_sus, A, U_g, h, P, U_w, V, c_p, rho, t_ve_ann_ave, t_int_ann_ave, t_e_ann_ave
):
    """Function G.3 - Thermal transmitance of the floor
    between internal and external environments."""
    x = A * U_g
    y = h * P * U_w
    z = V * c_p * rho
    t = (t_int_ann_ave - t_ve_ann_ave) / (t_int_ann_ave - t_e_ann_ave)
    numerator = x + y + z * t
    denominator = A * U_f_sus + x + y + z
    return U_f_sus * numerator / denominator


def V(epsilon, v, f_w, P):
    """Function G.4 - Ventilation rate."""
    return 0.59 * epsilon * v * f_w * P


def U_fg_sus_in(U_f_sus, U_g, h, U_w, B, V, c_p, rho, A):
    """Function G.5 - Thermal transmitance of the floor for ventilated from inside."""
    z = V * c_p * rho
    return 1 / (1 / U_f_sus + (1 + z / (A * U_f_sus)) / (U_g + 2 * h * U_w / B))


def U_fg_sus_out(U_f_sus, U_g, h, U_w, B, V, c_p, rho, A):
    """Function G.6 - Thermal transmitance of the floor for ventilated from outside."""
    z = V * c_p * rho
    return 1 / (1 / U_f_sus + 1 / (U_g + 2 * h * U_w / B + z / A))


def U_fg_sus_un(U_f_sus, U_g, h, U_w, B):
    """Function G.7 - Thermal transmitance of the floor for unventilated."""
    return 1 / (1 / U_f_sus + 1 / (U_g + 2 * h * U_w / B))


def sigma1(k_g, rho, c):
    """Function H.1 - Periodic penetration depth."""
    return sqrt(3.15 * 10**7 * k_g / (pi * rho * c))


def sigma2(material):
    """Table H.1 - Periodic penetration depth."""
    switcher = {
        "clay": 2.2,
        "silt": 2.2,
        "sand": 3.2,
        "gravel": 3.2,
        "homogenerous rock": 4.2,
    }
    return switcher.get(material.lower())


def H_pi1(A, k_g, d_f, sigma):
    """Function H.2 - Internal periodic heat transfer coefficient
    for slab-on-ground floor: uninsulated, with all-over insulation,
    with edge insulation."""
    return A * k_g / d_f * sqrt(2 / ((1 + sigma / d_f) ** 2 + 1))


def H_pe1(P, k_g, d_f, sigma):
    """Function H.3 - External periodic heat transfer coefficient
    for slab-on-ground floor: uninsulated or with all-over insulation."""
    return 0.37 * P * k_g * log(sigma / d_f + 1)


def H_pe2(P, k_g, d_f, sigma, d, D):
    """Function H.4 - External periodic heat transfer coefficient
    for slab-on-ground floor with horizontal edge insulation."""
    x = 0.37 * P * k_g
    y = e ** (-D / sigma)
    return x * ((1 - y) * log(sigma / (d_f + d) + 1) + y * log(sigma / d_f + 1))


def H_pe3(P, k_g, d_f, sigma, d, D):
    """Function H.5 - External periodic heat transfer coefficient
    for slab-on-ground floor with vertical edge insulation."""
    x = 0.37 * P * k_g
    y = e ** (-2 * D / sigma)
    return x * ((1 - y) * log(sigma / (d_f + d) + 1) + y * log(sigma / d_f + 1))


def H_pi2(A, U_f_sus, k_g, sigma, U_x):
    """Function H.6 - Internal periodic heat transfer coefficient
    for suspended floor."""
