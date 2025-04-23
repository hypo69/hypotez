# Модуль `src.goog.google_search`

## Обзор

Модуль предназначен для парсинга HTML-страниц поисковой выдачи Google с целью извлечения структурированных данных, таких как органические результаты поиска, "featured snippets" и карточки знаний. Он предоставляет класс `GoogleHtmlParser`, который обрабатывает HTML-код и извлекает необходимую информацию.

## Подробнее

Модуль облегчает автоматизированный сбор данных из поисковой выдачи Google, что может быть полезно для анализа поисковых результатов, мониторинга позиций веб-сайтов и других задач, связанных с поисковой оптимизацией и анализом данных.

## Классы

### `GoogleHtmlParser`

**Описание**: Класс предназначен для парсинга HTML-страниц, полученных из поисковой выдачи Google. Он может работать как с десктопной, так и с мобильной версиями HTML.

**Атрибуты**:
- `tree` (html.Element): Дерево документа, представляющее HTML-структуру страницы, созданное с помощью `html.fromstring()`.
- `user_agent` (str): User agent, использованный для получения HTML Google Search. Определяет, какая версия HTML (мобильная или десктопная) будет обрабатываться.

**Методы**:

- `__init__(self, html_str: str, user_agent: str = 'desktop') -> None`: Инициализирует экземпляр класса `GoogleHtmlParser`.
- `_clean(self, content: str) -> str`: Очищает входную строку от лишних пробелов и символов.
- `_normalize_dict_key(self, content: str) -> str`: Преобразует строку для использования в качестве ключа в словаре, заменяя пробелы на подчеркивания, удаляя двоеточия и приводя к нижнему регистру.
- `_get_estimated_results(self) -> int`: Извлекает количество найденных результатов поиска (для десктопной версии).
- `_get_organic(self) -> list`: Извлекает органические результаты поиска без дополнительных элементов, таких как сниппеты.
- `_get_featured_snippet(self) -> dict | None`: Извлекает "featured snippet" (если он есть) с заголовком и URL.
- `_get_knowledge_card(self) -> dict | None`: Извлекает карточку знаний (если она есть) с заголовком, подзаголовком и описанием.
- `_get_scrolling_sections(self) -> list`: Извлекает данные из скроллируемых виджетов, например, "топовые истории" или "твиты".
- `get_data(self) -> dict`: Собирает итоговые данные с поисковой страницы, включая органические результаты, карточку знаний и другие элементы.

### `__init__(self, html_str: str, user_agent: str = 'desktop') -> None`

**Назначение**: Инициализация парсера.

**Параметры**:
- `html_str` (str): HTML Google Search в виде строки.
- `user_agent` (str): User agent для получения HTML. Может быть 'mobile' или 'desktop'. По умолчанию 'desktop'.

**Как работает функция**:

- Функция инициализирует парсер, создавая дерево документа из HTML-строки с использованием `html.fromstring()`.
- Затем она проверяет, является ли предоставленный `user_agent` допустимым ('mobile' или 'desktop'). Если `user_agent` допустим, он устанавливается как атрибут экземпляра. В противном случае `user_agent` по умолчанию устанавливается как 'desktop'.

**Примеры**:

```python
from src.goog.google_search import GoogleHtmlParser

# Пример с десктопным user agent
html_content = "<html><body>...</body></html>"  #  <подставьте сюда HTML-код поисковой выдачи Google>
parser = GoogleHtmlParser(html_content)

# Пример с мобильным user agent
html_content = "<html><body>...</body></html>"  # <подставьте сюда HTML-код поисковой выдачи Google>
parser = GoogleHtmlParser(html_content, user_agent='mobile')
```

### `_clean(self, content: str) -> str`

**Назначение**: Очистка строки от лишних символов.

**Параметры**:
- `content` (str): Строка для очистки.

**Возвращает**:
- `str`: Очищенная строка.

**Как работает функция**:

- Функция очищает входную строку, удаляя начальные и конечные пробелы с помощью `content.strip()`.
- Затем она заменяет множественные пробелы одним пробелом с использованием `' '.join(content.split())`.
- Если входная строка `content` пуста, функция возвращает пустую строку.

**Примеры**:

```python
from src.goog.google_search import GoogleHtmlParser

html_content = "<html><body>...</body></html>"  #  <подставьте сюда HTML-код поисковой выдачи Google>
parser = GoogleHtmlParser(html_content)

# Пример очистки строки
dirty_string = "  Пример   строки   с лишними  пробелами  "
cleaned_string = parser._clean(dirty_string)
print(cleaned_string)  # Вывод: "Пример строки с лишними пробелами"

# Пример очистки пустой строки
empty_string = ""
cleaned_string = parser._clean(empty_string)
print(cleaned_string)  # Вывод: ""
```

### `_normalize_dict_key(self, content: str) -> str`

**Назначение**: Нормализация строки для использования в качестве ключа словаря.

**Параметры**:
- `content` (str): Строка для нормализации.

**Возвращает**:
- `str`: Нормализованная строка.

**Как работает функция**:

- Функция преобразует входную строку `content` для использования в качестве ключа словаря.
- Она заменяет пробелы на символы подчеркивания с помощью `replace(' ', '_')`.
- Удаляет двоеточия с помощью `replace(':', '')`.
- Приводит все символы к нижнему регистру с помощью `lower()`.
- Удаляет начальные и конечные символы подчеркивания с помощью `strip('_')`.
- Если строка `content` пуста, функция возвращает пустую строку.

**Примеры**:

```python
from src.goog.google_search import GoogleHtmlParser

html_content = "<html><body>...</body></html>"  # <подставьте сюда HTML-код поисковой выдачи Google>
parser = GoogleHtmlParser(html_content)

# Пример нормализации строки
input_string = "Пример строки: Для нормализации"
normalized_string = parser._normalize_dict_key(input_string)
print(normalized_string)  # Вывод: "пример_строки_для_нормализации"

# Пример нормализации пустой строки
empty_string = ""
normalized_string = parser._normalize_dict_key(empty_string)
print(normalized_string)  # Вывод: ""
```

### `_get_estimated_results(self) -> int`

**Назначение**: Получение количества результатов поиска.

**Возвращает**:
- `int`: Число результатов поиска.

**Как работает функция**:

- Функция извлекает количество найденных результатов для десктопной версии Google Search.
- Она использует XPath для поиска элемента с id "result-stats" и извлекает текст.
- Затем она разделяет текст на слова, берет второе слово (которое представляет собой количество результатов), удаляет запятые и преобразует его в целое число.
- Если элемент не найден, функция возвращает 0.

**Примеры**:

```python
from src.goog.google_search import GoogleHtmlParser

# Пример HTML-кода поисковой выдачи Google (desktop)
html_content = """
<html>
<body>
    <div id="result-stats">
        Результатов: примерно 12 345 678 (0,35 секунд)
    </div>
</body>
</html>
"""
parser = GoogleHtmlParser(html_content)
estimated_results = parser._get_estimated_results()
print(estimated_results)  # Вывод: 12345678
```

### `_get_organic(self) -> list`

**Назначение**: Получение органических результатов поиска.

**Возвращает**:
- `list`: Список словарей с органическими результатами.

**Как работает функция**:

- Функция извлекает органические результаты поиска без дополнительных элементов, таких как сниппеты.
- Она использует XPath для поиска всех div-элементов с классом "g", которые содержат органические результаты.
- Для каждого результата она извлекает URL, заголовок и сниппет.
- Если присутствуют "rich snippets", они также извлекаются.
- Результаты возвращаются в виде списка словарей, где каждый словарь содержит URL, заголовок, сниппет и "rich snippet".

**Примеры**:

```python
from src.goog.google_search import GoogleHtmlParser

# Пример HTML-кода поисковой выдачи Google (desktop)
html_content = """
<html>
<body>
    <div class="g">
        <div>
            <div>
                <div>
                    <div>
                        <a href="https://www.example.com">
                            <h3>Example Website</h3>
                        </a>
                        <div>
                            Description of the website.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
parser = GoogleHtmlParser(html_content)
organic_results = parser._get_organic()
print(organic_results)
# Вывод:
# [{'url': 'https://www.example.com', 'title': 'Example Website', 'snippet': 'Description of the website.', 'rich_snippet': ''}]
```

### `_get_featured_snippet(self) -> dict | None`

**Назначение**: Получение featured snippet.

**Возвращает**:
- `dict | None`: Словарь с заголовком и URL или None.

**Как работает функция**:

- Функция извлекает featured snippet, если он присутствует на странице.
- Она использует XPath для поиска элемента с классом, содержащим "kp-blk".
- Если элемент найден, она извлекает заголовок и URL из этого элемента.
- Результаты возвращаются в виде словаря, содержащего заголовок и URL. Если featured snippet отсутствует, возвращается None.

**Примеры**:

```python
from src.goog.google_search import GoogleHtmlParser

# Пример HTML-кода поисковой выдачи Google (desktop) с featured snippet
html_content = """
<html>
<body>
    <div class="kp-blk">
        <h3>Featured Snippet Title</h3>
        <a href="https://www.example.com/featured">
            More info
        </a>
    </div>
</body>
</html>
"""
parser = GoogleHtmlParser(html_content)
featured_snippet = parser._get_featured_snippet()
print(featured_snippet)
# Вывод:
# {'title': 'Featured Snippet Title', 'url': 'https://www.example.com/featured'}
```

### `_get_knowledge_card(self) -> dict | None`

**Назначение**: Получение карточки знаний.

**Возвращает**:
- `dict | None`: Словарь с данными карточки знаний или None.

**Как работает функция**:

- Функция извлекает карточку знаний, если она присутствует на странице.
- Она использует XPath для поиска элемента с классом, содержащим "kp-wholepage".
- Если элемент найден, она извлекает заголовок, подзаголовок и описание из этого элемента.
- Также извлекается дополнительная информация из элементов с атрибутом data-attrid, начинающимся с ":/".
- Результаты возвращаются в виде словаря, содержащего заголовок, подзаголовок, описание и дополнительную информацию. Если карточка знаний отсутствует, возвращается None.

**Примеры**:

```python
from src.goog.google_search import GoogleHtmlParser

# Пример HTML-кода поисковой выдачи Google (desktop) с карточкой знаний
html_content = """
<html>
<body>
    <div class="kp-wholepage">
        <h2><span>Knowledge Card Title</span></h2>
        <div data-attrid="subtitle">Subtitle of the card</div>
        <div class="kno-rdesc"><span>Description of the card</span></div>
        <div data-attrid=":/"><span>Key1</span><span>Value1</span></div>
        <div data-attrid=":/"><span>Key2</span><span>Value2</span></div>
    </div>
</body>
</html>
"""
parser = GoogleHtmlParser(html_content)
knowledge_card = parser._get_knowledge_card()
print(knowledge_card)
# Вывод:
# {
#     'title': 'Knowledge Card Title',
#     'subtitle': 'Subtitle of the card',
#     'description': 'Description of the card',
#     'more_info': [
#         {'key1': 'Value1'},
#         {'key2': 'Value2'}
#     ]
# }
```

### `_get_scrolling_sections(self) -> list`

**Назначение**: Получение данных из скроллируемых виджетов.

**Возвращает**:
- `list`: Список словарей с данными из виджетов.

**Как работает функция**:

- Функция извлекает данные из скроллируемых виджетов, таких как "топовые истории" или "твиты".
- Она использует XPath для поиска всех элементов g-section-with-header, которые содержат скроллируемые виджеты.
- Для каждого виджета она извлекает заголовок секции и данные из внутренних карточек (g-inner-card).
- Результаты возвращаются в виде списка словарей, где каждый словарь содержит заголовок секции и данные секции.

**Примеры**:

```python
from src.goog.google_search import GoogleHtmlParser

# Пример HTML-кода поисковой выдачи Google (desktop) с скроллируемыми секциями
html_content = """
<html>
<body>
    <g-section-with-header>
        <h3>Section Title</h3>
        <g-inner-card>
            <div role="heading">Card Title 1</div>
            <a href="https://www.example.com/card1"></a>
        </g-inner-card>
        <g-inner-card>
            <div role="heading">Card Title 2</div>
            <a href="https://www.example.com/card2"></a>
        </g-inner-card>
    </g-section-with-header>
</body>
</html>
"""
parser = GoogleHtmlParser(html_content)
scrolling_sections = parser._get_scrolling_sections()
print(scrolling_sections)
# Вывод:
# [
#     {
#         'section_title': 'Section Title',
#         'section_data': [
#             {'title': 'Card Title 1', 'url': 'https://www.example.com/card1'},
#             {'title': 'Card Title 2', 'url': 'https://www.example.com/card2'}
#         ]
#     }
# ]
```

### `get_data(self) -> dict`

**Назначение**: Получение итоговых данных с поисковой страницы.

**Возвращает**:
- `dict`: Словарь с данными поисковой страницы.

**Как работает функция**:

- Функция собирает итоговые данные с поисковой страницы, объединяя результаты из других методов класса.
- Она вызывает методы для извлечения количества результатов, featured snippet, карточки знаний, органических результатов и скроллируемых виджетов.
- Результаты возвращаются в виде словаря, содержащего все извлеченные данные.

**Примеры**:

```python
from src.goog.google_search import GoogleHtmlParser

# Пример HTML-кода поисковой выдачи Google (desktop)
html_content = """
<html>
<body>
    <div id="result-stats">
        Результатов: примерно 12 345 678 (0,35 секунд)
    </div>
    <div class="kp-blk">
        <h3>Featured Snippet Title</h3>
        <a href="https://www.example.com/featured">
            More info
        </a>
    </div>
    <div class="kp-wholepage">
        <h2><span>Knowledge Card Title</span></h2>
        <div data-attrid="subtitle">Subtitle of the card</div>
        <div class="kno-rdesc"><span>Description of the card</span></div>
    </div>
    <div class="g">
        <div>
            <div>
                <div>
                    <div>
                        <a href="https://www.example.com">
                            <h3>Example Website</h3>
                        </a>
                        <div>
                            Description of the website.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <g-section-with-header>
        <h3>Section Title</h3>
        <g-inner-card>
            <div role="heading">Card Title 1</div>
            <a href="https://www.example.com/card1"></a>
        </g-inner-card>
    </g-section-with-header>
</body>
</html>
"""
parser = GoogleHtmlParser(html_content)
data = parser.get_data()
print(data)
# Вывод (пример):
# {
#     'estimated_results': 12345678,
#     'featured_snippet': {'title': 'Featured Snippet Title', 'url': 'https://www.example.com/featured'},
#     'knowledge_card': {
#         'title': 'Knowledge Card Title',
#         'subtitle': 'Subtitle of the card',
#         'description': 'Description of the card',
#         'more_info': []
#     },
#     'organic_results': [
#         {'url': 'https://www.example.com', 'title': 'Example Website', 'snippet': 'Description of the website.', 'rich_snippet': ''}
#     ],
#     'scrolling_widgets': [
#         {
#             'section_title': 'Section Title',
#             'section_data': [
#                 {'title': 'Card Title 1', 'url': 'https://www.example.com/card1'}
#             ]
#         }
#     ]
# }