import iso_13370.functions as f
from iso_13370.methodology import (
    Ground,
    SlabOnGroundFloor,
    SuspendedFloor,
    BasementFloor,
)
from iso_6946.methodology import Construction, Material

GroundA = Ground("Soil", k_g=2.0)
MaterialA = Material(name="Concrete", d=0.3, k=1.0)
ConstructionA = Construction(name="Slab", materials=MaterialA)

ClassA = SlabOnGroundFloor("FloorA", 100, 40, GroundA, ConstructionA)
ClassB = SuspendedFloor("FloorA", 100, 40, GroundA)
ClassC = BasementFloor("FloorA", 100, 40, GroundA)

print(ClassA)
print(ClassB)
print(ClassC)
