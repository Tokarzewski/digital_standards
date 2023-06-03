from methodology import *
from functions import *

Wood = Material(name="Wood", thickness=0.05, conductivity=0.9)
Concrete = Material(name="Concrete", thickness=0.3, conductivity=1.0)
ExternalWall = Construction(name="ExternalWall", materials=[Wood, Concrete])

boundary = "ext"
direction = "horizontal"

R_s_c = R_s_c(boundary=boundary, direction=direction)

U_test = Transmittance(
    name="TExternalWall", construction=ExternalWall, direction="horizontal"
)

print("External Wall")
print("R:", ExternalWall.R)
print("U:", round(U_test.U, 2))
print("R_se:", U_test.R_se)
print("R_se_c:", R_s_c)