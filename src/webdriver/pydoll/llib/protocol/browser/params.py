from typing_extensions import NotRequired

from src.webdriver.pydoll.llib.constants import DownloadBehavior, PermissionType
from src.webdriver.pydoll.llib.protocol.base import CommandParams
from src.webdriver.pydoll.llib.protocol.browser.types import WindowBoundsDict


class GetWindowForTargetParams(CommandParams):
    """Parameters for getting window by target ID."""

    targetId: str


class SetDownloadBehaviorParams(CommandParams):
    """Parameters for setting download behavior."""

    behavior: DownloadBehavior
    downloadPath: NotRequired[str]
    browserContextId: NotRequired[str]
    eventsEnabled: NotRequired[bool]


class SetWindowBoundsParams(CommandParams):
    """Parameters for setting window bounds."""

    windowId: int
    bounds: WindowBoundsDict


class ResetPermissionsParams(CommandParams):
    """Parameters for resetting permissions."""

    browserContextId: NotRequired[str]


class CancelDownloadParams(CommandParams):
    """Parameters for cancelling downloads."""

    guid: str
    browserContextId: NotRequired[str]


class GrantPermissionsParams(CommandParams):
    """Parameters for granting permissions."""

    permissions: list[PermissionType]
    origin: NotRequired[str]
    browserContextId: NotRequired[str]
