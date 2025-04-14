# Модуль `src.webdriver.bs`

## Обзор

Модуль `src.webdriver.bs` предназначен для парсинга HTML-контента с использованием библиотек `BeautifulSoup` и `lxml` с поддержкой XPath. Он предоставляет класс `BS` для получения и обработки HTML-страниц из файлов или URL-адресов, а также для выполнения XPath-запросов к содержимому.

## Подробнее

Модуль облегчает извлечение данных из веб-страниц, позволяя указать URL или путь к файлу, загрузить содержимое и выполнить XPath-запросы для поиска нужных элементов. Класс `BS` инкапсулирует функциональность парсинга, предоставляя простой интерфейс для взаимодействия с HTML-контентом. Этот модуль может быть использован для автоматизации сбора данных, тестирования веб-сайтов и других задач, требующих анализа HTML-структуры.

## Классы

### `BS`

**Описание**: Класс `BS` предназначен для парсинга HTML-контента с использованием BeautifulSoup и XPath.

**Принцип работы**:
1.  **Инициализация**: При инициализации класса можно указать URL или путь к файлу. Если URL указан, происходит загрузка HTML-контента.
2.  **Загрузка контента**: Метод `get_url` загружает HTML-контент из указанного URL или файла. Поддерживаются как локальные файлы (с префиксом `file://`), так и веб-страницы (с префиксом `https://`).
3.  **Выполнение XPath-запросов**: Метод `execute_locator` выполняет XPath-запрос к загруженному HTML-контенту и возвращает список найденных элементов.
4.  **Использование BeautifulSoup и lxml**: Для парсинга используется `BeautifulSoup` для предварительной обработки, а `lxml` для выполнения XPath-запросов.

**Атрибуты**:

*   `html_content` (str): HTML-контент, который будет парситься.

**Методы**:

*   `__init__(url: Optional[str] = None)`: Инициализирует экземпляр класса `BS`.
*   `get_url(url: str) -> bool`: Загружает HTML-контент из URL или файла.
*   `execute_locator(locator: Union[SimpleNamespace, dict], url: Optional[str] = None) -> List[etree._Element]`: Выполняет XPath-запрос к HTML-контенту.

### `__init__`

```python
def __init__(self, url: Optional[str] = None):
    """
    Initializes the BS parser with an optional URL.

    :param url: The URL or file path to fetch HTML content from.
    :type url: Optional[str]
    """
    if url:
        self.get_url(url)
```

**Назначение**: Инициализирует класс `BS` с возможностью сразу загрузить HTML-контент из указанного URL.

**Параметры**:

*   `url` (Optional[str], optional): URL или путь к файлу, из которого необходимо загрузить HTML-контент. По умолчанию `None`.

**Как работает функция**:
1. Проверяет, был ли передан URL при инициализации.
2. Если URL был передан, вызывает метод `get_url` для загрузки HTML-контента.

```mermaid
graph TD
    A[Начало] --> B{URL передан?};
    B -- Да --> C[Вызов get_url(url)];
    B -- Нет --> D[Конец];
    C --> D;
    D[Конец];
```

**Примеры**:

```python
# Инициализация без URL
parser = BS()

# Инициализация с URL
parser = BS('https://example.com')
```

### `get_url`

```python
def get_url(self, url: str) -> bool:
    """
    Fetch HTML content from a file or URL and parse it with BeautifulSoup and XPath.

    :param url: The file path or URL to fetch HTML content from.
    :type url: str
    :return: True if the content was successfully fetched, False otherwise.
    :rtype: bool
    """
    if url.startswith('file://'):
        # Remove 'file://' prefix and clean up the path
        cleaned_url = url.replace(r'file:///', '')

        # Extract the Windows path if it's in the form of 'c:/...' or 'C:/...'
        match = re.search(r'[a-zA-Z]:[\\\\/].*', cleaned_url)
        if match:
            file_path = Path(match.group(0))
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        self.html_content = file.read()
                    return True
                except Exception as ex:
                    logger.error('Exception while reading the file:', ex)
                    return False
            else:
                logger.error('Local file not found:', file_path)
                return False
        else:
            logger.error('Invalid file path:', cleaned_url)
            return False
    elif url.startswith('https://'):
        # Handle web URLs
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP request errors
            self.html_content = response.text
            return True
        except requests.RequestException as ex:
            logger.error(f"Error fetching {url}:", ex)
            return False
    else:
        logger.error('Invalid URL or file path:', url)
        return False
```

**Назначение**: Загружает HTML-контент из указанного URL или файла.

**Параметры**:

*   `url` (str): URL или путь к файлу, из которого необходимо загрузить HTML-контент.

**Возвращает**:

*   `bool`: `True`, если контент успешно загружен, `False` в противном случае.

**Вызывает исключения**:

*   `requests.RequestException`: Если возникает ошибка при выполнении HTTP-запроса.
*   `Exception`: Если возникает ошибка при чтении файла.

**Как работает функция**:

1.  **Проверка типа URL**: Определяет, является ли URL файловым (начинается с `file://`) или веб-адресом (начинается с `https://`).
2.  **Обработка файловых URL**:
    *   Удаляет префикс `file:///` из URL.
    *   Извлекает путь к файлу, используя регулярное выражение.
    *   Проверяет существование файла.
    *   Пытается открыть и прочитать файл, устанавливая `html_content`.
    *   В случае ошибки логирует исключение и возвращает `False`.
3.  **Обработка веб-URL**:
    *   Выполняет HTTP-запрос к указанному URL.
    *   Проверяет статус ответа (возбуждает исключение, если статус код не 200).
    *   Устанавливает `html_content` равным тексту ответа.
    *   В случае ошибки логирует исключение и возвращает `False`.
4.  **Обработка некорректных URL**: Если URL не соответствует ни одному из известных форматов, логирует ошибку и возвращает `False`.

```mermaid
graph TD
    A[Начало] --> B{URL начинается с 'file://'?};
    B -- Да --> C[Удаление префикса 'file:///'];
    C --> D[Извлечение пути к файлу];
    D --> E{Файл существует?};
    E -- Да --> F[Открытие и чтение файла];
    F --> G{Успешно?};
    G -- Да --> H[html_content = содержимое файла];
    H --> I[Возврат True];
    G -- Нет --> J[Логирование ошибки];
    J --> K[Возврат False];
    E -- Нет --> L[Логирование ошибки 'Local file not found'];
    L --> K;
    B -- Нет --> M{URL начинается с 'https://'?};
    M -- Да --> N[Выполнение HTTP-запроса];
    N --> O{Успешно?};
    O -- Да --> P[html_content = текст ответа];
    P --> I;
    O -- Нет --> Q[Логирование ошибки];
    Q --> K;
    M -- Нет --> R[Логирование ошибки 'Invalid URL or file path'];
    R --> K;
    K --> I[Возврат False];
    I[Возврат True];
```

**Примеры**:

```python
# Загрузка из файла
parser = BS()
result = parser.get_url('file:///c:/path/to/file.html')

# Загрузка из веб-URL
parser = BS()
result = parser.get_url('https://example.com')
```

### `execute_locator`

```python
def execute_locator(self, locator: Union[SimpleNamespace, dict], url: Optional[str] = None) -> List[etree._Element]:
    """
    Execute an XPath locator on the HTML content.

    :param locator: The locator object containing the selector and attribute.
    :type locator: Union[SimpleNamespace, dict]
    :param url: Optional URL or file path to fetch HTML content from.
    :type url: Optional[str]
    :return: A list of elements matching the locator.
    :rtype: List[etree._Element]
    """
    if url:
        self.get_url(url)

    if not self.html_content:
        logger.error('No HTML content available for parsing.')
        return []

    soup = BeautifulSoup(self.html_content, 'lxml')
    tree = etree.HTML(str(soup))  # Convert BeautifulSoup object to lxml tree

    if isinstance(locator, dict):
        locator = SimpleNamespace(**locator)

    attribute = locator.attribute
    by = locator.by.upper()
    selector = locator.selector
    elements = None

    if by == 'ID':
        elements = tree.xpath(f'//*[@id="{attribute}"]')
    elif by == 'CSS':
        elements = tree.xpath(f'//*[contains(@class, "{attribute}")]')
    elif by == 'TEXT':
        elements = tree.xpath(f'//input[@type="{attribute}"]')
    else:
        elements = tree.xpath(selector)

    return elements
```

**Назначение**: Выполняет XPath-запрос к HTML-контенту.

**Параметры**:

*   `locator` (Union[SimpleNamespace, dict]): Объект локатора, содержащий селектор и атрибут.
*   `url` (Optional[str], optional): URL или путь к файлу, из которого необходимо загрузить HTML-контент. По умолчанию `None`.

**Возвращает**:

*   `List[etree._Element]`: Список элементов, соответствующих локатору.

**Как работает функция**:

1.  **Загрузка HTML-контента**: Если передан URL, загружает HTML-контент с помощью `get_url`.
2.  **Проверка наличия контента**: Проверяет, был ли загружен HTML-контент. Если нет, логирует ошибку и возвращает пустой список.
3.  **Инициализация BeautifulSoup и lxml**: Инициализирует `BeautifulSoup` и `lxml` для парсинга HTML-контента.
4.  **Преобразование локатора**: Преобразует локатор из словаря в `SimpleNamespace`, если это необходимо.
5.  **Выполнение XPath-запроса**: Выполняет XPath-запрос на основе типа локатора (`ID`, `CSS`, `TEXT` или общий XPath).
6.  **Возврат результатов**: Возвращает список найденных элементов.

```mermaid
graph TD
    A[Начало] --> B{URL передан?};
    B -- Да --> C[Вызов get_url(url)];
    B -- Нет --> D{html_content существует?};
    C --> D;
    D -- Нет --> E[Логирование ошибки 'No HTML content available'];
    E --> F[Возврат []];
    D -- Да --> G[Инициализация BeautifulSoup и lxml];
    G --> H{locator - словарь?};
    H -- Да --> I[Преобразование в SimpleNamespace];
    H -- Нет --> J[Извлечение атрибутов локатора];
    I --> J;
    J --> K{by == 'ID'?};
    K -- Да --> L[Выполнение XPath-запроса по ID];
    K -- Нет --> M{by == 'CSS'?};
    L --> N[Возврат elements];
    M -- Да --> O[Выполнение XPath-запроса по CSS];
    O --> N;
    M -- Нет --> P{by == 'TEXT'?};
    P -- Да --> Q[Выполнение XPath-запроса по TEXT];
    Q --> N;
    P -- Нет --> R[Выполнение XPath-запроса по selector];
    R --> N;
    F --> N;
```

**Примеры**:

```python
# Инициализация парсера
parser = BS()
parser.get_url('https://example.com')

# Определение локатора
locator = SimpleNamespace(by='ID', attribute='element_id', selector='//*[@id="element_id"]')

# Выполнение локатора
elements = parser.execute_locator(locator)
print(elements)

# Определение локатора в виде словаря
locator_dict = {'by': 'ID', 'attribute': 'element_id', 'selector': '//*[@id="element_id"]'}

# Выполнение локатора
elements = parser.execute_locator(locator_dict)
print(elements)
```