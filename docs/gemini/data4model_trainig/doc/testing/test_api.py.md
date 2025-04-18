# Модуль для тестирования API

## Обзор

Модуль `src.endpoints.gpt4free/etc/testing/test_api.py` предназначен для тестирования API.

## Подробней

Модуль содержит примеры использования API для создания завершений текста (text completions) как в потоковом, так и в непотоковом режимах.

## Переменные

*   `openai.api_key` (str): Ключ API OpenAI (замените на свой реальный токен).
*   `openai.api_base` (str): Базовый URL API (значение: `"http://localhost:1337/v1"`).

## Функции

### `main`

**Назначение**: Основная функция для тестирования API.

**Как работает функция**:

1.  Отправляет запрос к OpenAI ChatCompletion API с указанием модели `gpt-3.5-turbo` и сообщением "write a poem about a tree".
2.  Проверяет, является ли ответ словарем или потоком:

    *   Если ответ - словарь (непотоковый режим), извлекает содержимое сообщения и выводит его в консоль.
    *   Если ответ - поток (потоковый режим), итерируется по токенам и выводит их содержимое в консоль.