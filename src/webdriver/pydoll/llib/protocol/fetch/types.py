from typing_extensions import NotRequired, TypedDict

from src.webdriver.pydoll.llib.constants import AuthChallengeResponseValues, RequestStage, ResourceType


class HeaderEntry(TypedDict):
    """HTTP header entry structure."""

    name: str
    value: str


class AuthChallengeResponseDict(TypedDict):
    response: AuthChallengeResponseValues
    username: NotRequired[str]
    password: NotRequired[str]


class RequestPattern(TypedDict):
    urlPattern: str
    resourceType: NotRequired[ResourceType]
    requestStage: NotRequired[RequestStage]
