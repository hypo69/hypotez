# Модуль API для взаимодействия с GPT4Free

## Обзор

Модуль `api.py` предоставляет API для взаимодействия с различными моделями и провайдерами в рамках проекта `GPT4Free`. Он включает в себя функции для получения списка моделей, провайдеров, версий, а также для создания и управления беседами с использованием этих моделей.

## Подробней

Модуль содержит класс `Api` с методами, которые обеспечивают доступ к информации о моделях, провайдерах и их параметрах. Он также включает функции для обработки запросов и формирования ответов в формате JSON для передачи данных между клиентом и сервером. Кроме того, модуль обеспечивает логирование и обработку ошибок.

## Классы

### `Api`

**Описание**: Класс, содержащий статические методы для получения информации о моделях, провайдерах и версиях, а также методы для обработки запросов и формирования ответов.

**Методы**:

- `get_models()`:
    ```python
    @staticmethod
    def get_models():
        """
        Возвращает список доступных моделей с информацией об их типах и провайдерах.

        Returns:
            list[dict]: Список словарей, каждый из которых содержит информацию о модели.
                         Каждый словарь имеет ключи "name" (название модели), "image" (является ли модель для работы с изображениями),
                         "vision" (является ли модель для компьютерного зрения) и "providers" (список провайдеров, поддерживающих модель).
        """
        ...
    ```

- `get_provider_models(provider: str, api_key: str = None, api_base: str = None)`:
    ```python
    @staticmethod
    def get_provider_models(provider: str, api_key: str = None, api_base: str = None):
        """
        Возвращает список моделей, поддерживаемых указанным провайдером.

        Args:
            provider (str): Название провайдера.
            api_key (str, optional): API-ключ для провайдера. По умолчанию `None`.
            api_base (str, optional): Базовый URL для провайдера. По умолчанию `None`.

        Returns:
            list[dict]: Список словарей, каждый из которых содержит информацию о модели провайдера.
                         Каждый словарь имеет ключи "model" (название модели), "default" (является ли модель моделью по умолчанию),
                         "vision" (является ли модель моделью для компьютерного зрения), "image" (является ли модель моделью для работы с изображениями)
                         и "task" (задача, которую выполняет модель).
        """
        ...
    ```

- `get_providers() -> dict[str, str]`:
    ```python
    @staticmethod
    def get_providers() -> dict[str, str]:
        """
        Возвращает список доступных провайдеров с информацией о них.

        Returns:
            dict[str, str]: Список словарей, каждый из которых содержит информацию о провайдере.
                            Каждый словарь имеет ключи "name" (название провайдера), "label" (метка провайдера),
                            "parent" (родительский провайдер, если есть), "image" (поддерживает ли провайдер работу с изображениями),
                            "vision" (поддерживает ли провайдер компьютерное зрение), "nodriver" (требуется ли драйвер для работы),
                            "hf_space" (является ли провайдер Hugging Face Space), "auth" (требуется ли аутентификация)
                            и "login_url" (URL для входа, если требуется аутентификация).
        """
        ...
    ```

- `get_version() -> dict`:
    ```python
    @staticmethod
    def get_version() -> dict:
        """
        Возвращает информацию о текущей и последней доступной версиях.

        Returns:
            dict: Словарь, содержащий информацию о версиях.
                  Имеет ключи "version" (текущая версия) и "latest_version" (последняя доступная версия).
        """
        ...
    ```

- `serve_images(self, name)`:
    ```python
    def serve_images(self, name):
        """
        Возвращает запрошенное изображение из директории с изображениями.

        Args:
            name (str): Имя файла изображения.

        Returns:
            flask.Response: Ответ Flask, содержащий запрошенное изображение.
        """
        ...
    ```

- `_prepare_conversation_kwargs(self, json_data: dict)`:
    ```python
    def _prepare_conversation_kwargs(self, json_data: dict):
        """
        Подготавливает аргументы для создания или продолжения беседы.

        Args:
            json_data (dict): JSON-данные запроса.

        Returns:
            dict: Словарь аргументов для создания или продолжения беседы.
        """
        ...
    ```

- `_create_response_stream(self, kwargs: dict, conversation_id: str, provider: str, download_media: bool = True) -> Iterator`:
    ```python
    def _create_response_stream(self, kwargs: dict, conversation_id: str, provider: str, download_media: bool = True) -> Iterator:
        """
        Создает поток ответов для беседы.

        Args:
            kwargs (dict): Аргументы для создания потока ответов.
            conversation_id (str): Идентификатор беседы.
            provider (str): Название провайдера.
            download_media (bool, optional): Флаг, указывающий, нужно ли скачивать медиафайлы. По умолчанию `True`.

        Yields:
            Iterator: Итератор, возвращающий части ответа в формате JSON.
        """
        ...
    ```

- `_yield_logs(self)`:
    ```python
    def _yield_logs(self):
        """
        Возвращает логи отладки.

        Yields:
            dict: Словарь с логами отладки.
        """
        ...
    ```

- `_format_json(self, response_type: str, content = None, **kwargs)`:
    ```python
    def _format_json(self, response_type: str, content = None, **kwargs):
        """
        Форматирует ответ в формате JSON.

        Args:
            response_type (str): Тип ответа.
            content (Any, optional): Содержимое ответа. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            dict: Словарь, содержащий отформатированный ответ в формате JSON.
        """
        ...
    ```

- `handle_provider(self, provider_handler, model)`:
    ```python
    def handle_provider(self, provider_handler, model):
        """
        Форматирует информацию о провайдере в формате JSON.

        Args:
            provider_handler: Обработчик провайдера.
            model: Модель.

        Returns:
            dict: Словарь, содержащий информацию о провайдере в формате JSON.
        """
        ...
    ```

## Функции

### `get_error_message(exception: Exception) -> str`

```python
def get_error_message(exception: Exception) -> str:
    """
    Форматирует сообщение об ошибке из исключения.

    Args:
        exception (Exception): Объект исключения.

    Returns:
        str: Отформатированное сообщение об ошибке.
    """
    ...