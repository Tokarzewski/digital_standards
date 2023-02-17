from methodology import *

embedded_pipe = EmbeddedPipe(
    name="pipe", external_diameter=0.016, wall_thickness=0.002, conductivity=0.35
)

UFH_A = EmbeddedRadiantSystem(
    name="System A - floor heating",
    system_type="A",
    embedded_pipe=embedded_pipe,
    case_of_application="floor heating",
    W=0.10,
)

UFH_B = EmbeddedRadiantSystem(
    name="System A - wall heating",
    system_type="A",
    embedded_pipe=embedded_pipe,
    case_of_application="wall heating",
    W=0.10,
)

UFH_D = EmbeddedRadiantSystem(
    name="System A - ceiling heating",
    system_type="A",
    embedded_pipe=embedded_pipe,
    case_of_application="ceiling heating",
    W=0.10,
)

for UFH in [UFH_A, UFH_B, UFH_D]:
    print(UFH.name + ":", round(UFH.q, 2), "W/m2")
    # print(UFH)

"""
System A - floor heating: 87.58 W/m2
System A - wall heating: 90.75 W/m2
System A - ceiling heating: 92.83 W/m2
emm why?
"""
