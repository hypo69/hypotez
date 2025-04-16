# Модуль для отображения вращающегося курсора

## Обзор

Этот модуль предоставляет утилиту для отображения вращающегося курсора в консоли, чтобы имитировать процесс загрузки или ожидания.

## Подробней

Модуль предоставляет функции для создания и отображения вращающегося курсора в консоли.  Это может быть полезно для визуального отображения длительных процессов, чтобы пользователь понимал, что программа не зависла, а продолжает работать.

## Функции

### `spinning_cursor`

**Назначение**: Генератор для вращающегося курсора, который циклически перебирает символы |, /, -, \\.

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

**Возвращает**:

-   `str`: Следующий символ в последовательности курсора.

**Как работает функция**:

1.  Определяет последовательность символов для вращения: `|/-\\\`.
2.  Использует бесконечный цикл `while True`, чтобы генератор работал непрерывно.
3.  Внутри цикла перебирает символы последовательности и возвращает их по одному с помощью `yield`.

**Примеры**:

```python
>>> cursor = spinning_cursor()
>>> next(cursor)  # '|'
>>> next(cursor)  # '/'
>>> next(cursor)  # '-'
>>> next(cursor)  # '\\'
```

### `show_spinner`

**Назначение**: Отображает вращающийся курсор в консоли в течение заданного времени.

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

**Параметры**:

-   `duration` (float): Продолжительность работы курсора в секундах. По умолчанию 5.0.
-   `delay` (float): Задержка между каждым шагом вращения в секундах. По умолчанию 0.1.

**Как работает функция**:

1.  Создает генератор `spinner` с использованием функции `spinning_cursor()`.
2.  Вычисляет время окончания работы курсора (`end_time`).
3.  Использует цикл `while time.time() < end_time`, чтобы отображать курсор в течение заданного времени.
4.  Внутри цикла:
    -   Выводит следующий символ курсора в консоль с помощью `sys.stdout.write(next(spinner))`.
    -   Принудительно отправляет вывод в консоль с помощью `sys.stdout.flush()`.
    -   Приостанавливает выполнение на заданное время задержки с помощью `time.sleep(delay)`.
    -   Удаляет предыдущий символ курсора из консоли с помощью `sys.stdout.write('\b')`.

**Примеры**:

```python
>>> show_spinner(duration=3.0, delay=0.2)  # Отображает курсор в течение 3 секунд
```

## Запуск модуля

В блоке `if __name__ == "__main__":` демонстрируется пример использования функции `show_spinner`.

```python
if __name__ == "__main__":
    # Example usage of the spinner in a script
    print("Spinner for 5 seconds:")
    show_spinner(duration=5.0, delay=0.1)
    print("\\nDone!")
```

При запуске этого скрипта в консоли будет отображаться вращающийся курсор в течение 5 секунд, после чего появится сообщение "Done!".