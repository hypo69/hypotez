# Модуль определения типов данных

## Обзор

Модуль `typing.py` предназначен для определения пользовательских типов данных и импорта необходимых элементов для работы с типами в Python.

## Подробнее

В данном модуле определен новый тип `sha256` на основе строки, который используется для представления SHA256 хешей. Также импортируются различные типы из модуля `typing` для удобства работы с аннотациями типов.

## Типы

### `sha256`

**Описание**: Тип, представляющий собой строку, содержащую SHA256 хеш.
**Принцип работы**:
   - Новый тип `sha256` создается с использованием `NewType` из модуля `typing`. Это позволяет создать логически отдельный тип, который все еще является строкой, но может использоваться для более точной типизации.

## Параметры типа

- `sha_256_hash` (str): Строка, представляющая SHA256 хеш.

```python
from typing import Dict, NewType, Union, Optional, List, get_type_hints
sha256 = NewType('sha_256_hash', str)