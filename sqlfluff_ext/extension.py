"""Meltano SQLFluff extension."""
from __future__ import annotations

import subprocess
import sys
from typing import Any

import structlog
from meltano.edk import models
from meltano.edk.extension import ExtensionBase
from meltano.edk.process import Invoker, log_subprocess_error

log = structlog.get_logger()


class SQLFluff(ExtensionBase):
    """Extension implementing the ExtensionBase interface."""

    def __init__(self) -> None:
        """Initialize the extension."""
        self.sqlfluff_bin = "sqlfluff"  # verify this is the correct name
        self.sqlfluff_invoker = Invoker(self.sqlfluff_bin)

    def invoke(self, command_name: str | None, *command_args: Any) -> None:
        """Invoke the underlying cli, that is being wrapped by this extension.

        Args:
            command_name: The name of the command to invoke.
            command_args: The arguments to pass to the command.
        """
        try:
            self.sqlfluff_invoker.run_and_log(command_name, *command_args)
        except subprocess.CalledProcessError as err:
            log_subprocess_error(
                f"sqlfluff {command_name}", err, "SQLFluff invocation failed"
            )
            sys.exit(err.returncode)

    def describe(self) -> models.Describe:
        """Describe the extension.

        Returns:
            The extension description
        """
        # TODO: could we auto-generate all or portions of this from typer instead?
        return models.Describe(
            commands=[
                models.ExtensionCommand(
                    name="sqlfluff_extension", description="extension commands"
                ),
                models.InvokerCommand(
                    name="sqlfluff_invoker", description="pass through invoker"
                ),
            ]
        )
