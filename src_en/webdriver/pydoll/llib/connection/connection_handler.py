## \file src/webdriver/pydoll/llib/connection/connection_handler.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module provides a connection handler for the Chrome DevTools Protocol.
=========================================================================

This module contains the `ConnectionHandler` class, which is responsible for
managing the WebSocket connection to the Chrome DevTools Protocol, sending commands,
and receiving events.

Example usage
-------------

```python
    import asyncio
    from src.webdriver.pydoll.llib.connection.connection_handler import ConnectionHandler
    from src.webdriver.pydoll.llib.commands.page_commands import PageCommands

    async def main():
        handler = ConnectionHandler(connection_port=9222)
        await handler._establish_new_connection()
        command = PageCommands.navigate(url="https://www.google.com")
        response = await handler.execute_command(command)
        print(response)
        await handler.close()

    if __name__ == "__main__":
        asyncio.run(main())
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/webdriver/pydoll/llib/connection/connection_handler.py
"""

import asyncio
import json
import logging
from contextlib import suppress
from typing import (
    Any,
    AsyncGenerator,
    Awaitable,
    Callable,
    Coroutine,
    Optional,
    TypeVar,
    Union,
    cast,
)

import websockets
from websockets.asyncio.client import ClientConnection
from websockets.asyncio.client import connect as Connect
from websockets.protocol import State

from src.webdriver.pydoll.llib.connection.managers import CommandsManager, EventsManager
from src.webdriver.pydoll.llib.exceptions import (
    CommandExecutionTimeout,
    WebSocketConnectionClosed,
)
from src.webdriver.pydoll.llib.protocol.base import Command, Event, Response
from src.webdriver.pydoll.llib.utils import get_browser_ws_address

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

T = TypeVar('T')


class ConnectionHandler:
    """
    WebSocket connection manager for Chrome DevTools Protocol endpoints.

    Handles connection lifecycle, command execution, and event subscription
    for both browser-level and page-level CDP endpoints.
    """

    def __init__(
        self,
        connection_port: int,
        page_id: Optional[str] = None,
        ws_address_resolver: Callable[[int], Coroutine[Any, Any, str]] = get_browser_ws_address,
        ws_connector: type[Connect] = websockets.connect,
    ):
        """
        Initialize connection handler.

        Args:
            connection_port: Browser's debugging server port.
            page_id: Target page ID. If None, connects to browser-level endpoint.
            ws_address_resolver: Function to resolve WebSocket URL from port.
            ws_connector: WebSocket connection factory (mainly for testing).
        """
        self._connection_port = connection_port
        self._page_id = page_id
        self._ws_address_resolver = ws_address_resolver
        self._ws_connector = ws_connector
        self._ws_connection: Optional[ClientConnection] = None
        self._command_manager = CommandsManager()
        self._events_handler = EventsManager()
        self._receive_task: Optional[asyncio.Task] = None
        logger.info('ConnectionHandler initialized.')

    @property
    def network_logs(self):
        """Access captured network request and response logs."""
        return self._events_handler.network_logs

    @property
    def dialog(self):
        """Access currently active JavaScript dialog information."""
        return self._events_handler.dialog

    async def ping(self) -> bool:
        """Test if WebSocket connection is active and responsive."""
        with suppress(Exception):
            await self._ensure_active_connection()
            await cast(ClientConnection, self._ws_connection).ping()
            return True
        return False

    async def execute_command(self, command: Command[T], timeout: int = 10) -> T:
        """
        Send CDP command and await response.

        Args:
            command: CDP command to send.
            timeout: Maximum seconds to wait for response.

        Returns:
            Parsed response object matching command's expected type.

        Raises:
            CommandExecutionTimeout: If browser doesn't respond within timeout.
            WebSocketConnectionClosed: If connection closes during execution.
        """
        await self._ensure_active_connection()
        future = self._command_manager.create_command_future(command)
        command_str = json.dumps(command)

        try:
            ws = cast(ClientConnection, self._ws_connection)
            await ws.send(command_str)
            response: str = await asyncio.wait_for(future, timeout)
            return json.loads(response)
        except asyncio.TimeoutError:
            self._command_manager.remove_pending_command(command['id'])
            raise CommandExecutionTimeout()
        except websockets.ConnectionClosed:
            await self._handle_connection_loss()
            raise WebSocketConnectionClosed()

    async def register_callback(
        self,
        event_name: str,
        callback: Callable[[dict], Awaitable[None]],
        temporary: bool = False,
    ) -> int:
        """
        Register event listener for CDP events.

        Args:
            event_name: CDP event name (e.g., 'Page.loadEventFired').
            callback: Async function called when event occurs.
            temporary: If True, callback removed after first trigger.

        Returns:
            Callback ID for later removal.

        Note:
            Corresponding CDP domain must be enabled before events fire.
        """
        return self._events_handler.register_callback(event_name, callback, temporary)

    async def remove_callback(self, callback_id: int) -> bool:
        """
        Remove registered event callback by ID.

        Args:
            callback_id: The ID of the callback to remove.

        Returns:
            bool: True if the callback was successfully removed, False otherwise.
        """
        return self._events_handler.remove_callback(callback_id)

    async def clear_callbacks(self):
        """
        Remove all registered event callbacks.

        This method clears all event listeners that have been registered with this handler.
        """
        self._events_handler.clear_callbacks()

    async def close(self):
        """
        Close WebSocket connection and release resources.

        This method closes the underlying WebSocket connection and cleans up any
        associated resources, including all registered event callbacks.
        """
        await self.clear_callbacks()
        if self._ws_connection is None:
            return

        with suppress(websockets.ConnectionClosed):
            await self._ws_connection.close()
        logger.info('WebSocket connection closed.')

    async def _ensure_active_connection(self):
        """
        Ensure active connection exists, establishing new one if needed.

        This method checks if the WebSocket connection is active. If not, it attempts
        to establish a new connection. This is crucial for maintaining a robust
        communication channel with the browser.
        """
        if self._ws_connection is None or self._ws_connection.state is State.CLOSED:
            await self._establish_new_connection()

    async def _establish_new_connection(self):
        """
        Create fresh WebSocket connection and start event listening.

        This method initiates a new WebSocket connection to the browser's DevTools
        endpoint and starts a background task to listen for incoming events.
        """
        ws_address = await self._resolve_ws_address()
        logger.info(f'Connecting to {ws_address}')
        self._ws_connection = await self._ws_connector(
            ws_address,
            max_size=1024 * 1024 * 10,  # 10MB
        )
        self._receive_task = asyncio.create_task(self._receive_events())
        logger.debug('WebSocket connection established')

    async def _resolve_ws_address(self):
        """
        Determine correct WebSocket address based on page ID.

        If a page ID is provided, it constructs the WebSocket URL for that specific page.
        Otherwise, it resolves the browser-level WebSocket address.

        Returns:
            str: The WebSocket URL to connect to.
        """
        if not self._page_id:
            return await self._ws_address_resolver(self._connection_port)
        return f'ws://localhost:{self._connection_port}/devtools/page/{self._page_id}'

    async def _handle_connection_loss(self):
        """
        Clean up resources after connection loss.

        This method is called when the WebSocket connection is lost. It closes the
        connection, cancels the event receiving task, and resets the connection state.
        """
        if self._ws_connection and self._ws_connection.state is not State.CLOSED:
            await self._ws_connection.close()
        self._ws_connection = None

        if self._receive_task and not self._receive_task.done():
            self._receive_task.cancel()

        logger.info('Connection resources cleaned up')

    async def _receive_events(self):
        """
        Main loop for receiving and processing WebSocket messages.

        This method continuously listens for incoming WebSocket messages and processes
        them. It handles both command responses and event notifications.
        """
        try:
            async for raw_message in self._incoming_messages():
                await self._process_single_message(raw_message)
        except websockets.ConnectionClosed as e:
            logger.info(f'Connection closed gracefully: {e}')
        except Exception as e:
            logger.error(f'Unexpected error in event loop: {e}')
            raise

    async def _incoming_messages(self) -> AsyncGenerator[Union[str, bytes], None]:
        """
        Generator yielding raw messages from WebSocket connection.

        This generator yields raw messages received from the WebSocket connection
        as long as the connection is open.

        Yields:
            Union[str, bytes]: The raw message received from the WebSocket.
        """
        ws = cast(ClientConnection, self._ws_connection)

        while ws.state is not State.CLOSED:
            yield await ws.recv()

    async def _process_single_message(self, raw_message: str):
        """
        Process single raw WebSocket message.

        This method parses the raw message and dispatches it to either the command
        manager (if it's a command response) or the event handler (if it's an event
        notification).

        Args:
            raw_message (str): The raw message string received from the WebSocket.
        """
        message = self._parse_message(raw_message)
        if not message:
            return

        if self._is_command_response(message):
            message = cast(Response, message)
            await self._handle_command_message(message)
        else:
            message = cast(Event, message)
            await self._handle_event_message(message)

    @staticmethod
    def _parse_message(raw_message: str) -> Union[Event, Response, None]:
        """
        Parse raw message string into JSON object.

        This static method attempts to parse a raw message string into a JSON object.
        It handles potential JSON decoding errors gracefully.

        Args:
            raw_message (str): The raw message string to parse.

        Returns:
            Union[Event, Response, None]: The parsed JSON object, or None if parsing fails.
        """
        try:
            return json.loads(raw_message)
        except json.JSONDecodeError:
            logger.warning(f'Failed to parse message: {raw_message[:200]}...')
            return None

    @staticmethod
    def _is_command_response(message: Union[Event, Response]) -> bool:
        """
        Determine if message is command response or event notification.

        This static method checks if a given message is a command response by verifying
        the presence and type of the 'id' field.

        Args:
            message (Union[Event, Response]): The message to check.

        Returns:
            bool: True if the message is a command response, False otherwise.
        """
        return 'id' in message and isinstance(message.get('id'), int)

    async def _handle_command_message(self, message: Response):
        """
        Process command response messages.

        This method resolves the pending command associated with the response ID
        using the command manager.

        Args:
            message (Response): The command response message to handle.
        """
        logger.debug(f'Processing command response: {message.get("id")}')
        self._command_manager.resolve_command(message['id'], json.dumps(message))

    async def _handle_event_message(self, message: Event):
        """
        Process event notification messages.

        This method dispatches the event to the event handler for further processing.

        Args:
            message (Event): The event notification message to handle.
        """
        event_type = message.get('method', 'unknown-event')
        logger.debug(f'Processing {event_type} event')
        await self._events_handler.process_event(message)

    def __repr__(self):
        """
        String representation for debugging.

        Returns:
            str: A string representation of the ConnectionHandler object.
        """
        return f'ConnectionHandler(port={self._connection_port})'

    def __str__(self):
        """
        User-friendly string representation.

        Returns:
            str: A user-friendly string representation of the ConnectionHandler object.
        """
        return f'ConnectionHandler(port={self._connection_port})'

    async def __aenter__(self):
        """
        Async context manager entry.

        This method is called when entering an asynchronous context. It returns the
        ConnectionHandler instance itself.

        Returns:
            ConnectionHandler: The ConnectionHandler instance.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Async context manager exit with cleanup.

        This method is called when exiting an asynchronous context. It ensures that
        the WebSocket connection is closed and resources are released.

        Args:
            exc_type: The type of the exception that caused the context to be exited.
            exc_val: The exception instance.
            exc_tb: The traceback object.
        """
        await self.close()
