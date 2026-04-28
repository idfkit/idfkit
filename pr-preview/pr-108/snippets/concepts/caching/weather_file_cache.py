from __future__ import annotations

# --8<-- [start:example]
import shutil
from idfkit.weather.download import default_cache_dir

shutil.rmtree(default_cache_dir())
# --8<-- [end:example]
