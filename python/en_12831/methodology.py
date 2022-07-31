from iso_6946.methodology import Construction, Transmittance
import en_12831.functions as f
from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class DesignDay:
    name: str
    external_design_temperature: float
    annual_mean_external_temperature: float


@dataclass
class Surface:
    name: str
    area: float
    perimeter: float
    direction: str


@dataclass
class FloorSlab:
    name: str
    surface: Surface
    exposed_perimeter: float
    depth_below_ground_level: float


@dataclass
class BuildingElement:
    name: str
    #type: str
    construction: Construction
    room_name: str
    outside_boundary_condition: str
    outside_boundary_condition_object: Any
    surface: Surface
    transmittance: Transmittance = field(init=False)
    additional_thermal_transmittance: float = 0.0
    # openings: Window, Door, Hole, ATD

    H_T_ix: float = field(init=False)

    def __post_init__(self) -> None:
        self.transmittance = Transmittance(
            name=self.name,
            construction=self.construction,
            direction=self.surface.direction,
        )
        if self.outside_boundary_condition in [
            "exterior",
            "adjacent room",
            "adjacent unheated room",
            "adjacent building entity",
            "ground",
        ]:
            self.H_T_ix = H_T_ix(self)


def H_T_ix(DesignDay, Room, BuildingElement):
    """Transmission heat transfer coefficient from the room (i) either to:
    exterior in accordance with 6.3.2.2,
    adjacent room in accordance with 6.3.2.3 (1)
    unheated room in accordance with 6.3.2.3 (3)/(4)
    adjacent building entity in accordance with 6.3.2.3 (2)
    ground in accordance with 6.3.2.4"""

    type = BuildingElement.type
    A_k = BuildingElement.surface.area
    U_k = BuildingElement.transmittance.U
    dU_TB = BuildingElement.additional_thermal_transmittance

    t_e = DesignDay.external_design_temperature
    t_int_i = Room.t_int_i
    t_star_int_k = t_int_i  # XYZ limitation - only for rooms with h < 4m

    if type == "exterior":
        f_1 = 1
        f_2 = f.f_2(t_int_i=t_int_i, t_e=t_e, t_star_int_k=t_star_int_k)
        f_ie_k = f.f_ix_k(f_1, f_2)
        f_U_k = 1
        return f.H_T_ie(A_k=A_k, U_k=U_k, dU_TB=dU_TB, f_U_k=f_U_k, f_ie_k=f_ie_k)

    if type in ["adjacent room", "adjacent unheated room", "adjacent building entity"]:
        t_x = BuildingElement.outside_boundary_condition_object.t_int_i
        f_1 = f.f_1(t_int_i, t_x=t_x, t_e=t_e)
        f_2 = f.f_2(t_int_i, t_e=t_e, t_star_int_k=t_star_int_k)
        f_ia_k = f.f_ix_k(f_1, f_2)

        return f.H_T_ia(A_k=A_k, U_k=U_k, f_ia_k=f_ia_k)

    if type == "ground":
        direction = BuildingElement.surface.direction
        floor_slab = BuildingElement.outside_boundary_condition_object
        z = floor_slab.depth_below_ground_level
        P = floor_slab.exposed_perimeter
        B_prim = f.B_prim(A_G=A_k, P=P)
        U_equiv_k = f.U_equiv_k(direction, z=z, B_prim=B_prim, U_k=U_k, dU_TB=dU_TB)

        t_x = DesignDay.annual_mean_external_temperature
        f_2 = f.f_2(t_int_i, t_e, t_star_int_k)
        f_ig_k = f.f_ix_k(f_1, f_2)
        f_GW_k = f.f_GW(Room.height)
        return f.H_T_ig(A_k, U_equiv_k, f_ig_k=f_ig_k, f_GW_k=f_GW_k, f_tann=f.f_tann)


@dataclass
class Room:
    name: str
    area: float
    height: float
    volume: float
    building_elements: List[BuildingElement] or BuildingElement

    H_T_ie: float = field(init=False)
    H_T_ia: float = field(init=False)
    H_T_iae: float = field(init=False)
    H_T_iaBE: float = field(init=False)
    H_T_ig: float = field(init=False)

    t_int_i: float = field(init=False)
    t_e: float = field(init=False)

    Phi_T_i: float = field(init=False)
    Phi_V_i: float = field(init=False)
    Phi_hu_i: float = field(init=False)
    Phi_gain_i: float = field(init=False)
    Phi_HL_i: float = field(init=False)

    def __post_init__(self) -> None:
        self.H_T_ie = f.H_T_ie(self.A_k, self.U_k, self.dU_TB, self.f_U_k, self.f_ie_k)
        self.Phi_T_i = f.Phi_T_i1(
            self.H_T_ie,
            self.H_T_ia,
            self.H_T_iae,
            self.H_T_iaBE,
            self.H_T_ig,
            self.t_int_i,
            self.t_e,
        )


@dataclass
class Zone:
    name: str

    transmission_heat_loss = field(init=False)
    ventilation_heat_loss = field(init=False)
    heating_up_powers = field(init=False)
    heat_gains = field(init=False)
    design_heat_load: float = field(init=False)


@dataclass
class Building:
    name: str

    transmission_heat_loss = field(init=False)
    ventilation_heat_loss = field(init=False)
    heating_up_powers = field(init=False)
    heat_gains = field(init=False)
    design_heat_load: float = field(init=False)
