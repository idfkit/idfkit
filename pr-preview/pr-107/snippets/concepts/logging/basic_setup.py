from __future__ import annotations

# --8<-- [start:example]
import logging

# Show all INFO-level messages from idfkit
logging.basicConfig(level=logging.INFO)

# Load and parse — idfkit logs progress automatically
from idfkit import load_idf

doc = load_idf("model.idf")
# INFO:idfkit.idf_parser:Parsed 850 objects from model.idf in 0.142s
# --8<-- [end:example]
