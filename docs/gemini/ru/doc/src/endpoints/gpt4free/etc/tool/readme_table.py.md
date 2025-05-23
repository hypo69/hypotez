# Модуль для генерации таблицы Readme

## Обзор

Модуль генерирует таблицу README для документации проекта `g4f`. Таблица содержит информацию о доступных моделях, провайдерах и их статусе.

## Подробней

Этот модуль использует библиотеку `g4f` для сбора информации о доступных провайдерах и моделях. Он анализирует список провайдеров, определенных в `__providers__`, и формирует таблицу, включающую:

- Название провайдера
- Статус провайдера (активен, неактивен, неизвестен)
- Веб-сайт провайдера
- Требуется ли аутентификация
- Поддерживает ли провайдер потоковую передачу (Streaming)
- Поддерживает ли провайдер системные сообщения
- Поддерживает ли провайдер историю сообщений
- Доступные модели (с разбивкой по категориям)

## Функции

### `test_async`

**Назначение**: Асинхронно проверяет доступность и работоспособность провайдера.

**Параметры**:

- `provider` (`ProviderType`): Провайдер для тестирования.

**Возвращает**:

- `bool`: `True`, если провайдер доступен и работает, `False` в противном случае.

**Как работает функция**:

- Функция отправляет тестовое сообщение провайдеру и ожидает ответа в течение 30 секунд.
- Если ответ получен, функция возвращает `True`.
- Если возникает ошибка, функция логирует ее с использованием `debug.logging` и возвращает `False`.

### `test_async_list`

**Назначение**: Тестирует список провайдеров асинхронно.

**Параметры**:

- `providers` (`list[ProviderType]`): Список провайдеров для тестирования.

**Возвращает**:

- `list`: Список результатов тестирования провайдеров.

**Как работает функция**:

- Функция запускает `test_async` для каждого провайдера в списке с использованием `asyncio.run`.
- Она собирает результаты в список и возвращает его.

### `print_providers`

**Назначение**: Генерирует строки таблицы README для провайдеров.

**Параметры**: 

- `None`

**Возвращает**:

- `list`: Список строк таблицы.

**Как работает функция**:

- Функция перебирает все провайдеры из `__providers__`.
- Для каждого провайдера она собирает информацию, такую как название, статус, веб-сайт, аутентификация, потоковая передача, системные сообщения, история сообщений и доступные модели.
- Она форматирует информацию в строки таблицы и добавляет их в список.
- В конце возвращает список строк таблицы.

### `print_models`

**Назначение**: Генерирует строки таблицы README для моделей.

**Параметры**: 

- `None`

**Возвращает**:

- `list`: Список строк таблицы.

**Как работает функция**:

- Функция перебирает все модели, доступные в `g4f.models.ModelUtils.convert`.
- Для каждой модели она получает информацию, такую как название, базовый провайдер, провайдер, веб-сайт.
- Она форматирует информацию в строки таблицы и добавляет их в список.
- В конце возвращает список строк таблицы.

### `print_image_models`

**Назначение**: Генерирует строки таблицы README для моделей, поддерживающих обработку изображений.

**Параметры**: 

- `None`

**Возвращает**:

- `list`: Список строк таблицы.

**Как работает функция**:

- Функция перебирает все провайдеры, поддерживающие обработку изображений.
- Для каждого провайдера она получает информацию, такую как название, веб-сайт, доступные модели для обработки изображений и поддерживает ли провайдер загрузку изображений.
- Она форматирует информацию в строки таблицы и добавляет их в список.
- В конце возвращает список строк таблицы.


## Примеры

```python
# Пример использования функции print_providers:
provider_table = print_providers()
print("\n".join(provider_table))

# Пример использования функции print_models:
models_table = print_models()
print("\n".join(models_table))

# Пример использования функции print_image_models:
image_models_table = print_image_models()
print("\n".join(image_models_table))
```