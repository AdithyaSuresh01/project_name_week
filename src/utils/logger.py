from __future__ import annotations

"""Logging utilities for ApiPlaygroundPy.

This module configures and exposes a small helper for obtaining
namespaced loggers with a consistent format.
"""

import logging
from typing import Optional


_DEFAULT_LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
_DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _configure_root_logger(level: int = logging.INFO) -> None:
    """Configure the root logger for the application.

    This setup is intentionally simple and writes to stdout with a
    readable, timestamped format. If the root logger is already
    configured (i.e. has handlers), this function does nothing.
    """

    root = logging.getLogger()
    if root.handlers:
        # Assume configuration already done by the application.
        return

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(_DEFAULT_LOG_FORMAT, _DEFAULT_DATE_FORMAT))
    root.addHandler(handler)
    root.setLevel(level)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a logger configured for the ApiPlaygroundPy project.

    Parameters
    ----------
    name:
        Logger name. If omitted or ``None``, returns the root logger.

    Notes
    -----
    The first call to this function sets up a basic configuration for
    the root logger. Subsequent calls will reuse that configuration.
    """

    _configure_root_logger()
    return logging.getLogger(name)
