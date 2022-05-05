from math import log, sqrt, prod

# ISO 11855-2 FUNCTIONS


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


def K_H(a_i, m_i, s_u, s_u_star, lambda_E):
    """Function A.8 - Heat transfer coefficient."""
    return 1 / (1 / power_product(a_i, m_i) + (s_u - s_u_star) / lambda_E)


def q7(K_H, deltat_H):
    """Function A.9 - Heat flux."""
    return K_H * deltat_H


def q8(q, W):
    """Function A.10 - Heat flux for pipe spacing W > 0.375 m."""
    return q * 0.375 / W


def q9(B, a_B, a_W, a_U, a_WL, a_K, m_W, deltat_H):
    """Function A.11 - Heat flux for system types B."""
    a_i = [a_B, a_W, a_U, a_WL, a_K]
    m_i = [1, m_W, 1, 1, 1]
    return q5(B, a_i, m_i, deltat_H)


def a_B1(B, a_U, a_W, m_W, a_WL, a_K, R_lambda_B, W):
    """Function A.12 - Surface covering factor for function A.11."""
    return 1 / (
        1 + B * a_U * a_W**m_W * a_WL * a_K * R_lambda_B * (1 + 0.44 * sqrt(W))
    )

def a_U(alfa, ):
    """Function A.13 - Covering factor for function A.11."""
    return 

# ISO 11855-3 FUNCTIONS
