from en_12831.functions import *

Phi_T_ie = [1, 1]
Phi_T_iae = [1, 0]
Phi_T_ig = [-2, 2]
Phi_V_build = 1
Phi_hu_i = [0, 0]
Phi_gain_i = [0, 0]

Phi_HL_build_list = Phi_HL_build(
    Phi_T_ie=Phi_T_ie,
    Phi_T_iae=Phi_T_iae,
    Phi_T_ig=Phi_T_ig,
    Phi_V_build=Phi_V_build,
    Phi_hu_i=Phi_hu_i,
    Phi_gain_i=Phi_gain_i,
)

# print(Phi_HL_build(2, 1, 0, 1, 0, 0))
# print(Phi_HL_build_list)
print(Phi_V_z(1.2, 1.005, [0.5, 1], [0.5, 1], [20, 20], -20))
