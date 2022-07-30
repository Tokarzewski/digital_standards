from iso_6946.methodology import *
from iso_6946.functions import *
from pprint import pprint

material1 = Material("Wood", 0.06, 1.0, 0.9)
material2 = Material("EPS", 0.1, 0.004)
material3 = Material("Concrete", 0.3, 1.0)
materials = [material1, material2, material3]
ConstructionA = Construction("Floor", materials)

MaterialA = Material(name="Wood", thickness=0.05, conductivity=0.9)
MaterialB = Material(name="Concrete", thickness=0.3, conductivity=1.0)
ConstructionB = Construction(name="Wall", materials=[MaterialA, MaterialB])

# print(ConstructionA.R_c_op)
# print(ConstructionB.R_c_op)

boundary = "ext"
direction = "horizontal"

R_s = SurfaceResistance(boundary=boundary, direction=direction, material=material1)
R_s_c = R_s_c(boundary=boundary, direction=direction)

# print("R_s", R_s.R_s)
# print("R_s_c", R_s_c)

U_value_test = Transmittance(
    name="Wall U-Value", construction=ConstructionB, direction="horizontal"
)

pprint(U_value_test)
