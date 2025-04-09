# Модуль для работы с файлами
=================================================

Модуль содержит функции для обработки различных типов файлов, включая текстовые, PDF, DOCX, ODT, EPUB, XLSX, HTML и ZIP архивы.
Он также включает в себя функции для скачивания файлов из интернета, кэширования и обработки текста с использованием библиотеки `spaCy`.

## Обзор

Этот модуль предоставляет набор инструментов для работы с файлами различных форматов,
включая их чтение, обработку и скачивание. Он предназначен для интеграции с другими
частями проекта `hypotez`, обеспечивая функциональность обработки файлов для различных задач.

## Подробнее

Модуль `files.py` предоставляет функции для работы с файлами различных форматов,
включая извлечение текста, скачивание файлов из интернета и предварительную обработку
текста с использованием библиотеки `spaCy`. Он включает в себя функции для:

- Безопасного создания имен файлов.
- Проверки поддержки формата файла.
- Чтения и обработки содержимого файлов различных форматов.
- Кэширования содержимого файлов для повышения производительности.
- Скачивания файлов из интернета с поддержкой рекурсивного скачивания ссылок с HTML-страниц.
- Разделения больших файлов на части для обработки.
- Потоковой передачи данных для эффективной обработки больших объемов информации.

Этот модуль играет важную роль в проекте `hypotez`, обеспечивая возможность обработки
файлов различных форматов, что необходимо для анализа данных и выполнения других задач.

## Функции

### `secure_filename`

```python
def secure_filename(filename: str) -> str:
    """Преобразует имя файла, удаляя небезопасные символы.

    Args:
        filename (str): Исходное имя файла.

    Returns:
        str: Безопасное имя файла.

    Как работает функция:
    1. Проверяет, что `filename` не равен `None`. Если `filename` равен `None`, функция возвращает `None`.
    2. Выполняет замену всех символов, которые не являются буквами, цифрами, символами из набора `.,_+-`, на символ `_`.
    3. Обрезает имя файла до 100 символов и удаляет символы `.,_-+` из начала и конца имени файла.

    ASCII flowchart:
    Проверка на None --> Замена небезопасных символов --> Обрезка имени файла --> Возврат безопасного имени

    Примеры:
        >>> secure_filename("безпечне ім'я.file")
        'безпечне_ім_я.file'
        >>> secure_filename("test file.txt")
        'test_file.txt'
        >>> secure_filename(None)
        None
    """
    ...
```

### `supports_filename`

```python
def supports_filename(filename: str) -> bool:
    """Проверяет, поддерживается ли указанный формат файла.

    Args:
        filename (str): Имя файла.

    Returns:
        bool: `True`, если формат файла поддерживается, `False` в противном случае.

    Raises:
        MissingRequirementsError: Если отсутствуют необходимые библиотеки для обработки определенного формата файла.

    Как работает функция:
    1. Проверяет расширение файла и наличие необходимых библиотек для его обработки.
    2. Для PDF, DOCX, ODT, EPUB, XLSX, HTML и ZIP определяет, установлены ли соответствующие библиотеки (PyPDF2, pdfplumber, pdfminer, docx, docx2txt, odfpy, ebooklib, pandas, beautifulsoup4).
    3. Если необходимые библиотеки отсутствуют, вызывает исключение `MissingRequirementsError`.
    4. Для файлов с расширениями из `PLAIN_FILE_EXTENSIONS` возвращает `True`.
    5. Для `package-lock.json` возвращает `False`.

    ASCII flowchart:
    Проверка расширения файла --> Проверка наличия библиотек --> Возврат результата

    Примеры:
        >>> supports_filename("example.pdf")
        True  # если установлены PyPDF2, pdfplumber или pdfminer
        >>> supports_filename("example.txt")
        True
        >>> supports_filename("package-lock.json")
        False
    """
    ...
```

### `get_bucket_dir`

```python
def get_bucket_dir(*parts) -> str:
    """Возвращает путь к каталогу bucket.

    Args:
        *parts: Части пути к каталогу.

    Returns:
        str: Полный путь к каталогу bucket.

    Как работает функция:
    1. Объединяет переданные части пути с путем к каталогу cookies.
    2. Использует `secure_filename` для каждой части пути для обеспечения безопасности имени.

    ASCII flowchart:
    Объединение частей пути --> Защита имени файла --> Возврат пути

    Примеры:
        >>> get_bucket_dir("test", "file.txt")
        '/path/to/cookies/buckets/test/file_txt'
    """
    ...
```

### `get_buckets`

```python
def get_buckets() -> Optional[List[str]]:
    """Получает список всех bucket.

    Returns:
        Optional[List[str]]: Список имен bucket или `None`, если каталог не существует.

    Как работает функция:
    1. Получает путь к каталогу buckets.
    2. Пытается получить список всех каталогов в каталоге buckets.
    3. Возвращает список имен каталогов или `None`, если каталог buckets не существует.

    ASCII flowchart:
    Получение пути к каталогу buckets --> Получение списка каталогов --> Возврат списка

    Примеры:
        >>> get_buckets()
        ['bucket1', 'bucket2']  # пример возвращаемого значения
    """
    ...
```

### `spacy_refine_chunks`

```python
def spacy_refine_chunks(source_iterator: Iterator[str]) -> Iterator[str]:
    """Обрабатывает текст с использованием библиотеки spaCy для извлечения значимых фрагментов.

    Args:
        source_iterator (Iterator[str]): Итератор строк для обработки.

    Returns:
        Iterator[str]: Итератор обработанных строк.

    Raises:
        MissingRequirementsError: Если библиотека spaCy не установлена.

    Как работает функция:
    1. Проверяет, установлена ли библиотека spaCy. Если нет, вызывает исключение `MissingRequirementsError`.
    2. Загружает модель `en_core_web_sm` из spaCy.
    3. Для каждой страницы текста в `source_iterator` выполняет обработку с использованием spaCy.
    4. Извлекает предложения и возвращает их в виде итератора.

    ASCII flowchart:
    Проверка spaCy --> Загрузка модели --> Обработка текста --> Извлечение предложений --> Возврат итератора

    Примеры:
        >>> source_data = ["This is a sentence. This is another sentence."]
        >>> iterator = iter(source_data)
        >>> for chunk in spacy_refine_chunks(iterator):
        ...     print(chunk)
        This is a sentence.
        This is another sentence.
    """
    ...
```

### `get_filenames`

```python
def get_filenames(bucket_dir: Path) -> list[str]:
    """Получает список имен файлов из файла `FILE_LIST` в указанном каталоге.

    Args:
        bucket_dir (Path): Путь к каталогу bucket.

    Returns:
        list[str]: Список имен файлов.

    Как работает функция:
    1. Формирует путь к файлу `FILE_LIST` в каталоге `bucket_dir`.
    2. Проверяет, существует ли файл `FILE_LIST`.
    3. Если файл существует, открывает его и считывает список имен файлов, удаляя пробельные символы в начале и конце каждой строки.
    4. Если файл не существует, возвращает пустой список.

    ASCII flowchart:
    Формирование пути к файлу --> Проверка существования файла --> Чтение списка файлов --> Возврат списка

    Примеры:
        >>> bucket_dir = Path("/path/to/bucket")
        >>> # Если файл FILE_LIST содержит "file1.txt\\nfile2.txt", функция вернет ['file1.txt', 'file2.txt']
        >>> get_filenames(bucket_dir)
        ['file1.txt', 'file2.txt']
    """
    ...
```

### `stream_read_files`

```python
def stream_read_files(bucket_dir: Path, filenames: list, delete_files: bool = False) -> Iterator[str]:
    """Читает содержимое файлов из указанного каталога, поддерживая различные форматы и ZIP архивы.

    Args:
        bucket_dir (Path): Путь к каталогу bucket.
        filenames (list): Список имен файлов для чтения.
        delete_files (bool, optional): Если `True`, файлы будут удалены после чтения. По умолчанию `False`.

    Yields:
        Iterator[str]: Итератор содержимого файлов.

    Как работает функция:
    1. Итерируется по списку имен файлов.
    2. Формирует путь к файлу на основе `bucket_dir` и имени файла.
    3. Проверяет существование файла и его размер (должен быть больше 0). Если файл не существует или его размер равен 0, переходит к следующему файлу.
    4. Если файл является ZIP архивом, извлекает все файлы из архива в `bucket_dir` и рекурсивно вызывает `stream_read_files` для обработки извлеченных файлов.
    5. Для каждого поддерживаемого формата файла (PDF, DOCX, ODT, EPUB, XLSX, HTML, TXT и другие) открывает файл и извлекает текст.
    6. Возвращает текст файла в виде итератора.
    7. Если `delete_files` равен `True`, удаляет файлы после чтения.

    ASCII flowchart:
    Итерация по файлам --> Проверка файла --> Обработка ZIP --> Чтение файла --> Возврат текста --> Удаление файла

    Примеры:
        >>> bucket_dir = Path("/path/to/bucket")
        >>> filenames = ["file1.txt", "file2.pdf"]
        >>> for chunk in stream_read_files(bucket_dir, filenames):
        ...     print(chunk)
        "Content of file1.txt"
        "Content of file2.pdf"
    """
    ...
```

### `cache_stream`

```python
def cache_stream(stream: Iterator[str], bucket_dir: Path) -> Iterator[str]:
    """Кэширует содержимое потока данных в файл.

    Args:
        stream (Iterator[str]): Итератор строк для кэширования.
        bucket_dir (Path): Путь к каталогу bucket.

    Yields:
        Iterator[str]: Итератор строк, идентичный входному потоку.

    Как работает функция:
    1. Формирует пути к файлу кэша и временному файлу.
    2. Если файл кэша существует, читает его содержимое и возвращает в виде итератора.
    3. Если файл кэша не существует, открывает временный файл для записи.
    4. Итерируется по входному потоку, записывает каждый фрагмент во временный файл и возвращает его.
    5. После завершения записи переименовывает временный файл в файл кэша.

    ASCII flowchart:
    Проверка кэша --> Чтение кэша (если есть) --> Запись во временный файл --> Переименование файла --> Возврат итератора

    Примеры:
        >>> bucket_dir = Path("/path/to/bucket")
        >>> data = ["chunk1", "chunk2"]
        >>> stream = iter(data)
        >>> for chunk in cache_stream(stream, bucket_dir):
        ...     print(chunk)
        "chunk1"
        "chunk2"
    """
    ...
```

### `is_complete`

```python
def is_complete(data: str) -> bool:
    """Проверяет, является ли переданная строка завершенным блоком данных.

    Args:
        data (str): Строка данных для проверки.

    Returns:
        bool: `True`, если строка завершена, `False` в противном случае.

    Как работает функция:
    1. Проверяет, заканчивается ли строка на "\\n```\\n\\n".
    2. Проверяет, является ли количество "```" в строке четным числом.
    3. Возвращает `True`, если оба условия выполняются, `False` в противном случае.

    ASCII flowchart:
    Проверка окончания строки --> Проверка количества "```" --> Возврат результата

    Примеры:
        >>> is_complete("Some text\\n```\\n\\n")
        True
        >>> is_complete("Some text```")
        False
    """
    ...
```

### `read_path_chunked`

```python
def read_path_chunked(path: Path) -> Iterator[str]:
    """Читает файл по частям, разделяя его на фрагменты.

    Args:
        path (Path): Путь к файлу.

    Yields:
        Iterator[str]: Итератор фрагментов файла.

    Как работает функция:
    1. Открывает файл для чтения в кодировке UTF-8.
    2. Итерируется по строкам файла.
    3. Накапливает строки в буфере, пока размер буфера не достигнет 4096 байт.
    4. Если размер буфера превышает 4096 байт, проверяет, является ли буфер завершенным блоком данных с помощью функции `is_complete`.
    5. Если буфер завершен или его размер превышает 8192 байта, возвращает буфер и очищает его.
    6. После завершения чтения файла возвращает оставшийся буфер, если он не пуст.

    ASCII flowchart:
    Открытие файла --> Чтение строк --> Накопление буфера --> Проверка размера буфера --> Проверка завершенности --> Возврат буфера

    Примеры:
        >>> file_path = Path("/path/to/file.txt")
        >>> # Если файл содержит "Line 1\\nLine 2\\n```\\n\\nLine 3", функция вернет "Line 1\\nLine 2\\n```\\n\\n" и "Line 3"
        >>> for chunk in read_path_chunked(file_path):
        ...     print(chunk)
        "Line 1\\nLine 2\\n```\\n\\n"
        "Line 3"
    """
    ...
```

### `read_bucket`

```python
def read_bucket(bucket_dir: Path) -> Iterator[str]:
    """Читает содержимое bucket из кэшированных файлов.

    Args:
        bucket_dir (Path): Путь к каталогу bucket.

    Yields:
        Iterator[str]: Итератор содержимого файлов.

    Как работает функция:
    1. Формирует пути к файлам кэша.
    2. Проверяет наличие файлов кэша `spacy_0001.cache` и `plain.cache`. Если `spacy_0001.cache` не существует, а `plain.cache` существует, читает и возвращает содержимое `plain.cache`.
    3. Итерируется по файлам `spacy_{idx:04d}.cache` и `plain_{idx:04d}.cache` (где idx от 1 до 999).
    4. Если файл `spacy_{idx:04d}.cache` существует, читает и возвращает его содержимое.
    5. Если файл `plain_{idx:04d}.cache` существует, читает и возвращает его содержимое.
    6. Если ни один из файлов не существует, завершает итерацию.

    ASCII flowchart:
    Проверка кэша --> Чтение кэша --> Итерация по файлам --> Чтение файлов --> Завершение

    Примеры:
        >>> bucket_dir = Path("/path/to/bucket")
        >>> # Если существует файл spacy_0001.cache с содержимым "chunk1", функция вернет "chunk1"
        >>> for chunk in read_bucket(bucket_dir):
        ...     print(chunk)
        "chunk1"
    """
    ...
```

### `stream_read_parts_and_refine`

```python
def stream_read_parts_and_refine(bucket_dir: Path, delete_files: bool = False) -> Iterator[str]:
    """Читает части файла и обрабатывает их с использованием spaCy.

    Args:
        bucket_dir (Path): Путь к каталогу bucket.
        delete_files (bool, optional): Если `True`, файлы будут удалены после обработки. По умолчанию `False`.

    Yields:
        Iterator[str]: Итератор обработанных фрагментов файла.

    Как работает функция:
    1. Формирует пути к файлам кэша и частям файлов.
    2. Проверяет наличие файлов `spacy_0001.cache`, `plain_0001.cache` и `PLAIN_CACHE`. Если `spacy_0001.cache` и `plain_0001.cache` не существуют, а `PLAIN_CACHE` существует, вызывает функцию `split_file_by_size_and_newline` для разделения `PLAIN_CACHE` на части.
    3. Итерируется по файлам `plain_{idx:04d}.cache` (где idx от 1 до 999).
    4. Если файл `spacy_{idx:04d}.cache` существует, читает и возвращает его содержимое.
    5. Если файл `plain_{idx:04d}.cache` не существует, завершает итерацию.
    6. Открывает временный файл для записи обработанных данных.
    7. Обрабатывает каждый фрагмент файла с помощью функции `spacy_refine_chunks`, записывает результат во временный файл и возвращает его.
    8. Переименовывает временный файл в файл `spacy_{idx:04d}.cache`.
    9. Если `delete_files` равен `True`, удаляет файл `plain_{idx:04d}.cache`.

    ASCII flowchart:
    Проверка файлов --> Разделение файла на части --> Итерация по частям --> Обработка spaCy --> Запись во временный файл --> Переименование файла --> Удаление файла

    Примеры:
        >>> bucket_dir = Path("/path/to/bucket")
        >>> # Если существуют файлы plain_0001.cache и plain_0002.cache, функция обработает их и вернет обработанные фрагменты
        >>> for chunk in stream_read_parts_and_refine(bucket_dir):
        ...     print(chunk)
        "Processed chunk 1"
        "Processed chunk 2"
    """
    ...
```

### `split_file_by_size_and_newline`

```python
def split_file_by_size_and_newline(input_filename: str, output_dir: str, chunk_size_bytes: int = 1024*1024):
    """Разделяет файл на части заданного размера, разделяя только по символу новой строки.

    Args:
        input_filename (str): Путь к входному файлу.
        output_dir (str): Префикс для выходных файлов (например, 'output_part_').
        chunk_size_bytes (int, optional): Желаемый размер каждой части в байтах. По умолчанию 1MB.

    Как работает функция:
    1. Формирует префикс имени выходного файла на основе имени входного файла и выходного каталога.
    2. Открывает входной файл для чтения в кодировке UTF-8.
    3. Инициализирует переменные для отслеживания номера части, текущего фрагмента и его размера.
    4. Итерируется по строкам входного файла.
    5. Добавляет каждую строку к текущему фрагменту и увеличивает размер фрагмента.
    6. Если размер фрагмента превышает `chunk_size_bytes`, проверяет, является ли фрагмент завершенным блоком данных с помощью функции `is_complete`.
    7. Если фрагмент завершен или его размер превышает `chunk_size_bytes * 2`, записывает фрагмент в выходной файл, очищает текущий фрагмент и сбрасывает его размер.
    8. После завершения чтения входного файла записывает последний фрагмент в выходной файл, если он не пуст.

    ASCII flowchart:
    Формирование префикса имени --> Открытие входного файла --> Инициализация переменных --> Итерация по строкам --> Добавление строки к фрагменту --> Проверка размера фрагмента --> Запись фрагмента в файл

    Примеры:
        >>> split_file_by_size_and_newline("/path/to/input.txt", "/path/to/output", chunk_size_bytes=500)
        # Создаст файлы output_0001.txt, output_0002.txt и т.д., каждый размером около 500 байт
    """
    ...
```

### `get_filename`

```python
async def get_filename(response: ClientResponse) -> Optional[str]:
    """Пытается извлечь имя файла из ответа aiohttp.

    Args:
        response: Объект aiohttp ClientResponse.

    Returns:
        Имя файла в виде строки или None, если не удалось определить имя файла.

    Как работает функция:
    1. Пытается получить имя файла из заголовка Content-Disposition.
    2. Если заголовок Content-Disposition отсутствует или не содержит имени файла, пытается определить имя файла на основе URL и заголовка Content-Type.
        2.1 Получает тип контента из заголовка Content-Type
        2.2 Если  тип контента содержится в url
            2.2.1 Получает расширение из URL
            2.2.2 Хэширует SHA256 url в base32
            2.2.3 Генерирует имя файла на основе netloc, url_path, hash и расширения
    3. Если имя файла не может быть определено, возвращает None.

    ASCII flowchart:
    Content-Disposition -> Извлечение имени файла -> URL + Content-Type -> Определение расширения -> Хэширование URL -> Генерация имени файла -> None

    Примеры:
        >>> response = ClientResponse(...)
        >>> response.headers['Content-Disposition'] = 'filename="example.txt"'
        >>> await get_filename(response)
        'example.txt'
    """
    ...
```

### `get_file_extension`

```python
async def get_file_extension(response: ClientResponse) -> Optional[str]:
    """Пытается определить расширение файла из ответа aiohttp.

    Args:
        response: Объект aiohttp ClientResponse.

    Returns:
        Расширение файла (например, ".html", ".json", ".pdf", ".zip", ".md", ".txt") в виде строки или None,
        если не удалось определить расширение.

    Как работает функция:
    1. Пытается получить тип контента из заголовка Content-Type.
    2. На основе типа контента определяет расширение файла.
    3. Если тип контента не содержит информации о расширении, пытается извлечь расширение из URL.
    4. Если расширение не может быть определено, возвращает None.

    ASCII flowchart:
    Content-Type -> Определение расширения -> URL -> Извлечение расширения -> None

    Примеры:
        >>> response = ClientResponse(...)
        >>> response.headers['Content-Type'] = 'application/pdf'
        >>> await get_file_extension(response)
        '.pdf'
    """
    ...
```

### `read_links`

```python
def read_links(html: str, base: str) -> set[str]:
    """Извлекает ссылки из HTML-кода, учитывая базовый URL.

    Args:
        html: HTML-код для анализа.
        base: Базовый URL для объединения относительных ссылок.

    Returns:
        Набор URL в виде строк.

    Как работает функция:
    1. Использует BeautifulSoup для разбора HTML-кода.
    2. Выбирает основной контент из HTML, используя селекторы CSS для поиска блоков основного контента.
    3. Извлекает все ссылки (теги `<a>`) из выбранного контента.
    4. Фильтрует ссылки, исключая ссылки с атрибутом `rel="nofollow"`.
    5. Объединяет относительные ссылки с базовым URL.
    6. Возвращает набор уникальных URL.

    ASCII flowchart:
    HTML -> BeautifulSoup -> Выбор контента -> Извлечение ссылок -> Фильтрация ссылок -> Объединение с базовым URL -> Набор URL

    Примеры:
        >>> html = '<a href="https://example.com">Example</a> <a href="/about">About</a>'
        >>> base = 'https://base.com'
        >>> read_links(html, base)
        {'https://example.com', 'https://base.com/about'}
    """
    ...
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
    """Асинхронно скачивает файлы по указанным URL, с возможностью рекурсивного скачивания ссылок с HTML-страниц.

    Args:
        bucket_dir: Путь к каталогу bucket для сохранения скачанных файлов.
        urls: Список URL для скачивания.
        max_depth: Максимальная глубина рекурсивного скачивания ссылок с HTML-страниц. По умолчанию 0 (отключено).
        loading_urls: Набор URL, которые уже находятся в процессе скачивания (используется для предотвращения дублирования).
        lock: Объект asyncio.Lock для синхронизации доступа к общим ресурсам (например, списку `loading_urls`).
        delay: Задержка в секундах между запросами.
        new_urls: Список для добавления новых URL, найденных на HTML-страницах.
        group_size: Размер группы URL для параллельного скачивания.
        timeout: Время ожидания ответа от сервера в секундах.
        proxy: Прокси-сервер для использования при скачивании.

    Yields:
        Имя скачанного файла.

    Как работает функция:
    1. Инициализирует асинхронную сессию aiohttp с заданным таймаутом и прокси.
    2. Определяет асинхронную функцию `download_url` для скачивания файла по одному URL.
    3. В функции `download_url`:
        - Отправляет GET-запрос по URL.
        - Извлекает имя файла из ответа сервера.
        - Если имя файла не удалось извлечь или расширение файла не поддерживается, прекращает обработку URL.
        - Если файл является HTML-страницей и `max_depth` > 0:
            - Извлекает ссылки с HTML-страницы с помощью функции `read_links`.
            - Добавляет новые ссылки в список `new_urls` для дальнейшего скачивания.
        - Сохраняет скачанный файл в каталоге `bucket_dir`.
    4. Параллельно запускает скачивание файлов по списку URL с использованием `asyncio.gather`.
    5. Рекурсивно вызывает `download_urls` для скачивания новых URL, найденных на HTML-страницах, пока `max_depth` не будет достигнута.
    6. Использует `asyncio.Lock` для синхронизации доступа к общим ресурсам, таким как списки `loading_urls` и `new_urls`.

    ASCII flowchart:
    Инициализация сессии -> Параллельное скачивание файлов -> Скачивание URL -> Обработка HTML (рекурсия)

    Примеры:
        >>> bucket_dir = Path("/path/to/bucket")
        >>> urls = ["https://example.com/file1.txt", "https://example.com/file2.txt"]
        >>> async for filename in download_urls(bucket_dir, urls):
        ...     print(filename)
        file1.txt
        file2.txt
    """
    ...
```

### `get_downloads_urls`

```python
def get_downloads_urls(bucket_dir: Path, delete_files: bool = False) -> Iterator[str]:
    """Получает список URL для скачивания из файла `DOWNLOADS_FILE` в указанном каталоге.

    Args:
        bucket_dir: Путь к каталогу bucket.
        delete_files: Если True, файл `DOWNLOADS_FILE` будет удален после чтения.

    Yields:
        Словарь с информацией о URL для скачивания.

    Как работает функция:
    1. Формирует путь к файлу `DOWNLOADS_FILE` в каталоге `bucket_dir`.
    2. Проверяет, существует ли файл `DOWNLOADS_FILE`.
    3. Если файл существует:
        - Открывает файл и загружает данные из него в формате JSON.
        - Если `delete_files` равно True, удаляет файл `DOWNLOADS_FILE`.
        - Итерируется по списку элементов в загруженных данных.
        - Для каждого элемента проверяет наличие ключей "url" или "urls".
        - Возвращает словарь с информацией о URL для скачивания.

    ASCII flowchart:
    Проверка DOWNLOADS_FILE -> Чтение JSON -> Удаление DOWNLOADS_FILE -> Итерация по URL

    Примеры:
        >>> bucket_dir = Path("/path/to/bucket")
        >>> # Если файл DOWNLOADS_FILE содержит '[{"url": "https://example.com/file1.txt"}]',
        >>> # функция вернет {"urls": ["https://example.com/file1.txt"]}
        >>> for item in get_downloads_urls(bucket_dir):
        ...     print(item)
        {'urls': ['https://example.com/file1.txt']}
    """
    ...
```

### `read_and_download_urls`

```python
def read_and_download_urls(bucket_dir: Path, delete_files: bool = False, event_stream: bool = False) -> Iterator[str]:
    """Читает список URL из файла загрузок, скачивает файлы и записывает имена скачанных файлов в файл списка файлов.

    Args:
        bucket_dir: Путь к каталогу bucket.
        delete_files: Если True, файл загрузок будет удален после чтения.
        event_stream: Если True, возвращает события в формате JSON для потоковой передачи.

    Yields:
        Имена скачанных файлов или события в формате JSON для потоковой передачи.

    Как работает функция:
    1. Получает список URL из файла загрузок с помощью функции `get_downloads_urls`.
    2. Если список URL не пуст:
        - Открывает файл списка файлов для добавления имен скачанных файлов.
        - Для каждого URL скачивает файлы с помощью функции `download_urls`.
        - Записывает имя каждого скачанного файла в файл списка файлов.
        - Если `event_stream` равно True, формирует и возвращает событие в формате JSON для потоковой передачи.

    ASCII flowchart:
    Получение списка URL -> Скачивание файлов -> Запись имен файлов -> Потоковая передача событий (опционально)

    Примеры:
        >>> bucket_dir = Path("/path/to/bucket")
        >>> # Если файл загрузок содержит '[{"url": "https://example.com/file1.txt"}]',
        >>> # функция скачает file1.txt и запишет его имя в файл списка файлов
        >>> for item in read_and_download_urls(bucket_dir):
        ...     print(item)
        file1.txt
    """
    ...
```

### `async_read_and_download_urls`

```python
async def async_read_and_download_urls(bucket_dir: Path, delete_files: bool = False, event_stream: bool = False) -> AsyncIterator[str]:
    """Асинхронно читает список URL из файла загрузок, скачивает файлы и записывает имена скачанных файлов в файл списка файлов.

    Args:
        bucket_dir: Путь к каталогу bucket.
        delete_files: Если True, файл загрузок будет удален после чтения.
        event_stream: Если True, возвращает события в формате JSON для потоковой передачи.

    Yields:
        Имена скачанных файлов или события в формате JSON для потоковой передачи.

    Как работает функция:
    1. Получает список URL из файла загрузок с помощью функции `get_downloads_urls`.
    2. Если список URL не пуст:
        - Открывает файл списка файлов для добавления имен скачанных файлов.
        - Для каждого URL асинхронно скачивает файлы с помощью функции `download_urls`.
        - Записывает имя каждого скачанного файла в файл списка файлов.
        - Если `event_stream` равно True, формирует и возвращает событие в формате JSON для потоковой передачи.

    ASCII flowchart:
    Получение списка URL -> Асинхронное скачивание файлов -> Запись имен файлов -> Потоковая передача событий (опционально)

    Примеры:
        >>> bucket_dir = Path("/path/to/bucket")
        >>> # Если файл загрузок содержит '[{"url": "https://example.com/file1.txt"}]',
        >>> # функция асинхронно скачает file1.txt и запишет его имя в файл списка файлов
        >>> async for item in async_read_and_download_urls(bucket_dir):
        ...     print(item)
        file1.txt
    """
    ...
```

### `stream_chunks`

```python
def stream_chunks(bucket_dir: Path, delete_files: bool = False, refine_chunks_with_spacy: bool = False, event_stream: bool = False) -> Iterator[str]:
    """Создает поток фрагментов текста из файлов в указанном каталоге.

    Args:
        bucket_dir: Путь к каталогу bucket.
        delete_files: Если True, файлы будут удалены после обработки.
        refine_chunks_with_spacy: Если True, фрагменты текста будут обработаны с использованием spaCy.
        event_stream: Если True, возвращает события в формате JSON для потоковой передачи.

    Yields:
        Фрагменты текста или события в формате JSON для потоковой передачи.

    Как работает функция:
    1. Определяет, нужно ли использовать spaCy для обработки фрагментов текста.
    2. Если `refine_chunks_with