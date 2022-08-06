from en_12831.methodology import *
from en_12831.functions import *
from iso_6946.methodology import *
from pprint import pprint

winter_design_day = DesignDay("Trzecia strefa klimatyczna", -20, 7.6)

sz1 = Surface('SZ1',100,40,'horizontal')

material1 = Material("Wood", 0.06, 1.0, 0.9)
material2 = Material("EPS", 0.1, 0.004)
material3 = Material("Concrete", 0.3, 1.0)
materials = [material1, material2, material3]
construction1 = Construction("Floor", materials)

BE1 = BuildingElement('BE1', construction1, 'exterior', None, sz1)
room1 = Room('room1', 100, 4, 400, BE1)

H_T_ie = H_T_ix(DesignDay = winter_design_day, 
                t_int_i = 20, 
                BuildingElement = BE1)

print(H_T_ie)

Phi_T_i = round(H_T_ie[1] * (20 - (-20)),0)

print(f'Phi_T_i {Phi_T_i} W')