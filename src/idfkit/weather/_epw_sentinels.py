"""Auto-generated EPW reserved-value table.

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_epw_sentinels

Emitted from checks/weather-monthly/sentinels.toml in idfkit-conformance at conformance-2026.12.

Source document: EnergyPlus Weather File (EPW) Data Dictionary, Auxiliary Programs
Versions checked: 23.2, 24.2
https://bigladdersoftware.com/epx/docs/24-2/auxiliary-programs/energyplus-weather-file-epw-data-dictionary.html

WHAT IS HERE AND WHAT IS NOT. Only the values that mean "not measured". A field may also reserve
values that are observations — ceiling height's 77777 for an unlimited ceiling and 88888 for a
cirroform one — and those are deliberately absent, because the reader's rule is to blank what this
table lists and to leave every other number alone. A reader that instead blanked "large numbers"
would blank 55% of the ceiling column in the sampled corpus.
"""

from __future__ import annotations

from typing import Final

#: Per numeric column position, the values that mean the measurement was not made. Positions absent
#: from this table reserve nothing.
MISSING_VALUES: Final[tuple[tuple[int, tuple[float, ...]], ...]] = (
    # Dry Bulb Temperature
    (6, (99.9,)),
    # Dew Point Temperature
    (7, (99.9,)),
    # Relative Humidity
    (8, (999,)),
    # Atmospheric Station Pressure
    (9, (999999,)),
    # Extraterrestrial Horizontal Radiation
    (10, (9999,)),
    # Extraterrestrial Direct Normal Radiation
    (11, (9999,)),
    # Horizontal Infrared Radiation Intensity from Sky
    (12, (9999,)),
    # Global Horizontal Radiation
    (13, (9999,)),
    # Direct Normal Radiation
    (14, (9999,)),
    # Diffuse Horizontal Radiation
    (15, (9999,)),
    # Global Horizontal Illuminance
    (16, (999999,)),
    # Direct Normal Illuminance
    (17, (999999,)),
    # Diffuse Horizontal Illuminance
    (18, (999999,)),
    # Zenith Luminance
    (19, (9999,)),
    # Wind Direction
    (20, (999,)),
    # Wind Speed
    (21, (999,)),
    # Total Sky Cover
    (22, (99,)),
    # Opaque Sky Cover
    (23, (99,)),
    # Visibility
    (24, (9999,)),
    # Ceiling Height
    (25, (99999,)),
    # Present Weather Observation
    (26, (9,)),
    # Precipitable Water
    (28, (999,)),
    # Aerosol Optical Depth
    (29, (0.999,)),
    # Snow Depth
    (30, (999,)),
    # Days Since Last Snowfall
    (31, (99,)),
    # Albedo
    (32, (999,)),
    # Liquid Precipitation Depth
    (33, (999,)),
    # Liquid Precipitation Quantity
    (34, (99,)),
)

#: The conformance level this table was generated from.
SENTINEL_LEVEL: Final[str] = "conformance-2026.12"
