from iso_13370.methodology import *
from iso_6946.methodology import *
from pprint import pprint

GroundA = Ground("Soil", conductivity=2.0)
MaterialA = Material(name="Concrete", thickness=0.3, conductivity=1.0)
ConstructionA = Construction(name="Slab", materials=MaterialA)

ClassA = SlabOnGroundFloor(
    name="FloorA",
    area=100,
    perimeter=40,
    ground=GroundA,
    construction=ConstructionA,
    d_w_e=0.2,
    R_f_sog=1,
)

# ClassB = SuspendedFloor("FloorA", 100, 40, GroundA)
# ClassC = HeatedBasement("FloorA", 100, 40, GroundA)
# ClassD = UnheatedBasement("FloorA", 100, 40, GroundA)

pprint(ClassA)
# print(ClassB)
# print(ClassC)
# print(ClassD)
