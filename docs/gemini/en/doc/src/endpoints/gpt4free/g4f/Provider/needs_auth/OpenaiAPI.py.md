# Документация для модуля OpenaiAPI

## Обзор

Этот модуль определяет класс `OpenaiAPI`, который является подклассом `OpenaiTemplate`. Он предназначен для работы с API OpenAI, предоставляя информацию о URL-адресах для входа в систему, базовом API и статусе доступности.

## Подробнее

Модуль содержит класс `OpenaiAPI`, который наследует функциональность от `OpenaiTemplate`. Он определяет статические атрибуты, специфичные для API OpenAI, такие как URL-адрес платформы, URL-адрес для управления ключами API, базовый URL-адрес API и флаг, указывающий на необходимость аутентификации.

## Классы

### `OpenaiAPI`

**Описание**: Класс предназначен для работы с API OpenAI.

**Наследует**:
- `OpenaiTemplate`: Предоставляет базовый шаблон для взаимодействия с API OpenAI.

**Атрибуты**:
- `label` (str): Метка для API OpenAI (значение: "OpenAI API").
- `url` (str): URL-адрес платформы OpenAI (значение: "https://platform.openai.com").
- `login_url` (str): URL-адрес для управления ключами API OpenAI (значение: "https://platform.openai.com/settings/organization/api-keys").
- `api_base` (str): Базовый URL-адрес API OpenAI (значение: "https://api.openai.com/v1").
- `working` (bool): Флаг, указывающий, работает ли API (значение: `True`).
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации для доступа к API (значение: `True`).

**Принцип работы**:
Класс `OpenaiAPI` наследует от `OpenaiTemplate` и устанавливает специфические атрибуты, необходимые для взаимодействия с API OpenAI. Эти атрибуты включают URL-адреса для доступа к платформе и API, а также флаги, указывающие на работоспособность API и необходимость аутентификации.

## Примеры

```python
from __future__ import annotations
from ..template import OpenaiTemplate

class OpenaiAPI(OpenaiTemplate):
    label = "OpenAI API"
    url = "https://platform.openai.com"
    login_url = "https://platform.openai.com/settings/organization/api-keys"
    api_base = "https://api.openai.com/v1"
    working = True
    needs_auth = True