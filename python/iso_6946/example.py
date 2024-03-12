from methodology import *
from functions import *

Wood = Material(name="Wood", thickness=0.05, conductivity=0.9)
Concrete = Material(name="Concrete", thickness=0.3, conductivity=1.0)
ExternalWall = Construction(name="ExternalWall", materials=[Wood, Concrete])
InternalFloor = Construction(name="InternalFloor", materials=[Wood, Concrete])

boundary = "ext"
direction = "horizontal"

#R_s_c = R_s_c(boundary=boundary, direction=direction)

U_EW = Transmittance(
    name="ExternalWall", construction=ExternalWall, direction="horizontal"
)
U_IF = Transmittance(
    name="InternalFloor", construction=InternalFloor, direction="upwards"
)

print("External Wall")
print("R:", ExternalWall.R)
print("R_se:", U_EW.R_se)