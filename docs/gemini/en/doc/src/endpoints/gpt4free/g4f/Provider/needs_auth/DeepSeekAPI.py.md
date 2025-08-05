# DeepSeekAPI Provider

## Overview

This module implements the `DeepSeekAPI` class, an asynchronous provider for the `hypotez` project, designed for interacting with the DeepSeek chat API. This provider supports authentication, model selection, and message handling for generating responses from DeepSeek models.

## Details

The `DeepSeekAPI` provider utilizes the `dsk` library to communicate with the DeepSeek chat API. It supports authentication using a user token stored in the browser's local storage. The provider also offers model selection, allowing users to choose between different DeepSeek models for generating responses.

## Classes

### `class DeepSeekAPI(AsyncAuthedProvider, ProviderModelMixin)`

**Description**: The `DeepSeekAPI` class represents an asynchronous provider for interacting with the DeepSeek chat API. It inherits from `AsyncAuthedProvider` for authentication and `ProviderModelMixin` for model selection.

**Inherits**:
    - `AsyncAuthedProvider`: Provides methods for authenticating with the API.
    - `ProviderModelMixin`:  Allows selecting different DeepSeek models for generating responses.

**Attributes**:
    - `url` (str): The base URL of the DeepSeek chat API.
    - `working` (bool): Indicates if the DeepSeek library is available and the provider can function correctly.
    - `needs_auth` (bool):  Indicates if the provider requires authentication.
    - `use_nodriver` (bool): Indicates if the provider uses `get_nodriver` for interacting with the browser.
    - `_access_token` (str): The user's access token for authentication.
    - `default_model` (str): The default DeepSeek model to use.
    - `models` (list): A list of available DeepSeek models.

**Methods**:

    - `on_auth_async(proxy: str = None, **kwargs) -> AsyncIterator`: Performs asynchronous authentication with the DeepSeek API.
        - **Purpose**:  This method authenticates with the DeepSeek API using the user's access token stored in the browser's local storage.
        - **Parameters**:
            - `proxy` (str, optional):  A proxy server address. Defaults to `None`.
            - `**kwargs`: Additional keyword arguments.
        - **Returns**:  An asynchronous iterator yielding `RequestLogin` and `AuthResult` objects.
        - **Raises Exceptions**:  If the authentication process fails.

    - `create_authed(model: str, messages: Messages, auth_result: AuthResult, conversation: JsonConversation = None, web_search: bool = False, **kwargs) -> AsyncResult`:  Creates an authenticated chat session with the DeepSeek API.
        - **Purpose**:  This method creates an authenticated chat session with the DeepSeek API, allowing users to send messages and receive responses from the chosen model.
        - **Parameters**:
            - `model` (str): The DeepSeek model to use for generating responses.
            - `messages` (Messages): A list of messages in the current conversation.
            - `auth_result` (AuthResult):  Authentication result containing the user's access token.
            - `conversation` (JsonConversation, optional):  A conversation object containing the chat session ID. Defaults to `None`.
            - `web_search` (bool, optional): Indicates if web search is enabled for the model. Defaults to `False`.
            - `**kwargs`: Additional keyword arguments.
        - **Returns**:  An asynchronous iterator yielding `JsonConversation`, `Reasoning`, and `FinishReason` objects.

## Table of Contents

- [DeepSeekAPI Provider](#deepseekapi-provider)
    - [Overview](#overview)
    - [Details](#details)
    - [Classes](#classes)
        - [`class DeepSeekAPI(AsyncAuthedProvider, ProviderModelMixin)`](#class-deepseekapiasyncauthedproviderprovidermodelmixin)
            - [Attributes](#attributes)
            - [Methods](#methods)
    - [Table of Contents](#table-of-contents)