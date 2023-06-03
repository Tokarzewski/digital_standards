from methodology import *

embedded_pipe = EmbeddedPipe(
    name="pipe", external_diameter=0.016, wall_thickness=0.002, conductivity=0.35
)

case_of_application="floor heating"
W=0.10

UFH_A = EmbeddedRadiantSystem(
    name="System A",
    system_type="A",
    embedded_pipe=embedded_pipe,
    case_of_application=case_of_application,
    W=W
)

UFH_B = EmbeddedRadiantSystem(
    name="System B",
    system_type="B",
    embedded_pipe=embedded_pipe,
    case_of_application=case_of_application,
    W=W,
)

UFH_D = EmbeddedRadiantSystem(
    name="System D",
    system_type="D",
    embedded_pipe=embedded_pipe,
    case_of_application=case_of_application,
    W=W,
)

for UFH in [UFH_A, UFH_B, UFH_D]:
    print(UFH.name + ":", round(UFH.q, 2), "W/m2")

"""
System A: 68.59 W/m2
System B: 69.30 W/m2
System D: 77.58 W/m2
"""
