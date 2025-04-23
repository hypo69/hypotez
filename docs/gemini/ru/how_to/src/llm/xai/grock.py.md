### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет класс `XAI` для взаимодействия с API x.ai. Он включает методы для отправки запросов на завершение чата как в непотоковом, так и в потоковом режимах. Класс использует библиотеку `requests` для выполнения HTTP-запросов и обрабатывает ответы API.

Шаги выполнения
-------------------------
1. **Инициализация класса `XAI`**:
   - Создается экземпляр класса `XAI` с использованием API-ключа.
   - Устанавливаются базовый URL API и заголовки для аутентификации и указания типа контента.

2. **Отправка запроса к API (`_send_request`)**:
   - Метод `_send_request` отправляет HTTP-запрос к указанной конечной точке API.
   - Определяется URL на основе базового URL и переданной конечной точки.
   - Выполняется запрос с использованием библиотеки `requests`.
   - Если статус ответа не 2xx, выбрасывается исключение `HTTPError`.
   - Возвращается JSON-ответ от API.

3. **Запрос на завершение чата (`chat_completion`)**:
   - Метод `chat_completion` отправляет запрос на завершение чата в API.
   - Формируются данные запроса, включающие сообщения, модель, флаг потоковой передачи и температуру.
   - Вызывается метод `_send_request` для отправки POST-запроса к конечной точке `chat/completions`.
   - Возвращается ответ от API.

4. **Запрос на завершение чата с потоковой передачей (`stream_chat_completion`)**:
   - Метод `stream_chat_completion` отправляет запрос на завершение чата с потоковой передачей.
   - Формируются данные запроса аналогично `chat_completion`, но с `stream=True`.
   - Выполняется POST-запрос к конечной точке `chat/completions` с использованием `requests.post` и `stream=True`.
   - Возвращается итератор строк из ответа, который позволяет читать данные по частям.

Пример использования
-------------------------

```python
import requests
import json

class XAI:
    def __init__(self, api_key: str):
        """
        Инициализация класса XAI.

        Args:
            api_key (str): Ключ API для аутентификации.
        """
        self.api_key = api_key
        self.base_url = "https://api.x.ai/v1"  # Базовый URL API
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _send_request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """
        Отправка запроса к API x.ai.

        Args:
            method (str): Метод HTTP (GET, POST, PUT, DELETE).
            endpoint (str): Конечная точка API.
            data (dict, optional): Данные для отправки в теле запроса (для POST и PUT). Defaults to None.

        Returns:
            dict: Ответ от API.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, headers=self.headers, json=data)
        response.raise_for_status()  # Выбрасывает исключение, если статус ответа не 2xx
        return response.json()

    def chat_completion(self, messages: list, model: str = "grok-beta", stream: bool = False, temperature: float = 0) -> dict:
        """
        Запрос на завершение чата.

        Args:
            messages (list): Список сообщений для чата.
            model (str, optional): Модель для использования. Defaults to "grok-beta".
            stream (bool, optional): Флаг для включения потоковой передачи. Defaults to False.
            temperature (float, optional): Температура для генерации ответа. Defaults to 0.

        Returns:
            dict: Ответ от API.
        """
        endpoint = "chat/completions"
        data = {
            "messages": messages,
            "model": model,
            "stream": stream,
            "temperature": temperature
        }
        response = self._send_request("POST", endpoint, data)
        return response

    def stream_chat_completion(self, messages: list, model: str = "grok-beta", temperature: float = 0) -> iter:
        """
        Запрос на завершение чата с потоковой передачей.

        Args:
            messages (list): Список сообщений для чата.
            model (str, optional): Модель для использования. Defaults to "grok-beta".
            temperature (float, optional): Температура для генерации ответа. Defaults to 0.

        Returns:
            iter: Поток ответов от API.
        """
        endpoint = "chat/completions"
        data = {
            "messages": messages,
            "model": model,
            "stream": True,
            "temperature": temperature
        }
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data, stream=True)
        response.raise_for_status()
        return response.iter_lines(decode_unicode=True)

# Пример использования класса XAI
if __name__ == "__main__":
    api_key = "your_api_key_here"  # Функция заменяет на ваш реальный API-ключ
    xai = XAI(api_key)

    messages = [
        {
            "role": "system",
            "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."
        },
        {
            "role": "user",
            "content": "What is the answer to life and universe?"
        }
    ]

    # Непотоковый запрос
    completion_response = xai.chat_completion(messages)
    print("Non-streaming response:", completion_response)

    # Потоковый запрос
    stream_response = xai.stream_chat_completion(messages)
    print("Streaming response:")
    for line in stream_response:
        if line.strip():
            print(json.loads(line))