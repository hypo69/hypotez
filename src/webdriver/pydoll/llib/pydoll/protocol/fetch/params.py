from typing_extensions import NotRequired

from src.webdriver.pydoll.llib.pydoll.constants import NetworkErrorReason, RequestMethod
from src.webdriver.pydoll.llib.pydoll.protocol.base import CommandParams
from src.webdriver.pydoll.llib.pydoll.protocol.fetch.types import (
    AuthChallengeResponseDict,
    HeaderEntry,
    RequestPattern,
)


class ContinueRequestParams(CommandParams):
    """Parameters for continuing a request."""

    requestId: str
    url: NotRequired[str]
    method: NotRequired[RequestMethod]
    postData: NotRequired[str]
    headers: NotRequired[list[HeaderEntry]]
    interceptResponse: NotRequired[bool]


class ContinueWithAuthParams(CommandParams):
    requestId: str
    authChallengeResponse: AuthChallengeResponseDict


class FetchEnableParams(CommandParams):
    patterns: NotRequired[list[RequestPattern]]
    handleAuthRequests: NotRequired[bool]


class FailRequestParams(CommandParams):
    requestId: str
    errorReason: NetworkErrorReason


class FulfillRequestParams(CommandParams):
    requestId: str
    responseCode: int
    responseHeaders: NotRequired[list[HeaderEntry]]
    body: NotRequired[str]
    responsePhrase: NotRequired[str]


class GetResponseBodyParams(CommandParams):
    requestId: str


class TakeResponseBodyAsStreamParams(CommandParams):
    requestId: str


class ContinueResponseParams(CommandParams):
    requestId: str
    responseCode: NotRequired[int]
    responsePhrase: NotRequired[str]
    responseHeaders: NotRequired[list[HeaderEntry]]
