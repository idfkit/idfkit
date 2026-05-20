from __future__ import annotations

# --8<-- [start:example]
# celeryconfig.py
broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/1"

# Serialisation — JSON is safe and human-readable
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]

# Prevent a slow simulation from being acknowledged before it finishes.
# With acks_late the message is re-delivered if the worker crashes mid-run.
task_acks_late = True
task_reject_on_worker_lost = True

# One simulation per worker process — EnergyPlus is CPU-bound
worker_concurrency = 1

# Long timeout for annual simulations (4 hours)
task_time_limit = 14400
task_soft_time_limit = 14000

# Result expiry (24 hours)
result_expires = 86400
# --8<-- [end:example]
