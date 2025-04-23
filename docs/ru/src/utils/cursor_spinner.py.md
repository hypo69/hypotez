# Модуль `cursor_spinner`

## Обзор

Модуль `cursor_spinner` предоставляет инструменты для отображения анимированного курсора в консоли, имитирующего процесс загрузки или ожидания. Он включает в себя генератор для создания последовательности символов вращающегося курсора и функцию для отображения этого курсора в течение заданного времени.

## Подробнее

Этот модуль полезен для визуального отображения активности программы в консольных приложениях, когда требуется показать пользователю, что происходит длительный процесс. Он использует символы `|`, `/`, `-`, `\` для создания анимации вращения.

## Функции

### `spinning_cursor`

#### Назначение:
Генератор для циклического перебора символов `|`, `/`, `-`, `\` вращающегося курсора.

#### Как работает функция:
Функция `spinning_cursor` является генератором, который бесконечно выдает символы из строки `'|/-\\'`. При каждом вызове `next(spinning_cursor())` возвращается следующий символ из этой последовательности.

```python
def spinning_cursor():
    """ Генератор для циклического перебора символов |, /, -, \\ вращающегося курсора.
    
    Yields:
        str: The next symbol in the cursor sequence.
    
    Example:
        >>> cursor = spinning_cursor()
        >>> next(cursor)  # '|'
        >>> next(cursor)  # '/'
        >>> next(cursor)  # '-'
        >>> next(cursor)  # '\\'
    """
    while True:
        for cursor in '|/-\\':
            yield cursor
```

#### Возвращает:
- `str`: Следующий символ в последовательности курсора.

#### Примеры:
```python
cursor = spinning_cursor()
print(next(cursor))
print(next(cursor))
print(next(cursor))
print(next(cursor))
```

### `show_spinner`

#### Назначение:
Отображает вращающийся курсор в консоли в течение указанного времени.

#### Как работает функция:
Функция `show_spinner` использует генератор `spinning_cursor` для отображения вращающегося курсора в консоли. Она выводит каждый символ курсора, ждет заданное время (`delay`), затем стирает символ, чтобы заменить его следующим. Процесс повторяется в течение указанной продолжительности (`duration`).

```python
def show_spinner(duration: float = 5.0, delay: float = 0.1):
    """ Shows a spinning cursor in the console for a specified duration.
    
    Args:
        duration (float): How long the spinner should run (in seconds). Defaults to 5.0.
        delay (float): Delay between each spin (in seconds). Defaults to 0.1.
    
    Example:
        >>> show_spinner(duration=3.0, delay=0.2)  # Shows a spinner for 3 seconds
    """
    spinner = spinning_cursor()
    end_time = time.time() + duration

    while time.time() < end_time:
        sys.stdout.write(next(spinner))   # Print the next spinner character
        sys.stdout.flush()                # Force print to console immediately
        time.sleep(delay)                 # Pause for the delay duration
        sys.stdout.write('\b')            # Backspace to overwrite the character
```

#### Параметры:
- `duration` (float): Как долго должен отображаться курсор (в секундах). По умолчанию 5.0.
- `delay` (float): Задержка между каждой сменой символа курсора (в секундах). По умолчанию 0.1.

#### Примеры:
```python
show_spinner(duration=3.0, delay=0.2)  # Отображает курсор в течение 3 секунд
```

## Пример использования

В основной части модуля (`if __name__ == "__main__":`) демонстрируется пример использования функции `show_spinner`. Курсор отображается в течение 5 секунд с задержкой 0.1 секунды между сменами символов.

```python
if __name__ == "__main__":
    # Example usage of the spinner in a script
    print("Spinner for 5 seconds:")
    show_spinner(duration=5.0, delay=0.1)
    print("\nDone!")