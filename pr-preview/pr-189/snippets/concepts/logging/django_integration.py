from __future__ import annotations

# --8<-- [start:example]
# In your Django settings.py
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "idfkit": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "idfkit.simulation": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
# --8<-- [end:example]
