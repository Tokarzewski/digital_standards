from iso_11855.methodology import *

embedded_pipe = EmbeddedPipe(
    name="pipe", external_diameter=0.016, wall_thickness=0.002, conductivity=0.35
)

UFH_A = EmbeddedRadiantSystem(
    name="System A", system_type="A", embedded_pipe=embedded_pipe
)

UFH_B = EmbeddedRadiantSystem(
    name="System B", system_type="B", embedded_pipe=embedded_pipe
)

UFH_D = EmbeddedRadiantSystem(
    name="System D", system_type="D", embedded_pipe=embedded_pipe
)

for UFH in [UFH_A, UFH_B, UFH_D]:
    print(UFH.name + ":", round(UFH.q, 2), "W/m2")
    # print(UFH)

"""
System A: 88.12 W/m2
System B: 91.41 W/m2
System D: 99.86 W/m2
"""
