from iso_6946.methodology import *


material1 = Material("Slab", 0.06, 1.0)
material2 = Material("EPS", 0.1, 0.004)
material3 = Material("Concrete", 0.3, 1.0)

materials = [material1, material2, material3]

construction1 = Construction("Floor", materials)

print(construction1)


MaterialA = Material(name="Concrete", d=0.3, k=1.0)
MaterialB = Material(name="Concrete", d=0.3, k=1.0)
ConstructionA = Construction(name="Slab", materials=[MaterialA, MaterialB])