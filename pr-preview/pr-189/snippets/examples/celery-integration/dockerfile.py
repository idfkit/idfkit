from __future__ import annotations

# --8<-- [start:example]
# Dockerfile
#
# FROM nrel/energyplus:25.2.0
#
# # Install Python and uv
# RUN apt-get update && apt-get install -y python3 python3-pip curl \
#     && curl -LsSf https://astral.sh/uv/install.sh | sh
#
# WORKDIR /app
# COPY pyproject.toml uv.lock ./
# RUN uv sync --frozen
#
# COPY celeryconfig.py tasks.py ./
# COPY models/ ./models/
# COPY weather/ ./weather/
#
# CMD ["uv", "run", "celery", "-A", "tasks", "worker", "--loglevel=info"]
# --8<-- [end:example]
