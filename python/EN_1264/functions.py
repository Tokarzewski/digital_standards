from math import log, sqrt


def deltat_H(t_V, t_R, t_i):
    """Function 1 - Temperature difference
    between heating fluid and room."""
    return t_V - t_R / log((t_V - t_i) / (t_R - t_i))


def q_H(K_H, deltat_H):
    """Function 2 - Specific heating output."""
    return K_H * deltat_H


def R_k_ins(s_ins, k_ins):
    """Function 3 - Thermal resistance of insulation."""
    return s_ins / k_ins


def s_ins(s_h, T, D, s_l):
    """Function 4 - Thickness of thermal insulation."""
    return (s_h * (T - D) + s_l * D) / T


def q_des1(Q_N_f, A_F):
    """Function 5 - Design specific thermal output."""
    return Q_N_f / A_F


def Q_F(q, A_F):
    """Function 6 - Design thermal output."""
    return q * A_F


def q_des2(A_R, A_F, A_A, q_R, q_A):
    """Function 7 - Specific thermal output with peripherals."""
    return A_R * q_R / A_F + A_A * q_A / A_F


def deltat_V_des1(deltat_H_des, sigma):
    """Function 8 - Design temperature difference between flow
    of heating fluid and room of heating systems,
    determined by room with q_max."""
    return deltat_H_des + sigma / 2


def deltat_V_des2(deltat_H_des, sigma):
    """Function 9 - Design temperature difference between flow
    of heating fluid and room of floor heating systems,
    determined by room with q_max."""
    return deltat_H_des + sigma / 2 + sigma ^ 2 / (12 * deltat_H_des)


def deltat_V_des(deltat_H, deltat_H_des, sigma):
    """Design temperature difference between flow
    of heating fluid and room of floor heating systems,
    determined by room with q_max."""
    if sigma / deltat_H > 0.5:
        # Function 9
        return deltat_V_des2(deltat_H_des, sigma)
    else:
        # Function 8
        return deltat_V_des1(deltat_H_des, sigma)


def deltat_V(deltat_V_des, t_i):
    """Heating design inlet temperature."""
    return deltat_V_des + t_i


def sigma_j1(deltat_V_des, deltat_H_j):
    """Function 10 - Design temperature drop of fluid in room."""
    return 2 * (deltat_V_des - deltat_H_j)


def sigma_j2(deltat_V_des, deltat_H_j):
    """Function 11 - Design temperature drop of fluid in room."""
    return (
        3
        * deltat_H_j
        * (sqrt(1 + (4 * deltat_V_des - deltat_H_j) / 3 * deltat_H_j) - 1)
    )


def sigma_j(sigma, t_H_j, deltat_V_des, deltat_H_j):
    """Design temperature drop of fluid in room."""
    if sigma / t_H_j > 0.5:
        # Function 11
        return sigma_j2(deltat_V_des, deltat_H_j)
    else:
        # Function 10
        return sigma_j1(deltat_V_des, deltat_H_j)


def Q_out(Q_N_f, Q_F):
    """Function 12 - Additional required thermal output."""
    return Q_N_f - Q_F


def m(q, A_F, sigma, t_i, t_u, R_o, R_u, c_W=4190):
    """Function 13 - Design heating flow rate."""
    return (A_F * q) / (sigma * c_W) * (1 + R_o / R_u + (t_i - t_u) / (q * R_u))


def R_o(R_k_B, s_u, k_u, alfa=10.8):
    """Function 14 - Upwards partial heat transmission
    resistance of the floor structure."""
    return 1 / alfa + R_k_B + s_u / k_u


def R_u(R_k_ins, R_k_construction, R_k_plaster, R_alfa):
    """Function 15 - Downwards partial heat transmission
    resistance of the floor structure."""
    return R_k_ins + R_k_construction + R_k_plaster + R_alfa


def alfa(process="heating", direction="upwards"):
    """EN 1264:5 Table A.1 - Thermal transfer resistance."""
    if process == "heating":
        switcher = {"upwards": 10.8, "horizontal": 8, "downwards": 6.5}
        return switcher.get(direction.lower())
    else:
        # process == "cooling"
        switcher = {"upwards": 6.5, "horizontal": 8, "downwards": 10.8}
        return switcher.get(direction.lower())


def deltat_C(t_C_out, t_C_in, t_i=26):
    """Function 16 - Temperature difference
    between heating fluid and room."""
    return t_C_out - t_C_in / log((t_C_in - t_i) / (t_C_out - t_i))


def q_C(K_H, deltat_C):
    """Function 2 - Specific cooling output."""
    return K_H * deltat_C


def deltat_C_in_des1(delta_t_C_des, sigma_C, deltat_C_N):
    """Function 18 - Design temperature difference between cooling
    fluid and room of system, determined by room with q_max."""
    if delta_t_C_des <= deltat_C_N:
        return delta_t_C_des + sigma_C / 2


def deltat_C_in_des2(delta_t_C_des, delta_t_C_N, sigma_C):
    """Function 19 - Check if design temperature difference between room
    temperature and inlet temperature of the cooling fluid is within range."""
    return deltat_C_in_des1(delta_t_C_des, sigma_C) <= delta_t_C_N + sigma_C / 2


def t_C_in_des(t_i, deltat_C_in_des):
    """Function 20 - Cooling design inlet temperature."""
    return t_i - deltat_C_in_des


def delta_t_C_in_des2(t_i, deltat_C_in_des, deltat_C_N, sigma_C):
    """Function 21 - Check if cooling design
    inlet temperature is within range."""
    t_C_in_des = t_C_in_des(t_i, deltat_C_in_des)
    return t_C_in_des >= t_i - deltat_C_N + sigma_C / 2


def deltat_C_des(deltat_C_in_des, sigma_C):
    """Function 22 - Cooling design average temperature
    difference between fluid and room of cooling system,
    determined by room with q_max."""
    return deltat_C_in_des - sigma_C / 2 - sigma_C ^ 2 / (
        12 * (deltat_C_in_des - sigma_C / 2)
    )


def m(q_C_des, A_F, sigma_C, t_i, t_u, R_o, R_u, c_W=4190):
    """Function 23 - Cooling design flow rate."""
    return (
        (A_F * q_C_des)
        / (sigma_C * c_W)
        * (1 + R_o / R_u + (t_u - t_i) / (q_C_des * R_u))
    )
