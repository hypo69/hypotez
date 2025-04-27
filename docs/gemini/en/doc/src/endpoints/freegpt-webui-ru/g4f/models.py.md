# Модуль `models`
## Обзор

Модуль `models` предоставляет определения для различных моделей искусственного интеллекта, используемых в проекте. 
Он содержит класс `Model`, который определяет атрибуты для каждой модели, такие как название модели, 
базовый провайдер и лучший провайдер.

## Детали

Модуль `models` используется для определения и управления доступными моделями AI. Он предоставляет 
список моделей, каждая из которых имеет уникальное название, базовый провайдер, 
лучший провайдер и, возможно, список лучших провайдеров. 
Этот модуль играет важную роль в выборе подходящих моделей AI 
для выполнения различных задач в проекте. 

## Классы

### `class Model`

**Описание**: 
Этот класс определяет атрибуты для различных моделей AI. 
Он используется для хранения информации о каждой модели, 
включая ее название, базовый провайдер и лучший провайдер.

**Атрибуты**:

- `name` (str): Название модели AI.
- `base_provider` (str): Базовый провайдер модели AI.
- `best_provider` (`Provider.Provider`): Лучший провайдер для модели AI.

**Примеры**:

```python
# Пример создания экземпляра класса Model для модели "gpt-3.5-turbo"
gpt_35_turbo_model = Model.gpt_35_turbo

# Доступ к атрибутам модели
print(gpt_35_turbo_model.name)  # Выведет "gpt-3.5-turbo"
print(gpt_35_turbo_model.base_provider)  # Выведет "openai"
print(gpt_35_turbo_model.best_provider)  # Выведет "Mishalsgpt"
```

## Класс Методы

### `ModelUtils.convert`

**Описание**: 
Этот словарь предоставляет соответствие между названиями моделей AI 
и их соответствующими объектами класса `Model`.

**Примеры**:

```python
# Получение объекта модели по ее названию
model_object = ModelUtils.convert['gpt-3.5-turbo']

# Доступ к атрибутам модели
print(model_object.name)  # Выведет "gpt-3.5-turbo"
print(model_object.base_provider)  # Выведет "openai"
print(model_object.best_provider)  # Выведет "Mishalsgpt"
```

## Детали Параметров

- `name` (str): Название модели AI.
- `base_provider` (str): Базовый провайдер модели AI.
- `best_provider` (`Provider.Provider`): Лучший провайдер для модели AI.
- `best_providers` (list): Список лучших провайдеров для модели AI.

## Примеры

```python
# Пример использования словаря convert для получения объекта модели
model_name = 'gpt-3.5-turbo'
model_object = ModelUtils.convert[model_name]

# Доступ к атрибутам модели
print(model_object.name)  # Выведет "gpt-3.5-turbo"
print(model_object.base_provider)  # Выведет "openai"
print(model_object.best_provider)  # Выведет "Mishalsgpt"

# Пример использования класса Model для определения модели
model = Model.gpt_35_turbo

# Доступ к атрибутам модели
print(model.name)  # Выведет "gpt-3.5-turbo"
print(model.base_provider)  # Выведет "openai"
print(model.best_provider)  # Выведет "Mishalsgpt"
```