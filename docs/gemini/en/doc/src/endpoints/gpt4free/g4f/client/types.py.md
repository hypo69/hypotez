# Hypotez: GPT4Free Client Types Module

## Overview

This module defines types and classes used for interacting with the GPT4Free API. It sets up the foundation for handling API requests and responses.

## Details

The `types.py` file defines type aliases and a basic client class for working with the GPT4Free API. 

- `ImageProvider` defines a union type, allowing the use of either a `BaseProvider` object or a generic object. This provides flexibility for handling different image providers.
- `Proxies` allows passing either a dictionary of proxy settings or a simple proxy string. This supports both specific and generic proxy configurations.
- `IterResponse` and `AsyncIterResponse` define types for iterating through GPT4Free responses. These types represent the API's responses as iterators for efficient processing.

The `Client` class provides a base for interacting with the GPT4Free API, setting up initial configurations including API key and proxy settings. 

## Classes

### `Client`

**Description**: The `Client` class provides a basic structure for interacting with the GPT4Free API.

**Attributes**:

- `api_key` (str): The GPT4Free API key used for authentication.
- `proxies` (Proxies): Proxy settings for API requests.
- `proxy` (str): The selected proxy string, determined from `proxies`.

**Methods**:

- `get_proxy()`:  Retrieves the appropriate proxy string from the `proxies` attribute. It prioritizes a specific proxy for the `https` protocol, then the `all` proxy if available, and finally falls back to an environment variable `G4F_PROXY`.

```python
class Client():
    """
    Базовый класс для взаимодействия с GPT4Free API.

    Attributes:
        api_key (str): API-ключ GPT4Free для аутентификации.
        proxies (Proxies): Параметры прокси для API-запросов.
        proxy (str): Выбранная строка прокси, определенная из `proxies`.

    Methods:
        get_proxy(): Извлекает соответствующую строку прокси из атрибута `proxies`. 
            Сначала проверяется наличие прокси для `https`, затем `all`, 
            и, в качестве последнего средства, используется переменная окружения `G4F_PROXY`.
    """
    def __init__(
        self,
        api_key: str = None,
        proxies: Proxies = None,
        **kwargs
    ) -> None:
        """
        Инициализирует клиент GPT4Free.

        Args:
            api_key (str, optional): API-ключ GPT4Free. Defaults to None.
            proxies (Proxies, optional): Настройки прокси. Defaults to None.
            **kwargs: Дополнительные аргументы.
        """
        self.api_key: str = api_key
        self.proxies= proxies 
        self.proxy: str = self.get_proxy()

    def get_proxy(self) -> Union[str, None]:
        """
        Извлекает соответствующую строку прокси из атрибута `proxies`.

        Returns:
            Union[str, None]: Выбранная строка прокси или `None`, 
                если прокси не найден.
        """
        if isinstance(self.proxies, str):
            return self.proxies
        elif self.proxies is None:
            return os.environ.get("G4F_PROXY")
        elif "all" in self.proxies:
            return self.proxies["all"]
        elif "https" in self.proxies:
            return self.proxies["https"]
```