import numpy as np


def Q_W_b_i(Q_W_b_t):
    """Function 1 - Cumulative energy need for water heating."""
    return sum(Q_W_b_t)


def Q_W_b_t1(V_t, rho_w, c_w, t_w_draw, t_w_c):
    """Function 2A - Energy need for DHW in one minute."""
    return V_t * rho_w * c_w * (t_w_draw - t_w_c) / 3600


def Q_W_b_t2(Q_W_b, x_h):
    """Function 2B - Energy need for DHW in one minute."""
    return Q_W_b * x_h / 3600


def density_of_water(water_temperature):
    """B.1 Density of water [kg/m3]"""
    return 1000 - 0.005 * (water_temperature - 4) ** 2
