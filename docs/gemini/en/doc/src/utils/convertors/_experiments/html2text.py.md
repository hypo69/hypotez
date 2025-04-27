# Модуль src.utils.convertors._experiments

## Обзор

Модуль `src.utils.convertors._experiments` содержит экспериментальные функции для преобразования HTML-кода в текст. Этот модуль пока находится в разработке и может содержать нестабильные или экспериментальные функции. 

## Детали

Модуль импортирует необходимые библиотеки и функции из других модулей проекта `hypotez`.  

- `header`: импортирует заголовок модуля.
- `src`: импортирует модуль `gs`, который предоставляет доступ к настройкам Google Drive.
- `src.utils.convertors`: импортирует функции `html2text` и `html2text_file` для преобразования HTML-кода в текст.
- `src.utils.file`: импортирует функции `read_text_file` и `save_text_file` для работы с файлами.

Модуль выполняет следующие действия:

1. **Считывает HTML-код из файла**:
    - Использует функцию `read_text_file` для чтения HTML-кода из файла `index.html`, расположенного в папке `html2text` на Google Drive.
2. **Преобразует HTML-код в текст**:
    - Использует функцию `html2text` для преобразования полученного HTML-кода в текст.
3. **Сохраняет текст в файл**:
    - Использует функцию `save_text_file` для сохранения полученного текста в файл `index.txt`, расположенный в папке `html2text` на Google Drive.

## Функции

### `html2text`

**Цель**:  Преобразует HTML-код в текст, удаляя HTML-теги.

**Параметры**:

- `html` (str): HTML-код, который нужно преобразовать в текст.

**Возвращает**:

- `str`: Текстовое представление HTML-кода.

**Пример**:

```python
from src.utils.convertors._experiments.html2text import html2text

html = "<h1>Заголовок</h1><p>Текст страницы</p>"
text = html2text(html)
print(text)
```
**Вывод**:

```
Заголовок
Текст страницы
```

### `html2text_file`

**Цель**: Преобразует HTML-код из файла в текст и сохраняет результат в файл.

**Параметры**:

- `input_file` (str | Path): Путь к файлу, содержащему HTML-код.
- `output_file` (str | Path): Путь к файлу, в который нужно сохранить полученный текст.

**Возвращает**:

- `None`: Функция не возвращает значение.

**Пример**:

```python
from src.utils.convertors._experiments.html2text import html2text_file

html2text_file("input.html", "output.txt")
```

**Пример работы**:

Функция `html2text_file` считывает HTML-код из файла `input.html`, затем использует функцию `html2text` для преобразования кода в текст и сохраняет полученный текст в файл `output.txt`. 

## Примеры

```python
from src.utils.convertors._experiments.html2text import html2text, html2text_file

# Пример 1: преобразование HTML-кода в текст
html = "<h1>Заголовок</h1><p>Текст страницы</p>"
text = html2text(html)
print(text)

# Пример 2: преобразование HTML-кода из файла в текст
html2text_file("input.html", "output.txt") 
```