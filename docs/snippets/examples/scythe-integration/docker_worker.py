from __future__ import annotations

# --8<-- [start:dockerfile]
# syntax=docker/dockerfile:1
# FROM nrel/energyplus:24.2.0
#
# RUN pip install idfkit scythe-engine
#
# COPY experiments/ /app/experiments/
# COPY main.py /app/main.py
#
# WORKDIR /app
# CMD ["python", "main.py"]
# --8<-- [end:dockerfile]
