# Модуль для тестирования Interference API

## Обзор

Модуль `src.endpoints.gpt4free/etc/testing/test_interference.py` предназначен для тестирования Interference API.

## Подробней

Модуль отправляет запрос к OpenAI ChatCompletion API через Interference API и выводит полученный ответ в консоль.

## Переменные

*   `openai.api_key` (str): Ключ API OpenAI (значение: `""`).
*   `openai.api_base` (str): Базовый URL API (значение: `"http://localhost:1337"`).
*   `response` (object): Объект ответа от API.

## Как работает модуль

1.  Устанавливает ключ API и базовый URL для OpenAI.
2.  Отправляет запрос к OpenAI ChatCompletion API с указанием модели `gpt-3.5-turbo` и сообщением "write a poem about a tree".
3.  Проверяет, является ли ответ словарем или потоком:

    *   Если ответ - словарь (непотоковый режим), извлекает содержимое сообщения и выводит его в консоль.
    *   Если ответ - поток (потоковый режим), итерируется по токенам и выводит их содержимое в консоль.