from __future__ import annotations

# --8<-- [start:example]
# docker-compose.yml
#
# services:
#   redis:
#     image: redis:7-alpine
#     ports:
#       - "6379:6379"
#
#   worker:
#     build: .
#     command: celery -A tasks worker --loglevel=info --concurrency=1
#     environment:
#       - ENERGYPLUS_DIR=/usr/local/EnergyPlus-25-2-0
#     volumes:
#       - ./models:/app/models:ro
#       - ./weather:/app/weather:ro
#       - sim-results:/tmp/sim-results
#     depends_on:
#       - redis
#     deploy:
#       replicas: 4          # 4 workers = 4 parallel simulations
#       resources:
#         limits:
#           cpus: "1"         # 1 CPU per worker
#           memory: 2G
#
#   flower:
#     image: mher/flower
#     command: celery --broker=redis://redis:6379/0 flower
#     ports:
#       - "5555:5555"
#     depends_on:
#       - redis
#
# volumes:
#   sim-results:
# --8<-- [end:example]
