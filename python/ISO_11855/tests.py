from methodology import *
from functions import *

embedded_pipe = EmbeddedPipe(name="pipe", d_a=0.016, s_R=0.002, k_R=0.35)

UFH_A = EmbeddedRadiantSystem(name="System A", system_type="A", embedded_pipe=embedded_pipe)
UFH_B = EmbeddedRadiantSystem(name="System B", system_type="B", embedded_pipe=embedded_pipe)
UFH_D = EmbeddedRadiantSystem(name="System D", system_type="D", embedded_pipe=embedded_pipe)

for UFH in [UFH_A, UFH_B, UFH_D]:
    print(UFH.name + ":", round(UFH.q, 2), "W/m2")
    #print(UFH)

"""
A 88.89 W/m2
B 80.75 W/m2
D 102.98 W/m2
"""
