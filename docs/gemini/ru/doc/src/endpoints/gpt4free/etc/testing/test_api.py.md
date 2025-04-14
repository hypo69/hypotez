# Модуль для тестирования API OpenAI

## Обзор

Модуль `test_api.py` предназначен для тестирования API OpenAI. Он включает в себя настройку API ключа и базового URL, а также функцию `main`, демонстрирующую взаимодействие с API для получения поэтического ответа на заданный вопрос.

## Подробнее

Данный модуль позволяет проверить работоспособность API OpenAI, включая возможность потоковой передачи данных. Он настраивает API ключ и базовый URL, а затем отправляет запрос на генерацию стихов о дереве. В зависимости от типа ответа (потоковый или нет), он обрабатывает и выводит полученный результат.

## Функции

### `main`

```python
def main():
    """
    Отправляет запрос в API OpenAI для генерации стихов о дереве и обрабатывает ответ.

    Args:
        None

    Returns:
        None

    Raises:
        openai.error.OpenAIError: Если возникает ошибка при взаимодействии с API OpenAI.

    Как работает функция:
    - Настраивает параметры запроса к API OpenAI, включая модель и сообщение для генерации стихов.
    - Отправляет запрос к API OpenAI на создание чата.
    - Проверяет, является ли ответ потоковым или нет.
    - Если ответ не потоковый, выводит содержимое первого выбора.
    - Если ответ потоковый, итерируется по токенам и выводит содержимое каждого токена.
    """
    ...
```

## Параметры OpenAI

- `openai.api_key`: API ключ для доступа к OpenAI.
- `openai.api_base`: Базовый URL для доступа к API OpenAI, например, для локальной разработки.

## Примеры

Пример использования функции `main`:

```python
import openai

# Замените на ваш актуальный токен
openai.api_key = "YOUR_HUGGING_FACE_TOKEN"

# Установите базовый URL API, если необходимо, например, для локальной среды разработки
openai.api_base = "http://localhost:1337/v1"

def main():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "write a poem about a tree"}],
        stream=True,
    )
    if isinstance(response, dict):
        # Not streaming
        print(response.choices[0].message.content)
    else:
        # Streaming
        for token in response:
            content = token["choices"][0]["delta"].get("content")
            if content is not None:
                print(content, end="", flush=True)

if __name__ == "__main__":
    main()