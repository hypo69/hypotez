# API Модуль для сервера G4F

## Обзор

Этот модуль предоставляет API для сервера G4F, который обрабатывает запросы от графического интерфейса (GUI) и взаимодействует с различными моделями искусственного интеллекта (ИИ) для выполнения задач обработки текста и изображений.

## Подробности

API обрабатывает запросы от графического интерфейса (GUI) и взаимодействует с различными моделями искусственного интеллекта (ИИ), такими как Google Gemini и OpenAI, для выполнения задач обработки текста и изображений. Он обеспечивает интерфейс для получения списка доступных моделей, получения моделей для конкретного провайдера, получения списка провайдеров, получения текущей и последней версии, а также обработки разговоров с использованием выбранных моделей.

## Классы

### `class Api`

**Описание**: Класс `Api` предоставляет набор статических методов для взаимодействия с различными моделями ИИ и провайдерами.

**Атрибуты**:

- `None`

**Методы**:

- `get_models()`: Возвращает список доступных моделей ИИ, включая информацию о их типах (текст, изображения, видение) и доступных провайдерах.

  ```python
  def get_models():
      """
      Возвращает список доступных моделей ИИ, включая информацию о их типах (текст, изображения, видение) и доступных провайдерах.

      Returns:
          list: Список словарей с информацией о каждой модели.
      """
  ```

- `get_provider_models(provider: str, api_key: str = None, api_base: str = None)`: Возвращает список моделей для указанного провайдера.

  ```python
  def get_provider_models(provider: str, api_key: str = None, api_base: str = None):
      """
      Возвращает список моделей для указанного провайдера.

      Args:
          provider (str): Имя провайдера.
          api_key (str, optional): Ключ API для провайдера. Defaults to None.
          api_base (str, optional): Базовый URL API для провайдера. Defaults to None.

      Returns:
          list: Список словарей с информацией о каждой модели для заданного провайдера.
      """
  ```

- `get_providers() -> dict[str, str]`: Возвращает словарь с информацией о доступных провайдерах.

  ```python
  def get_providers() -> dict[str, str]:
      """
      Возвращает словарь с информацией о доступных провайдерах.

      Returns:
          dict: Словарь, содержащий информацию о провайдерах, включая их имена, метки, типы (изображения, видение), 
          требования к аутентификации и другие атрибуты.
      """
  ```

- `get_version() -> dict`: Возвращает словарь с информацией о текущей и последней доступной версиях приложения.

  ```python
  def get_version() -> dict:
      """
      Возвращает словарь с информацией о текущей и последней доступной версиях приложения.

      Returns:
          dict: Словарь, содержащий текущую и последнюю версии приложения.
      """
  ```

- `serve_images(self, name)`: Возвращает изображение из папки `images_dir`.

  ```python
  def serve_images(self, name):
      """
      Возвращает изображение из папки `images_dir`.

      Args:
          name (str): Имя файла изображения.

      Returns:
          flask.Response: Ответ с изображением.
      """
  ```

- `_prepare_conversation_kwargs(self, json_data: dict)`: Подготавливает параметры для функции `ChatCompletion.create` на основе данных из запроса.

  ```python
  def _prepare_conversation_kwargs(self, json_data: dict):
      """
      Подготавливает параметры для функции `ChatCompletion.create` на основе данных из запроса.

      Args:
          json_data (dict): Данные запроса.

      Returns:
          dict: Словарь с параметрами для `ChatCompletion.create`.
      """
  ```

- `_create_response_stream(self, kwargs: dict, conversation_id: str, provider: str, download_media: bool = True) -> Iterator`: Создает поток ответов для обработки запроса.

  ```python
  def _create_response_stream(self, kwargs: dict, conversation_id: str, provider: str, download_media: bool = True) -> Iterator:
      """
      Создает поток ответов для обработки запроса.

      Args:
          kwargs (dict): Параметры для `ChatCompletion.create`.
          conversation_id (str): Идентификатор разговора.
          provider (str): Имя провайдера.
          download_media (bool, optional): Флаг для загрузки медиафайлов. Defaults to True.

      Returns:
          Iterator: Итератор, выдающий части ответа.
      """
  ```

- `_yield_logs()`: Выдает записи из буфера логов.

  ```python
  def _yield_logs():
      """
      Выдает записи из буфера логов.
      """
  ```

- `_format_json(self, response_type: str, content = None, **kwargs)`: Форматирует ответ в JSON.

  ```python
  def _format_json(self, response_type: str, content = None, **kwargs):
      """
      Форматирует ответ в JSON.

      Args:
          response_type (str): Тип ответа.
          content (any, optional): Содержимое ответа. Defaults to None.
          **kwargs: Дополнительные параметры для ответа.

      Returns:
          dict: Ответ в формате JSON.
      """
  ```

- `handle_provider(self, provider_handler, model)`: Обрабатывает информацию о провайдере и модели.

  ```python
  def handle_provider(self, provider_handler, model):
      """
      Обрабатывает информацию о провайдере и модели.

      Args:
          provider_handler (ProviderModelMixin): Объект провайдера.
          model (str): Имя модели.

      Returns:
          dict: Словарь с информацией о провайдере и модели.
      """
  ```

## Функции

### `get_error_message(exception: Exception) -> str`

**Цель**: Преобразует исключение в строку ошибки.

**Параметры**:

- `exception (Exception)`: Исключение, которое необходимо преобразовать в строку.

**Возвращает**:

- `str`: Строка с описанием ошибки.

**Примеры**:

```python
>>> get_error_message(ValueError("Invalid value"))
'ValueError: Invalid value'
```

## Примеры

### Пример использования класса `Api`

```python
from hypotez.src.endpoints.gpt4free.g4f.gui.server.api import Api

api = Api()
models = api.get_models()
print(models)

# Пример получения моделей для провайдера "OpenAI"
provider_models = api.get_provider_models(provider="OpenAI")
print(provider_models)

# Пример получения информации о версии
version_info = api.get_version()
print(version_info)
```

## Дополнительная информация

- Этот модуль является частью проекта `hypotez` и используется для управления API сервера G4F.
- Сервер G4F работает на Flask и обеспечивает взаимодействие с GUI-интерфейсом.
- `j_loads`, `j_loads_ns` используются для чтения JSON и конфигурационных файлов.
-  Используется `driver`  из модуля `src.webdirver`
- `print`  используется из модуля `src.utils.printer`
- Используются логгеры из модуля `src.logger`. 

## Ссылки
- [hypotez project repository](https://github.com/hypotez/hypotez)
- [Flask documentation](https://flask.palletsprojects.com/en/2.3.x/)
- [OpenAI API documentation](https://platform.openai.com/docs/api-reference)
- [Google Gemini documentation](https://developers.google.com/gemini)
- [Selenium documentation](https://www.selenium.dev/)
- [Playwright documentation](https://playwright.dev/)