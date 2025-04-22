# Модуль `html2text`

## Обзор

Модуль предназначен для преобразования HTML-контента в текстовый формат и сохранения результата. Он использует функции для чтения HTML-файлов, конвертации HTML в текст и сохранения текста в файл.

## Подробней

Этот модуль предназначен для обработки HTML-файлов, расположенных в Google Drive, извлечения текста из HTML-кода и сохранения этого текста в текстовый файл. Модуль использует другие утилиты, такие как `html2text` и `html2text_file` для конвертации, а также функции для чтения и записи файлов.

## Зависимости

-   `header`: Импортируется для каких-то целей (требуется дополнительная информация о модуле `header`).
-   `src.gs`: Используется для доступа к путям в Google Drive.
-   `src.utils.convertors.html2text`, `src.utils.convertors.html2text_file`: Функции для конвертации HTML в текст.
-   `src.utils.file.read_text_file`, `src.utils.file.save_text_file`: Функции для чтения и записи текстовых файлов.

## Параметры модуля

-   `html` (str): Содержимое HTML-файла, прочитанное функцией `read_text_file`.
-   `text_from_html` (str): Текст, полученный после конвертации HTML-кода функцией `html2text`.

## Функции

Модуль использует следующие функции из других модулей:

### `read_text_file`

```python
def read_text_file(
    file_path: str | Path,
    as_list: bool = False,
    extensions: Optional[List[str]] = None,
    chunk_size: int = 8192,
) -> Generator[str, None, None] | str | None:
    """
    Считывает содержимое файла (или файлов из каталога) с использованием генератора для экономии памяти.

    Args:
        file_path (str | Path): Путь к файлу или каталогу.
        as_list (bool): Если `True`, возвращает генератор строк.
        extensions (Optional[List[str]]): Список расширений файлов для чтения из каталога.
        chunk_size (int): Размер чанков для чтения файла в байтах.

    Returns:
        Generator[str, None, None] | str | None: Генератор строк, объединенная строка или `None` в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при чтении файла.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('example.txt')
        >>> content = read_text_file(file_path)
        >>> if content:
        ...    print(f'File content: {content[:100]}...')
        File content: Example text...
    """
```

**Назначение**: Читает содержимое текстового файла.

**Параметры**:

-   `file_path` (str | Path): Путь к файлу, который нужно прочитать.
-   `as_list` (bool, optional): Если `True`, возвращает содержимое файла в виде списка строк. По умолчанию `False`.
-   `extensions` (Optional[List[str]], optional): Список расширений файлов для чтения (используется при чтении директории). По умолчанию `None`.
-   `chunk_size` (int, optional): Размер чанка для чтения файла. По умолчанию `8192`.

**Возвращает**:

-   `Generator[str, None, None] | str | None`: Генератор строк, объединенная строка или `None` в случае ошибки.

**Вызывает исключения**:

-   `Exception`: Если возникает ошибка при чтении файла.

**Как работает функция**:
1.  Функция принимает путь к файлу `file_path` и считывает его содержимое.
2.  Если `as_list` установлен в `True`, функция возвращает генератор строк.
3.  Если произойдет ошибка во время чтения файла, функция перехватит исключение и залогирует его, а затем вернет `None`.

**Примеры**:

```python
from pathlib import Path
file_path = Path('example.txt')
content = read_text_file(file_path)
if content:
    print(f'File content: {content[:100]}...')
```

### `html2text`

```python
def html2text(html: str) -> str:
    """
    Конвертирует HTML-код в текст, удаляя HTML-теги и атрибуты.

    Args:
        html (str): HTML-код для конвертации.

    Returns:
        str: Текст без HTML-тегов.

    Raises:
        Отсутствуют явные исключения, но могут быть вызваны исключения из BeautifulSoup.

    Example:
        >>> html_code = '<p>Hello, <b>world!</b></p>'
        >>> text = html2text(html_code)
        >>> print(text)
        Hello, world!
    """
```

**Назначение**: Преобразует HTML-код в текст.

**Параметры**:

-   `html` (str): HTML-код для преобразования.

**Возвращает**:

-   `str`: Текст, извлеченный из HTML-кода.

**Как работает функция**:
1.  Функция принимает HTML-код в качестве входных данных.
2.  Использует библиотеку BeautifulSoup для парсинга HTML-кода.
3.  Извлекает весь текст из HTML-кода, удаляя все HTML-теги и атрибуты.

**Примеры**:

```python
html_code = '<p>Hello, <b>world!</b></p>'
text = html2text(html_code)
print(text)
```

### `save_text_file`

```python
def save_text_file(text: str, file_path: str | Path) -> None:
    """
    Сохраняет текст в файл.

    Args:
        text (str): Текст для сохранения.
        file_path (str | Path): Путь к файлу, в который нужно сохранить текст.

    Returns:
        None

    Raises:
        Exception: Если возникает ошибка при сохранении файла.

    Example:
        >>> file_path = 'example.txt'
        >>> text = 'Hello, world!'
        >>> save_text_file(text, file_path)
    """
```

**Назначение**: Сохраняет текст в файл.

**Параметры**:

-   `text` (str): Текст, который нужно сохранить в файл.
-   `file_path` (str | Path): Путь к файлу, в который нужно сохранить текст.

**Возвращает**:

-   `None`: Функция ничего не возвращает.

**Вызывает исключения**:

-   `Exception`: Если возникает ошибка при сохранении файла.

**Как работает функция**:
1.  Функция принимает текст и путь к файлу.
2.  Открывает файл по указанному пути в режиме записи (`'w'`).
3.  Записывает переданный текст в файл.
4.  Если во время записи возникает ошибка, функция перехватывает исключение, логирует его и завершает работу.

**Примеры**:

```python
file_path = 'example.txt'
text = 'Hello, world!'
save_text_file(text, file_path)
```

## Принцип работы

1.  Читается HTML-файл `index.html` из Google Drive с использованием функции `read_text_file`.
2.  HTML-код конвертируется в текст с помощью функции `html2text`.
3.  Полученный текст сохраняется в файл `index.txt` в Google Drive с использованием функции `save_text_file`.

## Использование

Для использования этого модуля необходимо:

1.  Установить необходимые зависимости, такие как `beautifulsoup4`.
2.  Указать правильные пути к файлам в Google Drive.
3.  Вызвать функции `read_text_file`, `html2text` и `save_text_file` для выполнения преобразования и сохранения.

Пример использования:

```python
from src import gs
from src.utils.convertors import html2text
from src.utils.file import read_text_file, save_text_file

html = read_text_file(gs.path.google_drive / 'html2text' / 'index.html')
text_from_html = html2text(html)
save_text_file(text_from_html, gs.path.google_drive / 'html2text' / 'index.txt')
```