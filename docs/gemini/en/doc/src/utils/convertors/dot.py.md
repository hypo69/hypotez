# Модуль для преобразования файлов DOT в PNG

## Обзор

Модуль `src.utils.convertors.dot` содержит функцию `dot2png`, которая преобразует файлы DOT в изображения PNG с использованием библиотеки Graphviz. 

## Подробности

Файлы DOT представляют собой текстовые файлы, описывающие графики в формате Graphviz. Функция `dot2png` читает DOT-файл, создает объект `Source` с помощью библиотеки Graphviz и затем преобразует его в изображение PNG.

## Функции

### `dot2png`

```python
def dot2png(dot_file: str, png_file: str) -> None:
    """ Преобразует файл DOT в изображение PNG.

    Args:
        dot_file (str): Путь к входному DOT-файлу.
        png_file (str): Путь, где будет сохранен выходной PNG-файл.

    Raises:
        FileNotFoundError: Если DOT-файл не существует.
        Exception: При возникновении других ошибок во время преобразования.

    Example:
        >>> dot2png('example.dot', 'output.png')
        
        Это преобразует DOT-файл 'example.dot' в изображение PNG с именем 'output.png'.
        
        Пример содержимого DOT-файла 'example.dot':
        
        ```dot
        digraph G {
            A -> B;
            B -> C;
            C -> A;
        }
        ```
        
        Чтобы запустить скрипт из командной строки:
        
        ```bash
        python dot2png.py example.dot output.png
        ```
        
        Эта команда создаст PNG-файл с именем 'output.png' из графика, определенного в 'example.dot'.
    """
    ...
```

**Описание**: Функция `dot2png` считывает DOT-файл, создает объект `Source` и преобразует его в изображение PNG.

**Параметры**:

- `dot_file` (str): Путь к входному DOT-файлу.
- `png_file` (str): Путь к выходному PNG-файлу.

**Возвращаемое значение**: 
- `None`

**Исключения**:

- `FileNotFoundError`: Возникает, если DOT-файл не найден.
- `Exception`: Возникает при возникновении других ошибок во время преобразования.


**Как работает функция**:

1. Функция открывает входной DOT-файл и считывает его содержимое.
2. Создается объект `Source` библиотеки Graphviz, используя прочитанное содержимое DOT-файла.
3. Устанавливается формат выходного файла как `png`.
4. Выполняется рендеринг объекта `Source` в PNG-файл с использованием функции `render`.

**Примеры**:

```python
# Преобразование DOT-файла 'example.dot' в PNG-файл 'output.png'
dot2png('example.dot', 'output.png')
```

## Примеры использования

```python
# Создание объекта Driver с помощью Chrome
driver = Driver(Chrome)

# Пример использования функции `dot2png`
dot2png('my_graph.dot', 'my_graph.png')
```

## Дополнительные сведения

- Документация библиотеки Graphviz: [https://graphviz.org/](https://graphviz.org/)
- Документация библиотеки Python `graphviz`: [https://graphviz.readthedocs.io/en/stable/](https://graphviz.readthedocs.io/en/stable/)