import numpy as np


def Phi_HL_build1(
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


def Phi_HL_i(Phi_T_i, Phi_V_i, Phi_hu_i, Phi_gain_i=0):
    """Function 3 - Design heat load of the heated space."""
    return Phi_T_i + Phi_V_i + Phi_hu_i + Phi_gain_i


def Phi_T_i1(H_T_ie, H_T_ia, H_T_iae, H_T_iaBE, H_T_ig, t_int_i, t_e):
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
    """Function 7 - Heat transfer coefficient to adjacent room,
    adjacent unheated room or adjacent building entity."""
    return A_k * U_k * f_ia_k


def H_T_ig(A_k, U_equiv_k, f_ig_k, f_GW_k, f_tann):
    """Function 8 - Heat transfer coefficient through the ground."""
    return f_tann * A_k * U_equiv_k * f_ig_k * f_GW_k


def f_ix_k(f_1, f_2):
    """Function 9 - Temperature adjustment factor."""
    return f_1 + f_2


def f_1(t_int_i, t_x, t_e):
    """Function 10 - Temperature adjustment factor."""
    return (t_int_i - t_x) / (t_int_i - t_e)


def f_2(t_int_i, t_e, t_star_int_k):
    """Function 11 - Temperature adjustment factor."""
    return (t_star_int_k - t_int_i) / (t_int_i - t_e)


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


def q_v_ATD_50_z(q_v_ATD_design_z, dp_ATD_design_z=4, v_leak_z=0.67):
    """Function 30 - Air volume flow into the ventilation zone (z) through ATDs
    at a pressure difference of 50 Pa."""
    return q_v_ATD_design_z * (50 / dp_ATD_design_z) ** v_leak_z


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
        numerator = [q * t for q, t in zip(q_v_exh_i, t_star_int_i)]
        denominator = sum(q_v_exh_i)
        return numerator / denominator
    else:
        return t_star_int_i


def Phi_hu_i(A_i, phi_hu_i):
    """Function 39 - Simplified method to determine
    the heating-up power of a heated space (i)."""
    return A_i * phi_hu_i


def tau(C_eff, H):
    """Function 40 - Time constant."""
    return C_eff / H


def C_eff(c_eff, V_e):
    """Function 41 - Effective overall thermal storage capacity of the building."""
    return c_eff * V_e


def H_12(H_T_12, H_V_12):
    """Function 42 - Heat transfer coefficient between
    the space 1 and 2 without temperature adjustment."""
    return H_T_12 + H_V_12


def H_T_12(A_k, U_k, dU_TB):
    """Function 43 - Transmission heat transfer coefficient between
    the space 1 and 2 without temperature adjustment."""
    return sum([A * (U + dU) for A, U, dU in zip(A_k, U_k, dU_TB)])


def H_V_12(q_V_12, rho, c_p):
    """Function 44 -  Ventilation heat transfer coefficient between
    the space 1 and 2 without temperature adjustment."""
    return q_V_12 * rho * c_p


def t_e(t_e_0, dt_e_tau):
    """Function 45 - External design temperature for the considered building."""
    return t_e_0 + dt_e_tau


def dt_e(t_e_Ref, G_t_Ref, h_build, h_Ref):
    """Function 46 - External design temperature at the building site."""
    return t_e_Ref + G_t_Ref * (h_build - h_Ref)


def dt_e_tau(k_tau, tau, dt_e_tau_0, dt_e_tau_max, dt_e_tau_min):
    """Function 47 - Temperature correction taking into account the time constant."""
    return max(min(k_tau * tau + dt_e_tau_0, dt_e_tau_max), dt_e_tau_min)


def t_star_int_k(t_int_i, G_t_air_i, h_k, h_occup_i, dt_surf_k):
    """Function 48 - Mean internal surface temperature for the building element (k)."""
    return t_int_i + G_t_air_i * (h_k - h_occup_i) + dt_surf_k


def t_star_int_i(t_int_i, G_t_air_i, h_i, h_occup_i, dt_rad):
    """Function 49 - Mean internal air temperature in high rooms."""
    return t_int_i + G_t_air_i * (h_i / 2 - h_occup_i) + dt_rad


def Phi_HL_i(Phi_T_i, Phi_V_i, Phi_hu_i):
    """Function 50 - Design heat load of a room (i)."""
    return Phi_T_i + Phi_V_i + Phi_hu_i


def Phi_T_i2(A_k, U_k, dU_TB, f_x_k, t_int_i, t_e):
    """Function 51 - Design transmission heat loss of a room (i)."""
    list = [A * (U + dU) * f for A, U, dU, f in zip(A_k, U_k, dU_TB, f_x_k)]
    return sum(list) * (t_int_i - t_e)


def A_k(f_int_ext, A_k_inner):
    """Function 52 - Area of the outer wall from inner wall area."""
    return f_int_ext * A_k_inner


def Phi_V_i3(V_i, n_i, rho, c_p, t_int_i, t_e):
    """Function 53 - Design ventilation heat loss of the room (i)."""
    return V_i * n_i * rho * c_p * (t_int_i - t_e)


def Phi_HL_build2(Phi_T_i, Phi_V_i):
    """Function 54 - Design heat load of a building."""
    return Phi_T_i + Phi_V_i


def Phi_T_build(A_k, U_k, dU_TB, f_x_k, t_int_build, t_e):
    """Function 55 - Design transmission heat loss of a building."""
    list = [A * (U + dU) * f for A, U, dU, f in zip(A_k, U_k, dU_TB, f_x_k)]
    return sum(list) * (t_int_build - t_e)


def Phi_V_i4(V_build, n_build, rho, c_p, t_int_build, t_e):
    """Function 56 - Design ventilation heat loss of a building."""
    return V_build * n_build * rho * c_p * (t_int_build - t_e)


# Annex B - Input data, default values


def dU_TB(criteria1, criteria2):
    """Table B.1 - Blanket additional thermal transmitance for thermal bridges."""
    if criteria1 == "new building":
        if criteria2 == "best practice":
            dU_TB = 0.02
        else:
            dU_TB = 0.05
    else:
        if criteria2 == "internal broken insulation":
            dU_TB = 0.15
        else:
            dU_TB = 0.10
    return dU_TB


f_tann = 1.45


def f_GW(h_GW):
    """Water table correction factor."""
    if h_GW <= 1:
        return 1.15
    else:
        1.00


def c_eff(category):
    """Table B.4 - Volume specific thermal storage capacity."""
    if category in ["medium", "high"]:
        return 50
    else:
        return 15


def q_env_50(air_tightness_class):
    """Table B.6 - Air permeability default values."""
    switcher = {"i": 2, "ii": 3, "iii": 6, "iv": 12, "1": 2, "2": 3, "3": 6, "4": 12}
    return switcher.get(str(air_tightness_class).lower())


dp_ATD_design_z = 4
v_leak_z = 0.67


def f_int_ext(building_element):
    """Table B.10 - Ratio between external and internal surface areas."""
    if building_element.lower() == "vertical external wall" or "external wall":
        return 1.25
    else:
        return 1.00


def U_equiv_k(direction, z, B_prim, U_k, dU_TB):
    """Function E.1 - Equivalent U-value of the building part (k)
    in contact with the ground."""
    if z < 0:
        print("Warning! - The z value is negative.")
        z = 0
        print("The z value was overwritten to z=0.")
    if direction == "downwards":
        a = 0.9671
        b = -7.455
        c = [10.76, 9.773, 0.0265]
        d = -0.0203
        n = [0.5532, 0.6027, -0.9296]
    elif direction == "horizontal":
        a = 0.93328
        b = -2.1552
        c = [0, 1.466]
        d = 0.1006
        n = [0, 0.45325, -1.0068]
    x = b + (c[0] + B_prim) ** n[0] + (c[1] + z) ** n[1] + (c[2] + U_k + dU_TB) ** n[2]
    return a / x + d


def B_prim(A_G, P):
    """Function E.2 - Geometric parameter of the floor slab."""
    if P == 0:
        return 1
    else:
        return 2 * A_G / P
