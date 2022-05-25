from methodology import *
from functions import *

embedded_pipe = EmbeddedPipe()

UFH_A = EmbeddedRadiantSystem(system_type="A", embedded_pipe=embedded_pipe)
UFH_B = EmbeddedRadiantSystem(system_type="B", embedded_pipe=embedded_pipe)
UFH_D = EmbeddedRadiantSystem(system_type="D", embedded_pipe=embedded_pipe)

for UFH in [UFH_A, UFH_B, UFH_D]:
    print(UFH.system_type, round(UFH.q, 2), "W/m2")
    # print(UFH)

"""
A 88.89 W/m2
B 80.75 W/m2
D 102.98 W/m2
"""
