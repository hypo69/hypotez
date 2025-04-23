### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код отвечает за взаимодействие с GigaChat API от Сбербанка. Он получает токен доступа, отправляет запросы на генерацию текста и обрабатывает ответы, поддерживая как потоковую, так и не потоковую передачу данных. Также, создает и использует SSL-сертификат для безопасного соединения.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются различные модули, такие как `os`, `ssl`, `time`, `uuid`, `pathlib`, `json` и другие, необходимые для выполнения операций.

2. **Определение глобальных переменных**:
   - Определяются глобальные переменные `access_token` и `token_expires_at` для хранения токена доступа и времени его истечения.

3. **Чтение и использование сертификата**:
   - Проверяется наличие SSL, создается SSL-контекст с использованием сертификата `russian_trusted_root_ca.crt` для безопасного соединения.

4. **Создание сессии**:
   - Создается асинхронная сессия `ClientSession` с использованием `TCPConnector` и SSL-контекста.

5. **Получение токена доступа**:
   - Проверяется, истек ли срок действия текущего токена доступа. Если токен устарел или отсутствует, выполняется запрос к API для получения нового токена.
   - Для получения токена используется `api_key` из аргументов функции.
   - Сохраняется новый `access_token` и время его истечения `token_expires_at`.

6. **Отправка запроса к GigaChat API**:
   - Выполняется POST-запрос к API `https://gigachat.devices.sberbank.ru/api/v1/chat/completions` с использованием полученного токена доступа.
   - В запросе передаются параметры, такие как модель, сообщения, режим потоковой передачи и другие.

7. **Обработка ответа**:
   - Если `stream=False`, ответ возвращается как JSON, извлекается содержимое сообщения и возвращается.
   - Если `stream=True`, ответ обрабатывается построчно:
     - Каждая строка проверяется на наличие префикса `data:`.
     - Если строка содержит данные, они декодируются из JSON и извлекается содержимое сообщения.
     - Если строка содержит `[DONE]`, обработка завершается.
     - Извлекается контент из `msg['delta']['content']` и передается как результат.
     - Проверяется наличие `finish_reason` в сообщении, и если он присутствует, обработка завершается.

Пример использования
-------------------------

```python
from __future__ import annotations

import asyncio
import os
import time
import uuid
from pathlib import Path
import json
try:
    import ssl
    has_ssl = True
except ImportError:
    has_ssl = False
from aiohttp import ClientSession, TCPConnector, BaseConnector

# Mock необходимых классов и функций для примера
class MockResponse:
    async def json(self):
        return {'access_token': 'mock_token', 'expires_at': int(time.time() * 1000) + 100000}

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    async def iter_chunks(self):
        yield b'data: {"choices": [{"delta": {"content": "test"}}]}\n'
        yield b'data: [DONE]\n'

    @property
    def content(self):
        return self

class MockClientSession:
    def __init__(self, connector=None):
        pass

    async def post(self, url, headers, json=None, data=None):
        return MockResponse()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

async def mock_raise_for_status(response):
    pass

async def mock_get_connector(connector, proxy):
    return connector

async def mock_get_cookies_dir():
    return '.'

RUSSIAN_CA_CERT = """-----BEGIN CERTIFICATE-----\nMIIFwjCCA6qgAwIBAgICEAAwDQYJKoZIhvcNAQELBQAwcDELMAkGA1UEBhMCUlUx\nPzA9BgNVBAoMNlRoZSBNaW5pc3RyeSBvZiBEaWdpdGFsIERldmVsb3BtZW50IGFu\nZCBDb21tdW5pY2F0aW9uczEgMB4GA1UEAwwXUnVzc2lhbiBUcnVzdGVkIFJvb3Qg\nQ0EwHhcNMjIwMzAxMjEwNDE1WhcNMzIwMjI3MjEwNDE1WjBwMQswCQYDVQQGEwJS\nVTE/MD0GA1UECgw2VGhlIE1pbmlzdHJ5IG9mIERpZ2l0YWwgRGV2ZWxvcG1lbnQg\nYW5kIENvbW11bmljYXRpb25zMSAwHgYDVQQDDBdSdXNzaWFuIFRydXNzaWFuIFJvb3\ndCBDQTCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAMfFOZ8pUAL3+r2n\nqqE0Zp52selXsKGFYoG0GM5bwz1bSFtCt+AZQMhkWQheI3poZAToYJu69pHLKS6Q\nXBiwBC1cvzYmUYKMYZC7jE5YhEU2bSL0mX7NaMxMDmH2/NwuOVRj8OImVa5s1F4U\nzn4Kv3PFlDBjjSjXKVY9kmjUBsXQrIHeaqmUIsPIlNWUnimXS0I0abExqkbdrXbX\nYwCOXhOO2pDUx3ckmJlCMUGacUTnylyQW2VsJIyIGA8V0xzdaeUXg0VZ6ZmNUr5Y\nBer/EAOLPb8NYpsAhJe2mXjMB/J9HNsoFMBFJ0lLOT/+dQvjbdRZoOT8eqJpWnVD\nU+QL/qEZnz57N88OWM3rabJkRNdU/Z7x5SFIM9FrqtN8xewsiBWBI0K6XFuOBOTD\n4V08o4TzJ8+Ccq5XlCUW2L48pZNCYuBDfBh7FxkB7qDgGDiaftEkZZfApRg2E+M9\nG8wkNKTPLDc4wH0FDTijhgxR3Y4PiS1HL2Zhw7bD3CbslmEGgfnnZojNkJtcLeBH\nBLa52/dSwNU4WWLubaYSiAmA9IUMX1/RpfpxOxd4Ykmhz97oFbUaDJFipIggx5sX\nePAlkTdWnv+RWBxlJwMQ25oEHmRguNYf4Zr/Rxr9cS93Y+mdXIZaBEE0KS2iLRqa\nOiWBki9IMQU4phqPOBAaG7A+eP8PAgMBAAGjZjBkMB0GA1UdDgQWBBTh0YHlzlpf\nBKrS6badZrHF+qwshzAfBgNVHSMEGDAWgBTh0YHlzlpfBKrS6badZrHF+qwshzAS\nBgNVHRMBAf8ECDAGAQH/AgEEMA4GA1UdDwEB/wQEAwIBhjANBgkqhkiG9w0BAQsF\nAAOCAgEAALIY1wkilt/urfEVM5vKzr6utOeDWCUczmWX/RX4ljpRdgF+5fAIS4vH\ntmXkqpSCOVeWUrJV9QvZn6L227ZwuE15cWi8DCDal3Ue90WgAJJZMfTshN4OI8cq\nW9E4EG9wglbEtMnObHlms8F3CHmrw3k6KmUkWGoa+/ENmcVl68u/cMRl1JbW2bM+\n/3A+SAg2c6iPDlehczKx2oa95QW0SkPPWGuNA/CE8CpyANIhu9XFrj3RQ3EqeRcS\nAQQod1RNuHpfETLU/A2gMmvn/w/sx7TB3W5BPs6rprOA37tutPq9u6FTZOcG1Oqj\nC/B7yTqgI7rbyvox7DEXoX7rIiEqyNNUguTk/u3SZ4VXE2kmxdmSh3TQvybfbnXV\n4JbCZVaqiZraqc7oZMnRoWrXRG3ztbnbes/9qhRGI7PqXqeKJBztxRTEVj8ONs1d\nWN5szTwaPIvhkhO3CO5ErU2rVdUr89wKpNXbBODFKRtgxUT70YpmJ46VVaqdAhOZ\nD9EUUn4YaeLaS8AjSF/h7UkjOibNc4qVDiPP+rkehFWM66PVnP1Msh93tc+taIfC\nEYVMxjh8zNbFuoc7fzvvrFILLe7ifvEIUqSVIC/AzplM/Jxw7buXFeGP1qVCBEHq\n391d/9RAfaZ12zkwFsl+IKwE/OZxW8AHa9i1p4GO0YSNuczzEm4=\n-----END CERTIFICATE-----"""

access_token = ""
token_expires_at = 0
RUSSIAN_CA_CERT = RUSSIAN_CA_CERT

async def create_async_generator(
        model: str,
        messages: list,
        stream: bool = True,
        proxy: str = None,
        api_key: str = "YOUR_API_KEY",
        connector: BaseConnector = None,
        scope: str = "GIGACHAT_API_PERS",
        update_interval: float = 0,
        **kwargs
) -> str:
    global access_token, token_expires_at

    model = model
    if not api_key:
        raise ValueError('Missing "api_key"')

    # Create certificate file in cookies directory
    cookies_dir = Path('.')
    cert_file = cookies_dir / 'russian_trusted_root_ca.crt'

    # Write certificate if it doesn't exist
    if not cert_file.exists():
        cert_file.write_text(RUSSIAN_CA_CERT)

    if has_ssl and connector is None:
        ssl_context = ssl.create_default_context(cafile=str(cert_file))
        connector = TCPConnector(ssl_context=ssl_context)

    async with MockClientSession(connector=connector) as session:
        if token_expires_at - int(time.time() * 1000) < 60000:
            async with session.post(url="https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
                                    headers={"Authorization": f"Bearer {api_key}",
                                             "RqUID": str(uuid.uuid4()),
                                             "Content-Type": "application/x-www-form-urlencoded"},
                                    data={"scope": scope}) as response:
                await mock_raise_for_status(response)
                data = await response.json()
            access_token = data['access_token']
            token_expires_at = data['expires_at']

        async with session.post(url="https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
                                headers={"Authorization": f"Bearer {access_token}"},
                                json={
                                    "model": model,
                                    "messages": messages,
                                    "stream": stream,
                                    "update_interval": update_interval,
                                    **kwargs
                                }) as response:
            await mock_raise_for_status(response)
            output = []
            async for line in response.content:
                if not stream:
                    output.append(json.loads(line.decode("utf-8"))['choices'][0]['message']['content'])
                    return ''.join(output)

                if line and line.startswith(b"data:"):
                    line = line[6:-1]  # remove "data: " prefix and "\\n" suffix
                    if line.strip() == b"[DONE]":
                        return ''.join(output)
                    else:
                        msg = json.loads(line.decode("utf-8"))['choices'][0]
                        content = msg['delta']['content']
                        if content:
                            output.append(content)

                        if 'finish_reason' in msg:
                            return ''.join(output)
            return ''.join(output)

async def main():
    messages = [{"role": "user", "content": "Hello, GigaChat!"}]
    result = await create_async_generator(model="GigaChat:latest", messages=messages, api_key="YOUR_API_KEY")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())