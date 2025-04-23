### Как использовать блок кода Lockchat
=========================================================================================

Описание
-------------------------
Блок кода `Lockchat` представляет собой класс `Lockchat`, который является провайдером для работы с API Lockchat. Он позволяет отправлять запросы к API для создания завершений (completions) на основе предоставленных сообщений, используя модели GPT-3.5 Turbo и GPT-4. Класс поддерживает потоковую передачу данных.

Шаги выполнения
-------------------------
1. **Подготовка**:
   - Импортируются необходимые модули: `json`, `requests`, а также типы `Any`, `CreateResult` и `AbstractProvider`.

2. **Определение класса `Lockchat`**:
   - Определяется класс `Lockchat`, наследующийся от `AbstractProvider`.
   - Указываются атрибуты класса:
     - `url` (str): URL для API Lockchat ("http://supertest.lockchat.app").
     - `supports_stream` (bool): Поддержка потоковой передачи данных (True).
     - `supports_gpt_35_turbo` (bool): Поддержка модели GPT-3.5 Turbo (True).
     - `supports_gpt_4` (bool): Поддержка модели GPT-4 (True).

3. **Метод `create_completion`**:
   - Определяется статический метод `create_completion`, который принимает следующие аргументы:
     - `model` (str): Название используемой модели.
     - `messages` (list[dict[str, str]]): Список сообщений для запроса.
     - `stream` (bool): Флаг потоковой передачи данных.
     - `**kwargs` (Any): Дополнительные аргументы, такие как температура.

4. **Подготовка полезной нагрузки (payload)**:
   - Извлекается значение температуры из `kwargs` (по умолчанию 0.7).
   - Формируется словарь `payload` с параметрами запроса: `temperature`, `messages`, `model` и `stream`.

5. **Подготовка заголовков (headers)**:
   - Определяются заголовки `headers` с User-Agent.

6. **Отправка запроса к API**:
   - Отправляется POST-запрос к API Lockchat (`http://supertest.lockchat.app/v1/chat/completions`) с использованием библиотеки `requests`.
   - Передаются `payload` в формате JSON и `headers`.
   - Устанавливается `stream=True` для потоковой передачи данных.

7. **Обработка ответа**:
   - Вызывается `response.raise_for_status()` для проверки статуса ответа.
   - Итерируемся по строкам ответа (`response.iter_lines()`).
   - Если в токене содержится сообщение об ошибке (`b"The model: \`gpt-4\` does not exist"`), выводится сообщение об ошибке и делается повторная попытка запроса с теми же параметрами.
   - Если в токене содержится `b"content"`, токен декодируется из UTF-8, извлекается содержимое из JSON (`token["choices"][0]["delta"].get("content")`).
   - Если содержимое существует, оно возвращается через `yield (token)`.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.deprecated import Lockchat

messages = [
    {"role": "user", "content": "Hello, how are you?"}
]

for token in Lockchat.create_completion(model="gpt-3.5-turbo", messages=messages, stream=True):
    print(token, end="", flush=True)