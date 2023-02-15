from pprint import pprint 
from functions import *
from methodology import *

material2 = Material("Generic", 0.6, 1, surface_emissivity=0.90)
materials = [material2]
ConstructionA = Construction("Floor", materials)

# print(ConstructionA.R_c_op)
# print(ConstructionB.R_c_op)

boundary = "ext"
direction = "horizontal"

R_s = SurfaceResistance(boundary=boundary, direction=direction, material=material2)
R_s_c = R_s_c(boundary=boundary, direction=direction)

# print("R_s", R_s.R_s)
# print("R_s_c", R_s_c)

U_test = Transmittance(
    name="Wall U-Value", construction=ConstructionA, direction="horizontal"
)

pprint(U_test)