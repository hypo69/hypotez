# Модуль для работы с Perplexity API
=========================================

Модуль содержит класс `PerplexityApi`, который используется для взаимодействия с Perplexity AI.
Этот модуль предоставляет интерфейс для доступа к различным моделям Perplexity AI, включая `llama-3-sonar-large-32k-online` и другие.

## Обзор

Модуль предназначен для интеграции с API Perplexity AI, предоставляя удобный интерфейс для аутентификации и выполнения запросов к различным моделям. Он наследует базовый класс `OpenaiTemplate` и реализует специфические параметры и настройки для Perplexity API.

## Подробней

Этот модуль позволяет пользователям взаимодействовать с различными моделями Perplexity AI, такими как `llama-3-sonar-small-32k-chat`, `llama-3-sonar-large-32k-chat`, `llama-3-sonar-large-32k-online`, `llama-3-8b-instruct` и `llama-3-70b-instruct`. Он предоставляет возможность устанавливать соединение с API Perplexity AI, используя аутентификацию, и отправлять запросы для получения ответов от этих моделей.

## Классы

### `PerplexityApi`

**Описание**: Класс `PerplexityApi` предоставляет интерфейс для взаимодействия с API Perplexity AI.

**Наследует**:
- `OpenaiTemplate`: Этот класс наследует функциональность из `OpenaiTemplate`, что позволяет ему использовать общие методы и атрибуты для взаимодействия с API.

**Атрибуты**:
- `label` (str): Метка для идентификации провайдера API ("Perplexity API").
- `url` (str): URL главной страницы Perplexity AI ("https://www.perplexity.ai").
- `login_url` (str): URL страницы настроек API для получения ключа ("https://www.perplexity.ai/settings/api").
- `working` (bool): Указывает, работает ли API (True).
- `needs_auth` (bool): Указывает, требуется ли аутентификация для доступа к API (True).
- `api_base` (str): Базовый URL для API Perplexity AI ("https://api.perplexity.ai").
- `default_model` (str): Модель, используемая по умолчанию ("llama-3-sonar-large-32k-online").
- `models` (List[str]): Список поддерживаемых моделей API.

**Методы**:
- Отсутствуют явно определенные методы, так как класс наследует их из `OpenaiTemplate`.

## Функции

В данном коде функции отсутствуют.