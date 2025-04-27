# Модуль src.utils.convertors.html

## Обзор

Модуль `src.utils.convertors.html` предоставляет набор утилит для преобразования HTML-кода. 

## Детали

Модуль содержит функции для:

- Преобразования HTML в escape-последовательности (html2escape).
- Преобразования escape-последовательностей в HTML (escape2html).
- Преобразования HTML в словарь, где ключами являются теги, а значениями - содержимое (html2dict).
- Преобразования HTML в объект SimpleNamespace, где атрибутами являются теги, а значениями - содержимое (html2ns).
- Преобразования HTML в PDF-файл с использованием WeasyPrint (html2pdf).
- Преобразования HTML-файла в документ Word (DOCX) с использованием LibreOffice (html_to_docx).

## Функции

### `html2escape`

**Описание**: Функция преобразует HTML в escape-последовательности.

**Параметры**:

- `input_str` (str): HTML-код.

**Возвращаемое значение**:

- `str`: HTML-код, преобразованный в escape-последовательности.

**Пример**:

```python
>>> html = "<p>Hello, world!</p>"
>>> result = html2escape(html)
>>> print(result)
&lt;p&gt;Hello, world!&lt;/p&gt;
```

### `escape2html`

**Описание**: Функция преобразует escape-последовательности в HTML.

**Параметры**:

- `input_str` (str): Строка с escape-последовательностями.

**Возвращаемое значение**:

- `str`: Escape-последовательности, преобразованные обратно в HTML.

**Пример**:

```python
>>> escaped = "&lt;p&gt;Hello, world!&lt;/p&gt;"
>>> result = escape2html(escaped)
>>> print(result)
<p>Hello, world!</p>
```

### `html2dict`

**Описание**: Функция преобразует HTML в словарь, где ключами являются теги, а значениями - содержимое.

**Параметры**:

- `html_str` (str): HTML-строка для преобразования.

**Возвращаемое значение**:

- `dict`: Словарь с HTML-тегами в качестве ключей и их содержимым в качестве значений.

**Пример**:

```python
>>> html = "<p>Hello</p><a href='link'>World</a>"
>>> result = html2dict(html)
>>> print(result)
{'p': 'Hello', 'a': 'World'}
```

### `html2ns`

**Описание**: Функция преобразует HTML в объект SimpleNamespace, где атрибутами являются теги, а значениями - содержимое.

**Параметры**:

- `html_str` (str): HTML-строка для преобразования.

**Возвращаемое значение**:

- `SimpleNamespace`: Объект SimpleNamespace с HTML-тегами в качестве атрибутов и их содержимым в качестве значений.

**Пример**:

```python
>>> html = "<p>Hello</p><a href='link'>World</a>"
>>> result = html2ns(html)
>>> print(result.p)
Hello
>>> print(result.a)
World
```

### `html2pdf`

**Описание**: Функция преобразует HTML-содержимое в PDF-файл с использованием WeasyPrint.

**Параметры**:

- `html_str` (str): HTML-содержимое в виде строки.
- `pdf_file` (str | Path): Путь к выходному PDF-файлу.

**Возвращаемое значение**:

- `bool | None`: Возвращает `True`, если генерация PDF прошла успешно; `None` в противном случае.

**Пример**:

```python
>>> html = "<html><body><h1>Hello, world!</h1></body></html>"
>>> pdf_file = "output.pdf"
>>> result = html2pdf(html, pdf_file)
>>> if result:
>>>     print(f"PDF file {pdf_file} successfully generated.")
```

### `html_to_docx`

**Описание**: Функция преобразует HTML-файл в документ Word (DOCX) с использованием LibreOffice.

**Параметры**:

- `html_file` (str): Путь к входному HTML-файлу в виде строки.
- `output_docx` (Path | str): Путь к выходному DOCX-файлу.

**Возвращаемое значение**:

- `bool`: `True`, если преобразование прошло успешно; `False` в противном случае.

**Пример**:

```python
>>> html_file = "input.html"
>>> output_docx = "output.docx"
>>> result = html_to_docx(html_file, output_docx)
>>> if result:
>>>     print(f"HTML file {html_file} successfully converted to DOCX file {output_docx}.")
```

## Принцип работы

**Функции:**

- `html2escape`: Функция использует функцию `escape_html_tags` из модуля `src.utils.string.formatter` для преобразования HTML в escape-последовательности.
- `escape2html`: Функция использует функцию `unescape_html_tags` из модуля `src.utils.string.formatter` для преобразования escape-последовательностей в HTML.
- `html2dict`: Функция создает парсер HTML `HTMLToDictParser`, наследуемый от `HTMLParser`, который обрабатывает теги и содержимое HTML-кода.
- `html2ns`: Функция преобразует HTML-код в словарь с помощью `html2dict` и затем использует его для создания объекта `SimpleNamespace`.
- `html2pdf`: Функция использует библиотеку WeasyPrint для генерации PDF-файла из HTML-строки.
- `html_to_docx`: Функция использует библиотеку LibreOffice для преобразования HTML-файла в DOCX-файл. Она использует команду `soffice` LibreOffice для запуска headless-преобразования.

## Примеры

```python
# html2escape
>>> html = "<p>Hello, world!</p>"
>>> result = html2escape(html)
>>> print(result)
&lt;p&gt;Hello, world!&lt;/p&gt;

# escape2html
>>> escaped = "&lt;p&gt;Hello, world!&lt;/p&gt;"
>>> result = escape2html(escaped)
>>> print(result)
<p>Hello, world!</p>

# html2dict
>>> html = "<p>Hello</p><a href='link'>World</a>"
>>> result = html2dict(html)
>>> print(result)
{'p': 'Hello', 'a': 'World'}

# html2ns
>>> html = "<p>Hello</p><a href='link'>World</a>"
>>> result = html2ns(html)
>>> print(result.p)
Hello
>>> print(result.a)
World

# html2pdf
>>> html = "<html><body><h1>Hello, world!</h1></body></html>"
>>> pdf_file = "output.pdf"
>>> result = html2pdf(html, pdf_file)
>>> if result:
>>>     print(f"PDF file {pdf_file} successfully generated.")

# html_to_docx
>>> html_file = "input.html"
>>> output_docx = "output.docx"
>>> result = html_to_docx(html_file, output_docx)
>>> if result:
>>>     print(f"HTML file {html_file} successfully converted to DOCX file {output_docx}.")
```