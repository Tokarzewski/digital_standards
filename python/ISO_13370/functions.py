from math import log, cos, sin, pi


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


def H_g_H_adj(XYZ):
    """Function C.11 - Seasonal heat transfer coefficient adjusted
    to the average temperature difference over the heating season."""
    return XYZ


def H_g_C_adj(XYZ):
    """Function C.12 - Seasonal heat transfer coefficient adjusted
    to the average temperature difference over the cooling season."""
    return XYZ


def Q_1(Q_m):
    """Function C.13 - Total heat transfer to ground during season."""
    return sum(Q_m)


def Q_m(N_m, Phi_m):
    """Function C.14 - Total heat transfer to ground in month."""
    return 86400 * N_m * Phi_m


def Q_2(N, Phi):
    """Function C.15 - Total heat trasnfer to ground during season."""
    return 86400 * N * Phi
