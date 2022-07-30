from logging import exception
from re import X
import numpy as np
from math import log, sqrt


def Phi_HL_build(
    Phi_T_ie, Phi_T_iae, Phi_T_ig, Phi_V_build, Phi_hu_i=[0, 0], Phi_gain_i=[0, 0]
):
    """Function 1 - Design heat load of the building."""
    if np.iterable(Phi_T_ie):
        return (
            np.sum([Phi_T_ie, Phi_T_iae, Phi_T_ig, Phi_hu_i, Phi_gain_i]) + Phi_V_build
        )
    else:
        if np.iterable(Phi_hu_i):
            Phi_hu_i, Phi_gain_i = 0, 0
        return Phi_T_ie + Phi_T_iae + Phi_T_ig + Phi_V_build + Phi_hu_i + Phi_gain_i


def Phi_HL_BE(
    Phi_T_ie,
    Phi_T_iae,
    Phi_T_iaBE,
    Phi_T_ig,
    Phi_V_BE,
    Phi_hu_i=[0, 0],
    Phi_gain_i=[0, 0],
):
    """Function 2 - Design heat load of the building entity."""
    if np.iterable(Phi_T_ie):
        return np.sum(
            [Phi_T_ie, Phi_T_iae, Phi_T_iaBE, Phi_T_ig, Phi_V_BE, Phi_hu_i, Phi_gain_i]
        )
    else:
        if np.iterable(Phi_hu_i):
            Phi_hu_i, Phi_gain_i = 0, 0
        return (
            Phi_T_ie
            + Phi_T_iae
            + Phi_T_iaBE
            + Phi_T_ig
            + Phi_V_BE
            + Phi_hu_i
            + Phi_gain_i
        )


def Phi_HL_i(Phi_T_i, Phi_V_i, Phi_hu_i, Phi_gain_i):
    """Function 3 - Design heat load of the heated space."""
    return Phi_T_i + Phi_V_i + Phi_hu_i + Phi_gain_i


def Phi_T_i(H_T_ie, H_T_ia, H_T_iae, H_T_iaBE, H_T_ig, t_int_i, t_e):
    """Function 4 - Design transmission heat loss of the heated space."""
    return (H_T_ie + H_T_ia + H_T_iae + H_T_iaBE + H_T_ig) * (t_int_i - t_e)


def Phi_T_ix(H_T_ix, t_int_i, t_e):
    """Function 5 - Design transmission heat loss from the heated space (i)
    to another space (x)"""
    return H_T_ix * (t_int_i - t_e)


def H_T_ie(A_k, U_k, dU_TB, f_U_k, f_ie_k):
    """Function 6 - Heat transfer coefficient directly to the exterior."""
    return A_k * (U_k + dU_TB) * f_U_k * f_ie_k


def H_T_ia(A_k, U_k, f_ia_k):
    """Function 7 - Heat transfer coefficient to adjacent spaces."""
    return A_k * U_k * f_ia_k


def H_T_ig(A_k, U_equiv_k, f_ig_k, f_GW_k, f_tann):
    """Function 8 - Heat transfer coefficient through the ground."""
    return f_tann * A_k * U_equiv_k * f_ig_k * f_GW_k


def f_ix_k(t_int_i, t_x, t_e, t_star_int_k):
    """Function 9 - Temperature adjustment factor."""
    f1 = (t_int_i - t_x) / (t_int_i - t_e)  # Function 10
    f2 = (t_star_int_k - t_int_i) / (t_int_i - t_e)  # Function 11
    return f1 + f2


def Phi_V_build1(Phi_V_z):
    """Function 12 - Ventilation heat loss of the building."""
    if np.iterable(Phi_V_z):
        return sum(Phi_V_z)
    return Phi_V_z


def Phi_V_z1(Phi_V_i):
    """Function 13 - Ventilation heat loss of the zone."""
    if np.iterable(Phi_V_i):
        return sum(Phi_V_i)
    return Phi_V_i


def Phi_V_i1(rho, c_p, q_v_min_i, t_int_i, t_e):
    """Function 14 - Ventilation heat loss of the room."""
    return rho * c_p * q_v_min_i * (t_int_i - t_e)


def Phi_V_build2(Phi_V_z):
    """Function 15 - Ventilation heat loss of the building."""
    if np.iterable(Phi_V_z):
        return sum(Phi_V_z)
    return Phi_V_z


def Phi_V_z2(Phi_V_i):
    """Function 16 - Ventilation heat loss of the zone."""
    if np.iterable(Phi_V_i):
        return sum(Phi_V_i)
    return Phi_V_i


def Phi_V_i2(
    rho,
    c_p,
    q_v_env_i,
    q_v_open_i,
    q_v_min_i,
    q_v_techn_i,
    t_star_int_i,
    t_e,
    q_v_sup_i,
    t_rec_z,
    q_v_transfer_ij,
    t_transfer_ij,
):
    """Function 17 - Ventilation heat loss of the room."""
    q_max = max(q_v_env_i + q_v_open_i, q_v_min_i - q_v_techn_i)
    q_sum = (
        q_max * (t_star_int_i - t_e)
        + q_v_sup_i * (t_star_int_i - t_rec_z)
        + q_v_transfer_ij * (t_star_int_i - t_transfer_ij)
    )
    return rho * c_p * q_sum


def q_v_env_i(q_v_inf_add_z, q_v_env_z, q_v_leak_ATD_i, f_dir):
    """Function 18 - External air volume flow into the room (i) through the building envelope."""
    return (
        q_v_inf_add_z / q_v_env_z * max(q_v_env_z, q_v_leak_ATD_i * f_dir)
        + q_v_env_z
        - q_v_inf_add_z * q_v_leak_ATD_i / q_v_env_z
    )


def q_v_leak_ATD_i(
    q_v_leak_z, A_env_i, A_env_z, q_v_ATD_z, q_v_ATD_design_i, q_v_ATD_design_z
):
    """Function 19 - External air volume flow into the room (i) through leakages and ATDs."""
    return (
        q_v_leak_z * A_env_i / A_env_z + q_v_ATD_z * q_v_ATD_design_i / q_v_ATD_design_z
    )


def q_v_leak_z(a_ATD_z, q_v_env_z):
    """Function 20 - External air volume flow into the ventilation zone (z) through leakages."""
    return (1 - a_ATD_z) * q_v_env_z


def q_v_ATD_z(a_ATD_z, q_v_env_z):
    """Function 21 - External air volume flow into the zone (z) through ATDs."""
    return a_ATD_z * q_v_env_z


def a_ATD_z(q_v_ATD_50_z, q_env_50, A_env_z):
    """Function 22 - The ATD authority based on the design of
    the externally mounted air transfer devices."""
    return q_v_ATD_50_z / (q_v_ATD_50_z + q_env_50 * A_env_z)


def q_v_techn_i(q_v_sup_i, q_v_transfer_ij, q_v_exh_i, q_v_comb_i):
    """Function 23 - Technical air volume flow into the room (i)."""
    return max(q_v_sup_i + q_v_transfer_ij, q_v_exh_i + q_v_comb_i)


def q_v_env_z(q_v_exh_z, q_v_comb_z, q_v_sup_z, q_v_inf_add_z):
    """Function 24 - External air volume flow into the ventilation zone (z)
    through the building envelope"""
    return max(q_v_exh_z + q_v_comb_z - q_v_sup_z, 0) + q_v_inf_add_z


# Functions 25, 26, 27 are just the sum functions


def q_v_inf_add_z(q_env_50, A_env_z, q_v_ATD_50_z, f_qv_z, f_e_z):
    """Function 28 - Air volume flow through additonal
    infiltration into the zone (z)."""
    return (q_env_50 * A_env_z + q_v_ATD_50_z) * f_qv_z * f_e_z


def f_e_z(
    f_fac_z, f_qv_z, q_v_exh_z, q_v_comb_z, q_v_sup_z, q_env_50, A_env_z, q_v_ATD_50_z
):
    """Function 29 - Adjustement factor taking into account the additional
    pressure difference due to unbalanced ventilation."""
    x = (q_v_exh_z + q_v_comb_z - q_v_sup_z) / (q_env_50 * A_env_z + q_v_ATD_50_z)
    return 1 / ((1 + f_fac_z / f_qv_z) * x**2)


def q_v_ATD_50_z(q_v_ATD_design_z, dp_design_z, v_leak_z):
    """Function 30 - Air volume flow into the ventilation zone (z) through ATDs
    at a pressure difference of 50 Pa."""
    return q_v_ATD_design_z * (50 / dp_design_z) ** v_leak_z


def q_env_50(n_50, V_build, A_env_build):
    """Function 31 - Air permeability at 50 Pa."""
    return n_50 * V_build / A_env_build


def n_50(n_50_measure, A_small_open, V_build):
    """Function 32 - Air change rate at 50 Pa."""
    return n_50_measure + 2 * A_small_open / V_build


def q_v_min_i(n_min_i, V_i):
    """Function 33 - Minimum air volume flow."""
    return n_min_i * V_i


def A_env(A_fac, A_roof, A_bottom):
    """Functions 34, 35, 36 - Envelope surfaces of building, zone or room."""
    return A_fac + A_roof + A_bottom


def t_rec_z(t_e_0, eta_rec_z, t_exh_z):
    """Function 37 - Temperature of the supply air into the zone (z) after passing 
    heat recovery and, if any, passive preheating; without active preheating."""
    return t_e_0 + eta_rec_z * (t_exh_z - t_e_0)


def t_exh_z(q_v_exh_i, t_star_int_i):
    """Function 38 - Temperature of the exhaust air from the zone (z)."""
    if np.iterable(q_v_exh_i):
        numerator = [
            q_v_exh_i * t_star_int_i
            for q_v_exh_i, t_star_int_i in zip(q_v_exh_i, t_star_int_i)
        ]
        denominator = sum(q_v_exh_i)
        return numerator / denominator
    else:
        return t_star_int_i
