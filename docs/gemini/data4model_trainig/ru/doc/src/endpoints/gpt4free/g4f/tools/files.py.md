# Модуль для работы с файлами
=================================

Модуль предоставляет инструменты для обработки различных типов файлов, включая чтение, скачивание и преобразование контента. Он включает в себя функции для безопасной обработки имен файлов, определения поддерживаемых типов файлов, извлечения текста из различных форматов (PDF, DOCX, ODT, EPUB, XLSX, HTML, ZIP и другие текстовые форматы), а также для скачивания файлов из интернета.

## Обзор

Модуль `files.py` предназначен для работы с файлами различных форматов, обеспечивая их чтение, обработку и скачивание. Он включает в себя функции для безопасного управления именами файлов, проверки поддерживаемых форматов, извлечения текста и скачивания файлов из интернета. Модуль также предоставляет возможности для кэширования и очистки данных, а также для интеграции с другими инструментами, такими как `spacy` для улучшения обработки текста.

## Подробнее

Этот модуль является важной частью проекта `hypotez`, так как обеспечивает функциональность для работы с файлами, необходимую для различных задач, таких как анализ текста, обработка данных и взаимодействие с веб-контентом. Он используется для чтения и обработки файлов, загруженных пользователями, а также для скачивания и обработки данных из интернета.

## Классы

В данном модуле классы отсутствуют.

## Функции

### `secure_filename`

```python
def secure_filename(filename: str) -> str:
    """
    Очищает имя файла, удаляя небезопасные символы.

    Args:
        filename (str): Имя файла для очистки.

    Returns:
        str: Очищенное имя файла.

    Как работает функция:
    - Функция принимает имя файла в качестве входного параметра.
    - Удаляет все символы, кроме букв, цифр, основных знаков препинания, подчеркивания, плюса и минуса.
    - Удаляет пробелы в начале и конце имени файла.
    - Обрезает имя файла до 100 символов.
    - Удаляет точки, запятые, подчеркивания, плюсы и минусы в начале и конце имени файла.
    """
```

**Примеры**:

```python
secure_filename("example.txt")  # возвращает "example.txt"
secure_filename("file name.txt")  # возвращает "file_name.txt"
secure_filename("  file.txt  ")  # возвращает "file.txt"
secure_filename("file%name$.txt")  # возвращает "file_name_.txt"
```

### `supports_filename`

```python
def supports_filename(filename: str) -> bool:
    """
    Проверяет, поддерживается ли указанный тип файла для обработки.

    Args:
        filename (str): Имя файла для проверки.

    Returns:
        bool: `True`, если файл поддерживается, иначе `False`.

    Raises:
        MissingRequirementsError: Если отсутствуют необходимые библиотеки для обработки данного типа файла.

    Как работает функция:
    - Функция принимает имя файла в качестве входного параметра.
    - Проверяет расширение файла и наличие необходимых библиотек для обработки данного типа файла.
    - Для PDF файлов проверяет наличие `pypdf2`, `pdfplumber` или `pdfminer`.
    - Для DOCX файлов проверяет наличие `docx` или `docx2txt`.
    - Для ODT файлов проверяет наличие `odfpy`.
    - Для EPUB файлов проверяет наличие `ebooklib`.
    - Для XLSX файлов проверяет наличие `openpyxl`.
    - Для HTML файлов проверяет наличие `beautifulsoup4`.
    - Для ZIP файлов всегда возвращает `True`.
    - Для текстовых файлов проверяет, что расширение файла находится в списке `PLAIN_FILE_EXTENSIONS`.
    - Возвращает `True`, если файл поддерживается, иначе `False`.
    """
```

**Примеры**:

```python
supports_filename("example.pdf")  # возвращает True, если установлен pypdf2, pdfplumber или pdfminer
supports_filename("example.docx")  # возвращает True, если установлен docx или docx2txt
supports_filename("example.txt")  # возвращает True
supports_filename("example.odt") # возвращает True, если установлен odfpy
```

### `get_bucket_dir`

```python
def get_bucket_dir(*parts) -> str:
    """
    Возвращает путь к директории бакета, объединяя части пути и очищая имена файлов.

    Args:
        *parts: Переменное количество частей пути к бакету.

    Returns:
        str: Путь к директории бакета.

    Как работает функция:
    - Функция принимает переменное количество частей пути к бакету.
    - Объединяет части пути с помощью функции `os.path.join`.
    - Очищает имена файлов в каждой части пути с помощью функции `secure_filename`.
    - Возвращает путь к директории бакета.
    """
```

**Примеры**:

```python
get_bucket_dir("bucket1", "file.txt")  # возвращает путь к директории "bucket1/file.txt"
get_bucket_dir("bucket2", "file name.txt")  # возвращает путь к директории "bucket2/file_name.txt"
```

### `get_buckets`

```python
def get_buckets() -> Optional[List[str]]:
    """
    Возвращает список директорий бакетов.

    Returns:
        Optional[List[str]]: Список директорий бакетов или `None`, если директория бакетов не существует.

    Как работает функция:
    - Функция пытается получить список директорий в директории бакетов.
    - Если директория бакетов не существует, возвращает `None`.
    - Возвращает список директорий бакетов.
    """
```

**Примеры**:

```python
get_buckets()  # возвращает список директорий бакетов, например, ["bucket1", "bucket2"]
```

### `spacy_refine_chunks`

```python
def spacy_refine_chunks(source_iterator: Iterator[str]) -> Iterator[str]:
    """
    Улучшает фрагменты текста, используя `spacy` для выделения значимых предложений.

    Args:
        source_iterator (Iterator[str]): Итератор фрагментов текста.

    Returns:
        Iterator[str]: Итератор улучшенных фрагментов текста.

    Raises:
        MissingRequirementsError: Если библиотека `spacy` не установлена.

    Как работает функция:
    - Функция принимает итератор фрагментов текста.
    - Загружает модель `spacy` для английского языка.
    - Для каждого фрагмента текста выделяет предложения с наибольшей длиной.
    - Возвращает итератор улучшенных фрагментов текста.
    """
```

**Примеры**:

```python
# Пример использования spacy_refine_chunks с итератором строк
text_chunks = ["This is a sentence. This is another sentence.", "And yet another one."]
refined_chunks = spacy_refine_chunks(iter(text_chunks))
for chunk in refined_chunks:
    print(chunk)
```

### `get_filenames`

```python
def get_filenames(bucket_dir: Path) -> list[str]:
    """
    Возвращает список имен файлов, хранящихся в файле `FILE_LIST` в указанной директории бакета.

    Args:
        bucket_dir (Path): Путь к директории бакета.

    Returns:
        list[str]: Список имен файлов.

    Как работает функция:
    - Функция принимает путь к директории бакета в качестве входного параметра.
    - Пытается открыть файл `FILE_LIST` в директории бакета.
    - Читает имена файлов из файла `FILE_LIST` и возвращает их в виде списка.
    - Если файл `FILE_LIST` не существует, возвращает пустой список.
    """
```

**Примеры**:

```python
# Пример использования get_filenames с указанием директории бакета
bucket_dir = Path("/path/to/bucket")
filenames = get_filenames(bucket_dir)
print(filenames)
```

### `stream_read_files`

```python
def stream_read_files(bucket_dir: Path, filenames: list, delete_files: bool = False) -> Iterator[str]:
    """
    Читает содержимое файлов из указанной директории бакета и возвращает итератор строк.

    Args:
        bucket_dir (Path): Путь к директории бакета.
        filenames (list): Список имен файлов для чтения.
        delete_files (bool): Если `True`, файлы будут удалены после прочтения. По умолчанию `False`.

    Returns:
        Iterator[str]: Итератор строк с содержимым файлов.

    Как работает функция:
    - Функция принимает путь к директории бакета, список имен файлов и флаг для удаления файлов после прочтения.
    - Для каждого файла в списке:
        - Проверяет существование файла и его размер.
        - Если файл является ZIP архивом, распаковывает его и рекурсивно вызывает `stream_read_files` для распакованных файлов.
        - Если файл является PDF, DOCX, ODT, EPUB, XLSX или HTML, извлекает текст с использованием соответствующих библиотек.
        - Если файл имеет одно из расширений, перечисленных в `PLAIN_FILE_EXTENSIONS`, читает его содержимое как текст.
        - Возвращает итератор строк с содержимым файлов.
    """
```

**Примеры**:

```python
# Пример использования stream_read_files с указанием директории бакета и списка файлов
bucket_dir = Path("/path/to/bucket")
filenames = ["file1.txt", "file2.pdf"]
for chunk in stream_read_files(bucket_dir, filenames):
    print(chunk)
```

### `cache_stream`

```python
def cache_stream(stream: Iterator[str], bucket_dir: Path) -> Iterator[str]:
    """
    Кэширует поток данных в файл и возвращает итератор строк.

    Args:
        stream (Iterator[str]): Итератор строк для кэширования.
        bucket_dir (Path): Путь к директории бакета.

    Returns:
        Iterator[str]: Итератор строк с содержимым кэша.

    Как работает функция:
    - Функция принимает итератор строк и путь к директории бакета.
    - Проверяет, существует ли файл кэша. Если существует, возвращает итератор строк из файла кэша.
    - Если файл кэша не существует, создает временный файл и записывает в него содержимое итератора строк.
    - Переименовывает временный файл в файл кэша.
    - Возвращает итератор строк с содержимым кэша.
    """
```

**Примеры**:

```python
# Пример использования cache_stream с итератором строк и указанием директории бакета
data_stream = iter(["chunk1", "chunk2", "chunk3"])
bucket_dir = Path("/path/to/bucket")
for chunk in cache_stream(data_stream, bucket_dir):
    print(chunk)
```

### `is_complete`

```python
def is_complete(data: str) -> bool:
    """
    Проверяет, является ли переданная строка завершенным блоком данных.

    Args:
        data (str): Строка для проверки.

    Returns:
        bool: `True`, если строка является завершенным блоком данных, иначе `False`.

    Как работает функция:
    - Функция принимает строку в качестве входного параметра.
    - Проверяет, заканчивается ли строка на "\\n```\\n\\n" и содержит ли четное количество "```".
    - Возвращает `True`, если строка является завершенным блоком данных, иначе `False`.
    """
```

**Примеры**:

```python
is_complete("example\\n```\\n\\n")  # возвращает True
is_complete("example\\n```\\n\\n```\\n```")  # возвращает True
is_complete("example")  # возвращает False
```

### `read_path_chunked`

```python
def read_path_chunked(path: Path) -> Iterator[str]:
    """
    Читает файл по частям и возвращает итератор строк.

    Args:
        path (Path): Путь к файлу для чтения.

    Returns:
        Iterator[str]: Итератор строк с содержимым файла.

    Как работает функция:
    - Функция принимает путь к файлу в качестве входного параметра.
    - Открывает файл для чтения в кодировке UTF-8.
    - Читает файл по частям, размером до 4096 байт.
    - Если размер части превышает 4096 байт, проверяет, является ли часть завершенным блоком данных.
    - Если часть является завершенным блоком данных или ее размер превышает 8192 байта, возвращает часть.
    - Возвращает итератор строк с содержимым файла.
    """
```

**Примеры**:

```python
# Пример использования read_path_chunked с указанием пути к файлу
file_path = Path("/path/to/file.txt")
for chunk in read_path_chunked(file_path):
    print(chunk)
```

### `read_bucket`

```python
def read_bucket(bucket_dir: Path) -> Iterator[str]:
    """
    Читает содержимое бакета из кэшированных файлов и возвращает итератор строк.

    Args:
        bucket_dir (Path): Путь к директории бакета.

    Returns:
        Iterator[str]: Итератор строк с содержимым бакета.

    Как работает функция:
    - Функция принимает путь к директории бакета.
    - Проверяет наличие файлов кэша в директории бакета.
    - Если файлы кэша существуют, возвращает итератор строк с содержимым файлов кэша.
    - Если файлы кэша не существуют, возвращает пустой итератор.
    """
```

**Примеры**:

```python
# Пример использования read_bucket с указанием директории бакета
bucket_dir = Path("/path/to/bucket")
for chunk in read_bucket(bucket_dir):
    print(chunk)
```

### `stream_read_parts_and_refine`

```python
def stream_read_parts_and_refine(bucket_dir: Path, delete_files: bool = False) -> Iterator[str]:
    """
    Читает части файла из указанной директории, улучшает их с помощью `spacy` и возвращает итератор строк.

    Args:
        bucket_dir (Path): Путь к директории бакета.
        delete_files (bool): Если `True`, файлы будут удалены после прочтения. По умолчанию `False`.

    Returns:
        Iterator[str]: Итератор строк с улучшенным содержимым файлов.

    Как работает функция:
    - Функция принимает путь к директории бакета и флаг для удаления файлов после прочтения.
    - Проверяет наличие файлов кэша в директории бакета.
    - Если файлы кэша существуют, разделяет файл кэша на части с помощью функции `split_file_by_size_and_newline`.
    - Для каждой части файла:
        - Улучшает содержимое части с помощью функции `spacy_refine_chunks`.
        - Записывает улучшенное содержимое во временный файл.
        - Переименовывает временный файл в файл кэша.
        - Возвращает итератор строк с улучшенным содержимым файлов.
    """
```

**Примеры**:

```python
# Пример использования stream_read_parts_and_refine с указанием директории бакета
bucket_dir = Path("/path/to/bucket")
for chunk in stream_read_parts_and_refine(bucket_dir):
    print(chunk)
```

### `split_file_by_size_and_newline`

```python
def split_file_by_size_and_newline(input_filename: str, output_dir: str, chunk_size_bytes: int = 1024*1024) -> None:
    """
    Разделяет файл на части заданного размера, разделяя только по символам новой строки.

    Args:
        input_filename (str): Путь к входному файлу.
        output_dir (str): Префикс для выходных файлов (например, 'output_part_').
        chunk_size_bytes (int): Желаемый размер каждой части в байтах.
    """
```

**Как работает функция**:

Функция `split_file_by_size_and_newline` разделяет большой файл на несколько меньших файлов, каждый из которых имеет размер, близкий к `chunk_size_bytes`. Разделение происходит только по символам новой строки, чтобы избежать разрыва строк посередине.

- Открывает входной файл для чтения в кодировке UTF-8.
- Инициализирует переменные для хранения текущей части файла, ее размера и номера части.
- Читает файл построчно.
- Добавляет каждую строку к текущей части файла и увеличивает размер текущей части файла на длину строки в байтах.
- Если размер текущей части файла превышает `chunk_size_bytes`, записывает текущую часть файла в выходной файл и создает новую часть файла.
- Записывает последнюю часть файла в выходной файл.

**Примеры**:
```python
split_file_by_size_and_newline('input.txt', 'output_dir', chunk_size_bytes=500000)
```

### `get_filename`

```python
async def get_filename(response: ClientResponse) -> Optional[str]:
    """
    Пытается извлечь имя файла из ответа aiohttp.

    Args:
        response: Объект ClientResponse aiohttp.

    Returns:
        Имя файла в виде строки или None, если не удалось определить.

    Как работает функция:
    - Функция пытается извлечь имя файла из заголовка Content-Disposition.
    - Если заголовок Content-Disposition отсутствует или не содержит имени файла, пытается извлечь имя файла из URL.
    - Возвращает имя файла или None, если не удалось определить имя файла.
    """
```

**Примеры**:
```python
# Пример использования async get_filename с объектом ClientResponse
async def example():
    async with ClientSession() as session:
        async with session.get('https://example.com/file.pdf') as response:
            filename = await get_filename(response)
            print(filename)
```

### `get_file_extension`

```python
async def get_file_extension(response: ClientResponse) -> Optional[str]:
    """
    Пытается определить расширение файла из ответа aiohttp.

    Args:
        response: Объект ClientResponse aiohttp.

    Returns:
        Расширение файла (например, ".html", ".json", ".pdf", ".zip", ".md", ".txt") в виде строки,
        или None, если не удалось определить.

    Как работает функция:
    - Функция пытается определить расширение файла из заголовка Content-Type.
    - Если заголовок Content-Type отсутствует или не содержит расширения файла, пытается определить расширение файла из URL.
    - Возвращает расширение файла или None, если не удалось определить расширение файла.
    """
```

**Примеры**:
```python
# Пример использования async get_file_extension с объектом ClientResponse
async def example():
    async with ClientSession() as session:
        async with session.get('https://example.com/file.pdf') as response:
            extension = await get_file_extension(response)
            print(extension)
```

### `read_links`

```python
def read_links(html: str, base: str) -> set[str]:
    """
    Извлекает ссылки из HTML-кода.

    Args:
        html (str): HTML-код для анализа.
        base (str): Базовый URL для объединения относительных ссылок.

    Returns:
        set[str]: Множество URL-адресов, найденных в HTML-коде.

    Как работает функция:
    - Функция принимает HTML-код и базовый URL в качестве входных параметров.
    - Использует BeautifulSoup для анализа HTML-кода.
    - Извлекает все ссылки из HTML-кода.
    - Объединяет относительные ссылки с базовым URL.
    - Возвращает множество URL-адресов.
    """
```

**Примеры**:
```python
# Пример использования read_links с HTML-кодом и базовым URL
html = '<a href="https://example.com">Example</a> <a href="/page">Page</a>'
base = 'https://base.com'
links = read_links(html, base)
print(links)
```

### `download_urls`

```python
async def download_urls(
    bucket_dir: Path,
    urls: list[str],
    max_depth: int = 0,
    loading_urls: set[str] = set(),
    lock: asyncio.Lock = None,
    delay: int = 3,
    new_urls: list[str] = list(),
    group_size: int = 5,
    timeout: int = 10,
    proxy: Optional[str] = None
) -> AsyncIterator[str]:
    """
    Асинхронно скачивает файлы по заданным URL-адресам.

    Args:
        bucket_dir (Path): Директория, в которую сохраняются скачанные файлы.
        urls (list[str]): Список URL-адресов для скачивания.
        max_depth (int): Максимальная глубина рекурсивного скачивания HTML-страниц. По умолчанию 0.
        loading_urls (set[str]): Множество URL-адресов, которые в данный момент скачиваются.
        lock (asyncio.Lock): Блокировка для защиты общих ресурсов.
        delay (int): Задержка в секундах между запросами. По умолчанию 3.
        new_urls (list[str]): Список новых URL-адресов, найденных на скачанных HTML-страницах.
        group_size (int): Количество URL-адресов, скачиваемых одновременно. По умолчанию 5.
        timeout (int): Максимальное время ожидания ответа от сервера в секундах. По умолчанию 10.
        proxy (Optional[str]): Прокси-сервер для использования при скачивании. По умолчанию None.

    Returns:
        AsyncIterator[str]: Асинхронный итератор имен скачанных файлов.

    Как работает функция:
    - Функция асинхронно скачивает файлы по заданным URL-адресам.
    - Если URL-адрес ведет на HTML-страницу, функция рекурсивно скачивает все ссылки, найденные на этой странице, до заданной глубины.
    - Скачанные файлы сохраняются в указанной директории.
    - Функция возвращает асинхронный итератор имен скачанных файлов.

    Внутренние функции:

    - download_url(url: str, max_depth: int) -> str:
        - Асинхронно скачивает файл по заданному URL-адресу.
        - Извлекает имя файла из ответа сервера.
        - Сохраняет файл в указанной директории.
        - Если URL-адрес ведет на HTML-страницу и глубина рекурсии больше 0, извлекает все ссылки из этой страницы и добавляет их в список новых URL-адресов для скачивания.
        - Возвращает имя скачанного файла.
    """
```

**Примеры**:
```python
# Пример использования async download_urls с указанием директории для скачивания и списка URL-адресов
async def example():
    bucket_dir = Path('/path/to/bucket')
    urls = ['https://example.com/file1.pdf', 'https://example.com/file2.txt']
    async for filename in download_urls(bucket_dir, urls):
        print(filename)
```

### `get_downloads_urls`

```python
def get_downloads_urls(bucket_dir: Path, delete_files: bool = False) -> Iterator[str]:
    """
    Извлекает URL-адреса для скачивания из файла `DOWNLOADS_FILE` в указанной директории бакета.

    Args:
        bucket_dir (Path): Путь к директории бакета.
        delete_files (bool): Если `True`, файл `DOWNLOADS_FILE` будет удален после прочтения. По умолчанию `False`.

    Returns:
        Iterator[str]: Итератор URL-адресов для скачивания.

    Как работает функция:
    - Функция принимает путь к директории бакета и флаг для удаления файла `DOWNLOADS_FILE` после прочтения.
    - Пытается открыть файл `DOWNLOADS_FILE` в директории бакета.
    - Читает данные из файла `DOWNLOADS_FILE` и возвращает их в виде итератора URL-адресов для скачивания.
    - Если файл `DOWNLOADS_FILE` не существует, возвращает пустой итератор.
    """
```

**Примеры**:

```python
# Пример использования get_downloads_urls с указанием директории бакета
bucket_dir = Path("/path/to/bucket")
for url in get_downloads_urls(bucket_dir):
    print(url)
```

### `read_and_download_urls`

```python
def read_and_download_urls(bucket_dir: Path, delete_files: bool = False, event_stream: bool = False) -> Iterator[str]:
    """
    Читает URL-адреса из файла загрузок и скачивает их, записывая имена файлов в файл `FILE_LIST`.

    Args:
        bucket_dir (Path): Путь к директории бакета.
        delete_files (bool): Определяет, следует ли удалять файл загрузок после чтения.
        event_stream (bool): Определяет, следует ли генерировать события потока для каждого скачанного файла.

    Returns:
        Iterator[str]: Итератор строк, содержащих данные о событиях, если `event_stream` равно `True`.

    Как работает функция:
    - Функция сначала получает URL-адреса из файла загрузок с помощью `get_downloads_urls`.
    - Затем она открывает файл `FILE_LIST` в режиме добавления.
    - Для каждого URL-адреса она скачивает файл с помощью `download_urls` и записывает имя файла в `FILE_LIST`.
    - Если `event_stream` равно `True`, она также генерирует события потока для каждого скачанного файла.
    """
```

**Примеры**:
```python
# Пример использования read_and_download_urls с указанием директории бакета
bucket_dir = Path("/path/to/bucket")
for event in read_and_download_urls(bucket_dir):
    print(event)
```

### `async_read_and_download_urls`

```python
async def async_read_and_download_urls(bucket_dir: Path, delete_files: bool = False, event_stream: bool = False) -> AsyncIterator[str]:
    """
    Асинхронно читает URL-адреса из файла загрузок и скачивает их, записывая имена файлов в файл `FILE_LIST`.

    Args:
        bucket_dir (Path): Путь к директории бакета.
        delete_files (bool): Определяет, следует ли удалять файл загрузок после чтения.
        event_stream (bool): Определяет, следует ли генерировать события потока для каждого скачанного файла.

    Returns:
        AsyncIterator[str]: Асинхронный итератор строк, содержащих данные о событиях, если `event_stream` равно `True`.

    Как работает функция:
    - Функция сначала получает URL-адреса из файла загрузок с помощью `get_downloads_urls`.
    - Затем она открывает файл `FILE_LIST` в режиме добавления.
    - Для каждого URL-адреса она асинхронно скачивает файл с помощью `download_urls` и записывает имя файла в `FILE_LIST`.
    - Если `event_stream` равно `True`, она также генерирует события потока для каждого скачанного файла.
    """
```

**Примеры**:
```python
# Пример использования async async_read_and_download_urls с указанием директории бакета
async def example():
    bucket_dir = Path("/path/to/bucket")
    async for event in async_read_and_download_urls(bucket_dir):
        print(event)
```

### `stream_chunks`

```python
def stream_chunks(bucket_dir: Path, delete_files: bool = False, refine_chunks_with_spacy: bool = False, event_stream: bool = False) -> Iterator[str]:
    """
    Обрабатывает файлы в указанной директории бакета, возвращая фрагменты текста.

    Args:
        bucket_dir (Path): Путь к директории бакета.
        delete_files (bool): Если `True`, файлы будут удалены после обработки. По умолчанию `False`.
        refine_chunks_with_spacy (bool): Если `True`, фрагменты текста будут обработаны с помощью `spacy`. По умолчанию `False`.
        event_stream (bool): Если `True`, будут генерироваться события для каждого обработанного фрагмента. По умолчанию `False`.

    Returns:
        Iterator[str]: Итератор фрагментов текста или событий.

    Как работает функция:
    - Функция принимает путь к директории бакета и флаги для удаления файлов, обработки с помощью `spacy` и генерации событий.
    - Если `refine_chunks_with_spacy` равно `True`, обрабатывает файлы с помощью `stream_read_parts_and_refine`.
    - Если `refine_chunks_with_spacy` равно `False`, обрабатывает файлы с помощью `stream_read_files` и `cache_stream`.
    - Если `event_stream` равно `True`, генерирует события для каждого обработанного фрагмента.
    """
```

**Примеры**:
```python
# Пример использования stream_chunks с указанием директории бакета
bucket_dir = Path("/path/to/bucket")
for chunk in stream_chunks(bucket_dir):
    print(chunk)
```

### `get_streaming`

```python
def get_streaming(bucket_dir: str, delete_files: bool = False, refine_chunks_with_spacy: bool = False, event_stream: bool = False) -> Iterator[str]:
    """
    Предоставляет потоковую обработку файлов в указанной директории бакета.

    Args:
        bucket_dir (str): Путь к директории бакета.
        delete_files (bool): Если `True`, файлы будут удалены после обработки. По умолчанию `False`.
        refine_chunks_with_spacy (bool): Если `True`, фрагменты текста будут обработаны с помощью `spacy`. По умолчанию `False`.
        event_stream (bool): Если `True`, будут генерироваться события для каждого обработанного фрагмента. По умолчанию `False`.

    Returns:
        Iterator[str]: Итератор фрагментов текста или событий.

    Как работает функция:
    - Функция принимает путь к директории бакета и флаги для удаления файлов, обработки с помощью `spacy` и генерации событий.
    - Создает директорию бакета, если она не существует.
    - Сначала обрабатывает файлы загрузок с помощью `read_and_download_urls`.
    - Затем обрабатывает остальные файлы в директории бакета с помощью `stream_chunks`.
    - Если происходит ошибка, генерирует событие с информацией об ошибке.
    """
```

**Примеры**:
```python
# Пример использования get_streaming с указанием директории бакета
bucket_dir = "/path/to/bucket"
for chunk in get_streaming(bucket_dir):
    print(chunk)
```

### `get_async_streaming`

```python
async def get_async_streaming(bucket_dir: str, delete_files: bool = False, refine_chunks_with_spacy: bool = False, event_stream: bool = False) -> Iterator[str]:
    """
    Асинхронно предоставляет потоковую обработку файлов в указанной директории бакета.

    Args:
        bucket_dir (str): Путь к директории бакета.
        delete_files (bool): Если `True`, файлы будут удалены после обработки. По умолчанию `False`.
        refine_chunks_with_spacy (bool): Если `True`, фрагменты текста будут обработаны с помощью `spacy`. По умолчанию `False`.
        event_stream (bool): Если `True`, будут генерироваться события для каждого обработанного фрагмента. По умолчанию `False`.

    Returns:
        Iterator[str]: Итератор фрагментов текста или событий.

    Как работает функция:
    - Функция принимает путь к директории бакета и флаги для удаления файлов, обработки с помощью `spacy` и генерации событий.
    - Создает директорию бакета, если она не существует.
    - Сначала асинхронно обрабатывает файлы загрузок с помощью `async_read_and_download_urls`.
    - Затем обрабатывает остальные файлы в директории бакета с помощью `stream_chunks`.
    - Если происходит ошибка, генерирует событие с информацией об ошибке.
    """
```

**Примеры**:
```python
# Пример использования get_async_streaming с указанием директории бакета
async def example():
    bucket_dir = "/path/to/bucket"
    for chunk in get_async_streaming(bucket_dir):
        print(chunk)