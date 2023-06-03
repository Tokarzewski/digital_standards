from methodology import *
from functions import *
from pprint import pprint

Wood = Material(name="Wood", thickness=0.05, conductivity=0.9)
Concrete = Material(name="Concrete", thickness=0.3, conductivity=1.0)
ExternalWall = Construction(name="ExternalWall", materials=[Wood, Concrete])

# print(ConstructionA.R_c_op)
# print(ConstructionB.R_c_op)

boundary = "ext"
direction = "horizontal"

R_s_c = R_s_c(boundary=boundary, direction=direction)

# print("R_s", R_s.R_s)
# print("R_s_c", R_s_c)

U_test = Transmittance(
    name="TExternalWall", construction=ExternalWall, direction="horizontal"
)

print("U:", round(U_test.U, 2))
print("R_s:", U_test.R_se)
print("R_s_c:", R_s_c)

pprint(U_test)