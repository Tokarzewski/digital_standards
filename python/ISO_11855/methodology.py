from functions import *

# For system types A, C, H, I, J

t_i = 20  # Design indoor temperature [*C]
t_V = 40  # Supply temperature of heating or cooling medium [*C]
t_R = 35  # Return temperature of heating or cooling medium [*C]

D = 0.016  # External diameter of pipe, including sheating where used
W = 0.10  # Pipe spacing [m]
s_u = 0.02  # Thickness of layer above the pipe [m]
R_k_B = 0.05  # Thermal resistance of the floor covering [m2K/W]
k_E = 1  # Thermal conductivity of screed [W/mK]

s_WL = 0.002 # Thickness of the heat conducting material [m]
k_WL = 0.35 # thermal conductivity of the heat conducting material [W/mK]
L_WL = 1 # Width of heat conducting device

alfa = alfa("Floor heating")
m_W = m_W1(W)
deltat_H = deltat_H(t_V, t_R, t_i)
# deltat_H = 1 # for calculating K_H

if W <= 0.375:
    q = q6(
        a_B = a_B1(alfa, k_E, R_k_B), 
        a_W = a_W1(R_k_B), 
        a_U = a_U1(R_k_B, W), 
        a_D = a_D(R_k_B, W), 
        m_W = m_W, 
        m_U = m_U(s_u), 
        m_D = m_D(D), 
        deltat_H = deltat_H
        )
else:
    q = q6(
        a_B = a_B1(alfa, k_E, R_k_B), 
        a_W = a_W1(R_k_B), 
        a_U = a_U1(R_k_B, W=0.375), 
        a_D = a_D(R_k_B, W=0.375), 
        m_W = m_W1(W=0.375), 
        m_U = m_U(s_u), 
        m_D = m_D(D), 
        deltat_H = deltat_H
        )
    q = q8(q_0375=q, W=W)

print("q: ", round(q, 2), "W/m2")

# For system type B

a_U = a_U2(alfa, s_u, k_E)
a_W = a_W2(s_u, k_E)
b_u = b_u(W)
a_K = a_K(W)
K_WL = K_WL(s_WL, k_WL, b_u, s_u, k_E)

if K_WL < 0.5:
    a_WL = a_WL2(K_WL, W, D)
else:
    a_WL = a_WL3(K_WL, W, D)
if L_WL < W:
    a_0 = a_WL2(0, W, D)
    a_WL = a_WL1(a_WL, a_0, L_WL, W)

a_B = a_B2(
    a_U = a_U, 
    a_W = a_W, 
    m_W = m_W, 
    a_WL = a_WL, 
    a_K = a_K, 
    R_k_B = R_k_B, 
    W = W
    )

q = q9(
    a_B = a_B, 
    a_W = a_W, 
    a_U = a_U, 
    a_WL = a_WL, 
    a_K = a_K, 
    m_W = m_W, 
    deltat_H = deltat_H
    )

print("q: ", round(q, 2), "W/m2")

# For system type D