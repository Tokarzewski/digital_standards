from iso_6946.functions import *

print("R_tot =", R_tot1(0.17, [2, 0], 0.04))
print("R_tot =", R_tot1(0.17, 2, 0.04))

for direction in ["upwards", "horizontal", "downwards"]:
    print(direction, h_ci(direction))




