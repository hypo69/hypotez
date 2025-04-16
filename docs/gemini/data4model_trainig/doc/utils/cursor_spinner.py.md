# Модуль для отображения вращающегося курсора

## Обзор

Этот модуль предоставляет утилиту для отображения вращающегося курсора в консоли, чтобы имитировать процесс загрузки или ожидания.

## Подробнее

Модуль содержит функции для создания и отображения вращающегося курсора, который циклически изменяет символы `|`, `/`, `-`, `\`. Это может быть полезно для визуальной индикации выполнения длительных операций в консольных приложениях.

## Функции

### `spinning_cursor`

```python
def spinning_cursor():
    """ Generator for a spinning cursor that cycles through |, /, -, \\ symbols.
    
    Yields:
        str: The next symbol in the cursor sequence.
    
    Example:
        >>> cursor = spinning_cursor()
        >>> next(cursor)  # '|'
        >>> next(cursor)  # '/'
        >>> next(cursor)  # '-'
        >>> next(cursor)  # '\\'
    """
    ...
```

**Назначение**:
Генератор для вращающегося курсора, который циклически проходит через символы |, /, -, \\.

**Возвращает**:
- `str`: Следующий символ в последовательности курсора.

**Как работает функция**:
1. Определяет бесконечный цикл `while True`.
2. Внутри цикла перебирает символы `'|/-\\'`.
3. Использует `yield`, чтобы вернуть каждый символ по очереди при каждом вызове `next()`.

**Примеры**:

```python
cursor = spinning_cursor()
next(cursor)  # '|'
next(cursor)  # '/'
```

### `show_spinner`

```python
def show_spinner(duration: float = 5.0, delay: float = 0.1):
    """ Shows a spinning cursor in the console for a specified duration.
    
    Args:
        duration (float): How long the spinner should run (in seconds). Defaults to 5.0.
        delay (float): Delay between each spin (in seconds). Defaults to 0.1.
    
    Example:
        >>> show_spinner(duration=3.0, delay=0.2)  # Shows a spinner for 3 seconds
    """
    ...
```

**Назначение**:
Отображает вращающийся курсор в консоли в течение указанного времени.

**Параметры**:
- `duration` (float): Как долго должен отображаться курсор (в секундах). По умолчанию 5.0.
- `delay` (float): Задержка между каждым вращением (в секундах). По умолчанию 0.1.

**Возвращает**:
- None

**Как работает функция**:
1. Создает генератор вращающегося курсора `spinning_cursor()`.
2. Определяет время окончания отображения курсора `end_time`.
3. Пока текущее время меньше `end_time`:
    - Выводит следующий символ из генератора `spinner`.
    - Принудительно выводит символ в консоль с помощью `sys.stdout.flush()`.
    - Делает паузу на время `delay`.
    - Использует символ возврата каретки `\b` для перезаписи предыдущего символа.

**Примеры**:

```python
show_spinner(duration=3.0, delay=0.2)  # Отображает курсор в течение 3 секунд с задержкой 0.2 секунды
```

## Переменные

Отсутствуют

## Запуск

Для использования данного модуля необходимо вызвать функцию `show_spinner` с указанием продолжительности отображения курсора и задержки между вращениями.

```python
from src.utils.cursor_spinner import show_spinner

print("Loading...")
show_spinner(duration=5.0, delay=0.1)
print("Done!")