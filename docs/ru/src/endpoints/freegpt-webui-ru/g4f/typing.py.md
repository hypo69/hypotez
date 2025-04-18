# Модуль определения типов данных

## Обзор

Модуль содержит определения пользовательских типов данных, используемых в проекте, а также необходимые импорты для работы с типами. В частности, определяется тип `sha256` для представления хешей SHA256.

## Подробнее

Этот модуль предназначен для централизованного определения типов, что облегчает поддержку и рефакторинг кода. Использование `NewType` позволяет создавать новые типы, основанные на существующих, без дополнительных затрат во время выполнения. Это улучшает читаемость кода и позволяет статическим анализаторам лучше проверять типы.

## Типы

### `sha256`

**Описание**: Тип для представления SHA256 хешей.

**Принцип работы**:

Тип `sha256` создается с использованием `NewType` на основе типа `str`. Это означает, что переменная типа `sha256` ведет себя как строка, но позволяет статическим анализаторам отличать её от обычных строк, что улучшает безопасность и надежность кода.

```python
sha256 = NewType('sha_256_hash', str)
```

## Переменные

- `sha256` (NewType): Определяет новый тип `sha256` как псевдоним для `str`, используемый для представления SHA256 хешей.

## Импорты

- `typing.Dict`: Используется для работы со словарями, где ключи и значения имеют определенные типы.
- `typing.NewType`: Используется для создания новых типов на основе существующих.
- `typing.Union`: Используется для указания, что переменная может иметь один из нескольких типов.
- `typing.Optional`: Используется для указания, что переменная может иметь значение определенного типа или `None`.
- `typing.List`: Используется для работы со списками, содержащими элементы определенного типа.
- `typing.get_type_hints`: Используется для получения аннотаций типов для функций, методов и классов.