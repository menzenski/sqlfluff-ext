"""Passthrough shim for SQLFluff extension."""
import sys

import structlog
from meltano.edk.logging import pass_through_logging_config
from sqlfluff_ext.extension import SQLFluff


def pass_through_cli() -> None:
    """Pass through CLI entry point."""
    pass_through_logging_config()
    ext = SQLFluff()
    ext.pass_through_invoker(
        structlog.getLogger("sqlfluff_invoker"),
        *sys.argv[1:] if len(sys.argv) > 1 else []
    )
