"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class RoofCeilingDetailed_v9_6_to_v24_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition: Literal[
            "Adiabatic",
            "Ground",
            "GroundBasementPreprocessorAverageFloor",
            "GroundBasementPreprocessorAverageWall",
            "GroundBasementPreprocessorLowerWall",
            "GroundBasementPreprocessorUpperWall",
            "GroundSlabPreprocessorAverage",
            "GroundSlabPreprocessorCore",
            "GroundSlabPreprocessorPerimeter",
            "OtherSideCoefficients",
            "OtherSideConditionsModel",
            "Outdoors",
            "Surface",
            "Zone",
        ],
        space_name: str | None = ...,
        outside_boundary_condition_object: str | None = ...,
        sun_exposure: Literal["", "NoSun", "SunExposed"] | None = "SunExposed",
        wind_exposure: Literal["", "NoWind", "WindExposed"] | None = "WindExposed",
        view_factor_to_ground: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        number_of_vertices: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        vertices: Sequence[_g.RoofCeilingDetailedVerticesItem | _g.RoofCeilingDetailedVerticesGroup] = ...,
    ) -> None:
        """Create a new ``RoofCeiling:Detailed`` and add it to the document.

        Allows for detailed entry of roof/ceiling heat transfer surfaces.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.2/io-reference/overview/group-thermal-zone-description-geometry/#roofceilingdetailed
        """

class PerformancePrecisionTradeoffs_v9_3:
    def __call__(
        self,
        /,
        *,
        use_coil_direct_solutions: Literal["", "No", "Yes"] | None = "No",
        zone_radiant_exchange_algorithm: Literal["", "CarrollMRT", "ScriptF"] | None = "ScriptF",
        override_mode: Literal["", "Advanced", "Mode01", "Mode02", "Mode03", "Mode04", "Mode05", "Normal"]
        | None = "Normal",
        maxzonetempdiff: float | None = 0.3,
    ) -> None:
        """Create a new ``PerformancePrecisionTradeoffs`` and add it to the document.

        This object enables users to choose certain options that speed up EnergyPlus simulation, but may lead to small decreases in accuracy of results.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.3/io-reference/overview/group-simulation-parameters/#performanceprecisiontradeoffs
        """

class BuildingSurfaceDetailed_v25_1_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_type: Literal["Ceiling", "Floor", "Roof", "Wall"],
        construction_name: str,
        zone_name: str,
        outside_boundary_condition: Literal[
            "Adiabatic",
            "Foundation",
            "Ground",
            "GroundBasementPreprocessorAverageFloor",
            "GroundBasementPreprocessorAverageWall",
            "GroundBasementPreprocessorLowerWall",
            "GroundBasementPreprocessorUpperWall",
            "GroundFCfactorMethod",
            "GroundSlabPreprocessorAverage",
            "GroundSlabPreprocessorCore",
            "GroundSlabPreprocessorPerimeter",
            "OtherSideCoefficients",
            "OtherSideConditionsModel",
            "Outdoors",
            "Space",
            "Surface",
            "Zone",
        ],
        space_name: str | None = ...,
        outside_boundary_condition_object: str | None = ...,
        sun_exposure: Literal["", "NoSun", "SunExposed"] | None = "SunExposed",
        wind_exposure: Literal["", "NoWind", "WindExposed"] | None = "WindExposed",
        view_factor_to_ground: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        number_of_vertices: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        vertices: Sequence[_g.BuildingSurfaceDetailedVerticesItem | _g.BuildingSurfaceDetailedVerticesGroup] = ...,
    ) -> None:
        """Create a new ``BuildingSurface:Detailed`` and add it to the document.

        Allows for detailed entry of building heat transfer surfaces. Does not include subsurfaces such as windows or doors.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-thermal-zone-description-geometry/#buildingsurfacedetailed
        """
