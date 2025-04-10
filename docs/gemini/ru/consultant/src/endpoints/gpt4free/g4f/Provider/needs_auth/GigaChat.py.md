### **Анализ кода модуля `GigaChat.py`**

## \file /hypotez/src/endpoints/gpt4free/g4f/Provider/needs_auth/GigaChat.py

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
  - Использование `async` для асинхронных операций.
  - Обработка ошибок с помощью `raise_for_status`.
  - Поддержка потоковой передачи данных (`stream`).
  - Использование `ClientSession` для управления HTTP-соединениями.
- **Минусы**:
  - Отсутствуют аннотации типов для переменных и параметров функций.
  - Не используется `logger` для логирования ошибок и отладочной информации.
  - Глобальные переменные `access_token` и `token_expires_at` могут привести к проблемам с многопоточностью и отслеживанием состояния.
  - Нет обработки исключений при записи сертификата в файл.
  - Не все строки документированы.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех переменных, аргументов функций и возвращаемых значений. Это улучшит читаемость и поможет избежать ошибок.

2.  **Использовать `logger` для логирования**:
    - Добавить логирование для отладки и обработки ошибок. Например, логировать успешное получение токена, ошибки при запросах к API и другие важные события.
    - Обязательно логировать все исключения с использованием `logger.error` и `exc_info=True`.

3.  **Избегать глобальных переменных**:
    - Переделать код, чтобы избежать использования глобальных переменных `access_token` и `token_expires_at`. Вместо этого можно использовать атрибуты класса или передавать токен как аргумент функции.

4.  **Добавить обработку исключений при записи сертификата**:
    - Обернуть код записи сертификата в блок `try...except`, чтобы обработать возможные исключения при записи файла.

5.  **Документировать код**:
    - Добавить docstring для класса `GigaChat` и его методов, описывающие их назначение, аргументы и возвращаемые значения.
    - Добавить комментарии для пояснения сложных участков кода.

6.  **Улучшить обработку ошибок**:
    - Добавить более детальную обработку ошибок, чтобы можно было корректно реагировать на различные ситуации (например, отсутствие доступа к сети, неверный API-ключ и т.д.).

7.  **Использовать `j_loads` для чтения JSON**:
    - Для чтения JSON-данных из ответов использовать `j_loads` вместо `json.loads`.

8.  **Удалить неиспользуемые импорты**:
    - Проверить и удалить неиспользуемые импорты, такие как `os`.

**Оптимизированный код:**

```python
from __future__ import annotations

import ssl
import time
import uuid
from pathlib import Path

import json
from aiohttp import ClientSession, TCPConnector, BaseConnector
from ...requests import raise_for_status
from ...typing import AsyncResult, Messages
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ...errors import MissingAuthError
from ..helper import get_connector
from ...cookies import get_cookies_dir
from src.logger import logger  # Импортируем logger
from typing import Optional, Dict

RUSSIAN_CA_CERT: str = """-----BEGIN CERTIFICATE-----\nMIIFwjCCA6qgAwIBAgICEAAwDQYJKoZIhvcNAQELBQAwcDELMAkGA1UEBhMCUlUx
PzA9BgNVBAoMNlRoZSBNaW5pc3RyeSBvZiBEaWdpdGFsIERldmVsb3BtZW50IGFu
ZCBDb21tdW5pY2F0aW9uczEgMB4GA1UEAwwXUnVzc2lhbiBUcnVzdGVkIFJvb3Qg
Q0EwHhcNMjIwMzAxMjEwNDE1WhcNMzIwMjI3MjEwNDE1WjBwMQswCQYDVQQGEwJS
VTE/MD0GA1UECgw2VGhlIE1pbmlzdHJ5IG9mIERpZ2l0YWwgRGV2ZWxvcG1lbnQg
YW5kIENvbW11bmljYXRpb25zMSAwHgYDVQQDDBdSdXNzaWFuIFRydXN0ZWQgUm9v
dCBDQTCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAMfFOZ8pUAL3+r2n
qqE0Zp52selXsKGFYoG0GM5bwz1bSFtCt+AZQMhkWQheI3poZAToYJu69pHLKS6Q
XBiwBC1cvzYmUYKMYZC7jE5YhEU2bSL0mX7NaMxMDmH2/NwuOVRj8OImVa5s1F4U
zn4Kv3PFlDBjjSjXKVY9kmjUBsXQrIHeaqmUIsPIlNWUnimXS0I0abExqkbdrXbX
YwCOXhOO2pDUx3ckmJlCMUGacUTnylyQW2VsJIyIGA8V0xzdaeUXg0VZ6ZmNUr5Y
Ber/EAOLPb8NYpsAhJe2mXjMB/J9HNsoFMBFJ0lLOT/+dQvjbdRZoOT8eqJpWnVD
U+QL/qEZnz57N88OWM3rabJkRNdU/Z7x5SFIM9FrqtN8xewsiBWBI0K6XFuOBOTD
4V08o4TzJ8+Ccq5XlCUW2L48pZNCYuBDfBh7FxkB7qDgGDiaftEkZZfApRg2E+M9
G8wkNKTPLDc4wH0FDTijhgxR3Y4PiS1HL2Zhw7bD3CbslmEGgfnnZojNkJtcLeBH
BLa52/dSwNU4WWLubaYSiAmA9IUMX1/RpfpxOxd4Ykmhz97oFbUaDJFipIggx5sX
ePAlkTdWnv+RWBxlJwMQ25oEHmRguNYf4Zr/Rxr9cS93Y+mdXIZaBEE0KS2iLRqa
OiWBki9IMQU4phqPOBAaG7A+eP8PAgMBAAGjZjBkMB0GA1UdDgQWBBTh0YHlzlpf
BKrS6badZrHF+qwshzAfBgNVHSMEGDAWgBTh0YHlzlpfBKrS6badZrHF+qwshzAS
BgNVHRMBAf8ECDAGAQH/AgEEMA4GA1UdDwEB/wQEAwIBhjANBgkqhkiG9w0BAQsF
AAOCAgEAALIY1wkilt/urfEVM5vKzr6utOeDWCUczmWX/RX4ljpRdgF+5fAIS4vH
ntmXkqpSCOVeWUrJV9QvZn6L227ZwuE15cWi8DCDal3Ue90WgAJJZMfTshN4OI8cq
W9E4EG9wglbEtMnObHlms8F3CHmrw3k6KmUkWGoa+/ENmcVl68u/cMRl1JbW2bM+
/3A+SAg2c6iPDlehczKx2oa95QW0SkPPWGuNA/CE8CpyANIhu9XFrj3RQ3EqeRcS
AQQod1RNuHpfETLU/A2gMmvn/w/sx7TB3W5BPs6rprOA37tutPq9u6FTZOcG1Oqj
C/B7yTqgI7rbyvox7DEXoX7rIiEqyNNUguTk/u3SZ4VXE2kmxdmSh3TQvybfbnXV
4JbCZVaqiZraqc7oZMnRoWrXRG3ztbnbes/9qhRGI7PqXqeKJBztxRTEVj8ONs1d
WN5szTwaPIvhkhO3CO5ErU2rVdUr89wKpNXbBODFKRtgxUT70YpmJ46VVaqdAhOZ
D9EUUn4YaeLaS8AjSF/h7UkjOibNc4qVDiPP+rkehFWM66PVnP1Msh93tc+taIfC
EYVMxjh8zNbFuoc7fzvvrFILLe7ifvEIUqSVIC/AzplM/Jxw7buXFeGP1qVCBEHq
391d/9RAfaZ12zkwFsl+IKwE/OZxW8AHa9i1p4GO0YSNuczzEm4=
-----END CERTIFICATE-----"""

class GigaChat(AsyncGeneratorProvider, ProviderModelMixin):
    """
    Асинхронный генератор для взаимодействия с GigaChat API.

    Поддерживает потоковую передачу сообщений и аутентификацию через API-ключ.
    """
    url: str = "https://developers.sber.ru/gigachat"
    working: bool = True
    supports_message_history: bool = True
    supports_system_message: bool = True
    supports_stream: bool = True
    needs_auth: bool = True
    default_model: str = "GigaChat:latest"
    models: list[str] = [default_model, "GigaChat-Plus", "GigaChat-Pro"]

    # class Token:
    #     access_token: str = ""
    #     token_expires_at: int = 0

    @classmethod
    async def create_async_generator(
            cls,
            model: str,
            messages: Messages,
            stream: bool = True,
            proxy: Optional[str] = None,
            api_key: Optional[str] = None,
            connector: Optional[BaseConnector] = None,
            scope: str = "GIGACHAT_API_PERS",
            update_interval: float = 0,
            **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для получения ответов от GigaChat API.

        Args:
            model (str): Имя модели для использования.
            messages (Messages): Список сообщений для отправки.
            stream (bool, optional): Включает потоковую передачу ответов. По умолчанию True.
            proxy (Optional[str], optional): Прокси-сервер для использования. По умолчанию None.
            api_key (Optional[str], optional): API-ключ для аутентификации. По умолчанию None.
            connector (Optional[BaseConnector], optional): TCP-коннектор для сессии. По умолчанию None.
            scope (str, optional): Область доступа. По умолчанию "GIGACHAT_API_PERS".
            update_interval (float, optional): Интервал обновления. По умолчанию 0.
            **kwargs: Дополнительные аргументы для передачи в API.

        Returns:
            AsyncResult: Асинхронный генератор для получения ответов.

        Raises:
            MissingAuthError: Если не предоставлен API-ключ.
        """
        # global access_token, token_expires_at # Избегаем использования глобальных переменных
        # token: Token = Token()
        model = cls.get_model(model)
        if not api_key:
            raise MissingAuthError('Missing "api_key"')

        # Create certificate file in cookies directory
        cookies_dir: Path = Path(get_cookies_dir())
        cert_file: Path = cookies_dir / 'russian_trusted_root_ca.crt'

        # Write certificate if it doesn't exist
        if not cert_file.exists():
            try:
                cert_file.write_text(RUSSIAN_CA_CERT)
                logger.info(f'Certificate file created at {cert_file}')
            except Exception as ex:
                logger.error(f'Error writing certificate file to {cert_file}', ex, exc_info=True)
                raise

        ssl_context: Optional[ssl.SSLContext] = None

        if ssl and connector is None:
            ssl_context = ssl.create_default_context(cafile=str(cert_file))
            connector = TCPConnector(ssl_context=ssl_context)

        # async with ClientSession(connector=get_connector(connector, proxy)) as session:
        session_connector: BaseConnector = get_connector(connector, proxy)
        async with ClientSession(connector=session_connector) as session:
            token: Dict[str, str | int] = await cls.get_access_token(api_key, scope, session)
            access_token: str = token['access_token']
            # if token.token_expires_at - int(time.time() * 1000) < 60000:
            #     async with session.post(url="https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
            #                             headers={"Authorization": f"Bearer {api_key}",
            #                                      "RqUID": str(uuid.uuid4()),
            #                                      "Content-Type": "application/x-www-form-urlencoded"},
            #                             data={"scope": scope}) as response:
            #         await raise_for_status(response)
            #         data = await response.json()
            #     token.access_token = data['access_token']
            #     token.token_expires_at = data['expires_at']
            # access_token = token.access_token

            async with session.post(url="https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
                                    headers={"Authorization": f"Bearer {access_token}"},
                                    json={
                                        "model": model,
                                        "messages": messages,
                                        "stream": stream,
                                        "update_interval": update_interval,
                                        **kwargs
                                    }) as response:
                await raise_for_status(response)

                async for line in response.content:
                    if not stream:
                        yield json.loads(line.decode("utf-8"))['choices'][0]['message']['content']
                        return

                    if line and line.startswith(b"data:"):
                        line = line[6:-1]  # remove "data: " prefix and "\\n" suffix
                        if line.strip() == b"[DONE]":
                            return
                        else:
                            msg = json.loads(line.decode("utf-8"))['choices'][0]
                            content = msg['delta']['content']

                            if content:
                                yield content

                            if 'finish_reason' in msg:
                                return

    @classmethod
    async def get_access_token(cls, api_key: str, scope: str, session: ClientSession) -> Dict[str, str | int]:
        """
        Получает access token для GigaChat API.

        Args:
            api_key (str): API-ключ для аутентификации.
            scope (str): Область доступа.
            session (ClientSession): Асинхронная сессия для выполнения запросов.

        Returns:
            Dict[str, str | int]: Словарь с access token и временем истечения.

        Raises:
            Exception: Если не удалось получить access token.
        """
        try:
            async with session.post(
                    url="https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "RqUID": str(uuid.uuid4()),
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    data={"scope": scope}
            ) as response:
                await raise_for_status(response)
                data: Dict[str, str | int] = await response.json()
                logger.info(f'Токен успешно получен')
                return data
        except Exception as ex:
            logger.error('Error while getting access token', ex, exc_info=True)
            raise