# Модуль GigaChat.py

## Обзор

Модуль `GigaChat.py` предназначен для асинхронного взаимодействия с сервисом GigaChat от Сбербанка.
Он предоставляет функциональность для получения ответов от модели GigaChat, включая поддержку стриминга, истории сообщений и системных сообщений.
Модуль требует аутентификации через API ключ.

## Подробнее

Модуль использует `aiohttp` для выполнения асинхронных HTTP-запросов и включает поддержку SSL для безопасного соединения.
Он также управляет токенами доступа, автоматически обновляя их при необходимости.
Для работы требуется установленный сертификат безопасности.

## Классы

### `GigaChat`

**Описание**: Класс `GigaChat` предоставляет интерфейс для взаимодействия с API GigaChat.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL API GigaChat.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_stream` (bool): Флаг, указывающий на поддержку стриминга.
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.

## Методы класса

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool = True,
        proxy: str = None,
        api_key: str = None,
        connector: BaseConnector = None,
        scope: str = "GIGACHAT_API_PERS",
        update_interval: float = 0,
        **kwargs
    ) -> AsyncResult:
```

**Назначение**: Создает асинхронный генератор для взаимодействия с API GigaChat.

**Параметры**:
- `cls` (GigaChat): Ссылка на класс.
- `model` (str): Используемая модель GigaChat.
- `messages` (Messages): Список сообщений для отправки.
- `stream` (bool, optional): Флаг, указывающий на использование стриминга. По умолчанию `True`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `api_key` (str, optional): API ключ для аутентификации. По умолчанию `None`.
- `connector` (BaseConnector, optional): Асинхронный коннектор. По умолчанию `None`.
- `scope` (str, optional): Область доступа для токена. По умолчанию `"GIGACHAT_API_PERS"`.
- `update_interval` (float, optional): Интервал обновления. По умолчанию `0`.
- `**kwargs`: Дополнительные параметры для отправки в API.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от API GigaChat.

**Вызывает исключения**:
- `MissingAuthError`: Если отсутствует API ключ.

**Как работает функция**:
1. **Извлекает модель**: Извлекает имя модели с помощью `cls.get_model(model)`.
2. **Проверяет наличие API-ключа**: Если `api_key` не предоставлен, выбрасывается исключение `MissingAuthError`.
3. **Управление сертификатом**: Определяет путь к файлу сертификата (`russian_trusted_root_ca.crt`) в директории cookies. Если файл не существует, он создается и в него записывается содержимое `RUSSIAN_CA_CERT`.
4. **Создает SSL-контекст**: Если `has_ssl` истинно и `connector` не предоставлен, создает SSL-контекст с использованием сертификата.
5. **Создает сессию**: Создает асинхронную сессию `ClientSession` с использованием предоставленного или созданного коннектора.
6. **Обновление токена доступа**: Проверяет срок действия текущего токена доступа. Если токен истек или скоро истечет (менее 60 секунд), выполняет запрос на получение нового токена.
   - Функция отправляет POST-запрос на `https://ngw.devices.sberbank.ru:9443/api/v2/oauth` с заголовком `Authorization`, содержащим API-ключ, и телом запроса, содержащим область действия (`scope`).
   - Извлекает `access_token` и `expires_at` из полученных данных.
7. **Запрос к API GigaChat**: Отправляет POST-запрос к API GigaChat (`https://gigachat.devices.sberbank.ru/api/v1/chat/completions`) с использованием полученного токена доступа.
   - Тело запроса содержит параметры: `model`, `messages`, `stream`, `update_interval` и дополнительные параметры из `kwargs`.
8. **Обработка ответа**:
   - Если `stream` установлен в `False`, функция ожидает полный ответ, преобразует его из JSON и извлекает содержимое сообщения.
   - Если `stream` установлен в `True`, функция асинхронно итерирует по строкам ответа.
     - Удаляет префикс `data: ` и суффикс `\n` из каждой строки.
     - Если строка содержит `[DONE]`, функция завершает работу.
     - В противном случае строка преобразуется из JSON и извлекается содержимое (`content`) из `msg['delta']`.

**Примеры**:

```python
# Пример асинхронного вызова create_async_generator
import asyncio
from src.endpoints.gpt4free.g4f.Provider.needs_auth.GigaChat import GigaChat

async def main():
    api_key = "YOUR_API_KEY"  # Замените на ваш реальный API ключ
    messages = [{"role": "user", "content": "Привет, GigaChat!"}]
    
    generator = await GigaChat.create_async_generator(
        model="GigaChat:latest",
        messages=messages,
        api_key=api_key
    )
    
    async for message in generator:
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

## Параметры класса
- `url` (str): URL API GigaChat.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_stream` (bool): Флаг, указывающий на поддержку стриминга.
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.

## Переменные модуля
- `access_token` (str): Глобальная переменная для хранения токена доступа.
- `token_expires_at` (int): Глобальная переменная для хранения времени истечения токена доступа.
- `RUSSIAN_CA_CERT` (str): Строка, содержащая сертификат безопасности.