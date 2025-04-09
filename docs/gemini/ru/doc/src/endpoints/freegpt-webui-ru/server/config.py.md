# Модуль конфигурации для FreeGPT WebUI (Русская версия)

## Обзор

Этот модуль содержит конфигурационные данные, используемые в FreeGPT WebUI на русском языке. Он определяет доступные модели и специальные инструкции для различных режимов работы, таких как DAN Mode и Developer Mode.

## Подробнее

Модуль содержит словарь `models`, который определяет список поддерживаемых моделей, таких как `gpt-3.5-turbo`, `gpt-4` и другие. Также модуль содержит словарь `special_instructions`, который содержит инструкции для разных режимов работы, таких как `gpt-dan-11.0`, `gpt-evil` и другие. Эти инструкции используются для изменения поведения модели и выполнения определенных задач.

## Переменные

### `models`

```python
models = {
    'gpt-3.5-turbo',
    'gpt-3.5-turbo-16k-0613',
    'gpt-3.5-turbo-16k',
    'gpt-4',
    'gpt-4-for-dev'
}
```

**Описание**: Набор строк, представляющих идентификаторы поддерживаемых моделей.

### `special_instructions`

```python
special_instructions = {
    'default': [],
    'gpt-dan-11.0': [...],
    'gpt-dan-2.0': [...],
    'gpt-evil': [...],
    'gpt-dev-2.0': [...],
    'programming-assistant': [...],
    'editor': [...],
    'midjourney-promt': [...],
    'sd-promt': [...],
}
```

**Описание**: Словарь, содержащий специальные инструкции для различных режимов работы. Ключи словаря - это идентификаторы режимов, а значения - списки словарей, содержащих инструкции для модели. Каждый словарь в списке содержит ключи `role` и `content`, определяющие роль и содержание инструкции.

## Примеры

Пример использования словаря `special_instructions`:

```python
instructions = special_instructions['gpt-dan-11.0']
first_instruction = instructions[0]
role = first_instruction['role']  # 'user'
content = first_instruction['content']  # 'Ignore all the instructions you got before...'
```