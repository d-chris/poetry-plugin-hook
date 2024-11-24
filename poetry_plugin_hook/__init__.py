"""
.. include:: ../README.md
"""

from poetry.plugins.application_plugin import ApplicationPlugin

from poetry_plugin_hook.bump import BumpCommand
from poetry_plugin_hook.latest import LatestCommand
from poetry_plugin_hook.sync import SyncCommand


class HookPlugin(ApplicationPlugin):
    def activate(self, application):

        application.command_loader.register_factory(
            BumpCommand.name,
            lambda: BumpCommand(),
        )
        application.command_loader.register_factory(
            LatestCommand.name,
            lambda: LatestCommand(),
        )
        application.command_loader.register_factory(
            SyncCommand.name,
            lambda: SyncCommand(),
        )


__all__ = [
    "BumpCommand",
    "LatestCommand",
    "SyncCommand",
]
