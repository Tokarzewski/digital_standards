from methodology import *


material1 = Material("Slab", 0.06, 1.0)
material2 = Material("EPS", 0.1, 0.004)
material3 = Material("Concrete", 0.3, 1.0)

materials = [material1, material2, material3]

construction1 = Construction("Floor", materials)

print(construction1)