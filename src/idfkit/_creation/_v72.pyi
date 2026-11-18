"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence

from .. import _generated_types as _g
from .. import versioned as _vd

class ZonePropertyUserViewFactorsbySurfaceName_v9_2_to_v9_3:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_or_zonelist_name: str | None = ...,
        view_factors: Sequence[
            _vd.ZonePropertyUserViewFactorsbySurfaceNameViewFactorsItem_v9_2_to_v9_3
            | _vd.ZonePropertyUserViewFactorsbySurfaceNameViewFactorsGroup_v9_2_to_v9_3
        ] = ...,
    ) -> None:
        """Create a new ``ZoneProperty:UserViewFactors:bySurfaceName`` and add it to the document.

        View factors for Surface to Surface in a zone. (Number of Surfaces)**2 are expected. Any omitted surface pairs will be assumed to have a view factor of zero.
        """
