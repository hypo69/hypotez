# Модуль для создания файла OpenAPI

## Обзор

Модуль `src.endpoints.gpt4free/g4f/openapi.py` предназначен для создания файла OpenAPI (Swagger) для API.

## Подробней

Модуль создает файл `openapi.json`, содержащий описание API в формате OpenAPI.

## Переменные

*   `app` (FastAPI): Экземпляр FastAPI-приложения.
*   `data` (str): JSON-представление схемы OpenAPI.

## Как работает модуль

1.  Импортирует `create_app` из `g4f.api`.
2.  Создает экземпляр FastAPI-приложения с помощью `create_app()`.
3.  Создает JSON-представление схемы OpenAPI, используя `app.openapi()`.
4.  Записывает JSON-данные в файл `openapi.json`.
5.  Выводит размер файла `openapi.json` в консоль.