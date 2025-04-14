# Модуль Custom для работы с пользовательскими провайдерами

## Обзор

Модуль `Custom` предназначен для определения пользовательских провайдеров, использующих API OpenAI. Он содержит классы `Custom` и `Feature`, которые наследуются от `OpenaiTemplate`.

## Подробней

Этот модуль предоставляет базовую структуру для создания пользовательских провайдеров, совместимых с API OpenAI. Он определяет основные атрибуты и параметры, необходимые для работы с этими провайдерами.
Классы `Custom` и `Feature` позволяют гибко настраивать поведение и характеристики провайдеров.

## Классы

### `Custom`

**Описание**: Базовый класс для пользовательских провайдеров.

**Принцип работы**:
Класс `Custom` наследуется от `OpenaiTemplate` и определяет основные параметры для работы с пользовательскими провайдерами, использующими API OpenAI.
Он задает значения по умолчанию для таких атрибутов, как `label`, `working`, `needs_auth`, `api_base` и `sort_models`.

**Атрибуты**:
- `label` (str): Метка провайдера ("Custom Provider").
- `working` (bool): Указывает, работает ли провайдер (True).
- `needs_auth` (bool): Указывает, требуется ли аутентификация (False).
- `api_base` (str): Базовый URL API ("http://localhost:8080/v1").
- `sort_models` (bool): Указывает, нужно ли сортировать модели (False).

### `Feature`

**Описание**: Класс для провайдеров с дополнительными функциями.

**Принцип работы**:
Класс `Feature` наследуется от `Custom` и предназначен для создания провайдеров с расширенным функционалом.
В данном случае, он переопределяет атрибут `working` на `False`, указывая, что провайдер не работает.

**Атрибуты**:
- `label` (str): Метка провайдера ("Feature Provider").
- `working` (bool): Указывает, работает ли провайдер (False).

```python
from __future__ import annotations

from ..template import OpenaiTemplate

class Custom(OpenaiTemplate):
    label = "Custom Provider"
    working = True
    needs_auth = False
    api_base = "http://localhost:8080/v1"
    sort_models = False

class Feature(Custom):
    label = "Feature Provider"
    working = False