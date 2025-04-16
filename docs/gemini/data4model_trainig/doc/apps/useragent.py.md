# Модуль для получения User-Agent

## Обзор

Модуль `src.endpoints.bots.telegram.movie_bot-main/apps/useragent.py` предназначен для получения случайного User-Agent.

## Подробней

Модуль предоставляет функцию `get_useragent`, которая возвращает случайный User-Agent из списка.

## Функции

### `get_useragent`

```python
def get_useragent():
    return random.choice(_useragent_list)
```

**Назначение**: Возвращает случайный User-Agent из списка.

**Возвращает**:

*   `str`: Случайный User-Agent.

**Как работает функция**:

1.  Использует функцию `random.choice` для выбора случайного User-Agent из списка `_useragent_list`.

## Переменные

*   `_useragent_list` (list): Список User-Agent.

**Описание списка `_useragent_list`**:

Список содержит различные User-Agent, используемые для имитации запросов от разных браузеров и операционных систем.