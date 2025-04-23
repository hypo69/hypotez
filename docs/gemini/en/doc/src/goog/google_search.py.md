# Модуль `src.goog.google_search`

## Обзор

Модуль `src.goog.google_search` предназначен для парсинга HTML-кода, полученного из поисковой выдачи Google. Он позволяет извлекать различные данные, такие как органические результаты поиска, featured snippet, карточки знаний и другие элементы. Модуль содержит класс `GoogleHtmlParser`, который предоставляет методы для очистки, нормализации и извлечения данных из HTML-кода.

## Подробнее

Этот модуль используется для автоматизированного анализа результатов поиска Google. Он может быть полезен для SEO-специалистов, маркетологов и исследователей, которым необходимо собирать данные о поисковой выдаче в больших масштабах. Модуль поддерживает как десктопную, так и мобильную версии HTML Google Search.

## Классы

### `GoogleHtmlParser`

**Описание**:
Класс `GoogleHtmlParser` предназначен для парсинга HTML-кода, полученного из поисковой выдачи Google. Он преобразует HTML-код в словарь, содержащий различные элементы поисковой выдачи.

**Атрибуты**:
- `tree` (html.Element): Дерево документа, полученное с использованием `html.fromstring()`.
- `user_agent` (str): User agent, использованный для получения HTML Google Search. Может принимать значения `'mobile'` или `'desktop'`.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `GoogleHtmlParser`.
- `_clean`: Очищает строку от лишних символов.
- `_normalize_dict_key`: Нормализует строку для использования в качестве ключа словаря.
- `_get_estimated_results`: Получает количество результатов поиска.
- `_get_organic`: Получает органические результаты поиска.
- `_get_featured_snippet`: Получает featured snippet.
- `_get_knowledge_card`: Получает карточку знаний.
- `_get_scrolling_sections`: Получает данные из скроллируемых виджетов.
- `get_data`: Получает итоговые данные с поисковой страницы.

#### Принцип работы:
1. **Инициализация**: При создании экземпляра класса `GoogleHtmlParser` HTML-код преобразуется в дерево документа с использованием `html.fromstring()`. Также определяется user agent.
2. **Парсинг данных**: Методы, начинающиеся с `_get`, используются для извлечения различных элементов из дерева документа.
3. **Очистка и нормализация**: Методы `_clean` и `_normalize_dict_key` используются для очистки и нормализации извлеченных данных.
4. **Сбор данных**: Метод `get_data` собирает все извлеченные данные в один словарь и возвращает его.

### `__init__`

```python
def __init__(self, html_str: str, user_agent: str = 'desktop') -> None:
    """
    Инициализация парсера.

    Создает дерево документа из строки HTML.

    Args:
        html_str (str): HTML Google Search в виде строки.
        user_agent (str): User agent для получения HTML. Может быть 'mobile' или 'desktop'.

    Returns:
        None
    """
    self.tree = html.fromstring(html_str)
    if user_agent in ['mobile', 'desktop']:
        self.user_agent = user_agent
    else:
        self.user_agent = 'desktop'
```

**Описание**:
Инициализирует класс `GoogleHtmlParser`, преобразуя HTML в дерево документа и устанавливая user agent.

**Параметры**:
- `html_str` (str): HTML Google Search в виде строки.
- `user_agent` (str, optional): User agent для получения HTML. Может быть `'mobile'` или `'desktop'`. По умолчанию `'desktop'`.

**Пример**:
```python
parser = GoogleHtmlParser(html_str='<html>...</html>', user_agent='mobile')
```

### `_clean`

```python
def _clean(self, content: str) -> str:
    """
    Очистка строки от лишних символов.

    Очищает строку от пробелов и лишних символов.

    Args:
        content (str): Строка для очистки.

    Returns:
        str: Очищенная строка.
    """
    if content:
        content = content.strip()
        content = ' '.join(content.split())
        return content
    return ''
```

**Описание**:
Очищает строку от лишних пробелов и символов.

**Параметры**:
- `content` (str): Строка для очистки.

**Возвращает**:
- `str`: Очищенная строка.

**Пример**:
```python
cleaned_string = parser._clean(content='  Пример строки  ')
```

### `_normalize_dict_key`

```python
def _normalize_dict_key(self, content: str) -> str:
    """
    Нормализация строки для использования в качестве ключа словаря.

    Заменяет пробелы на подчеркивания, убирает двоеточия, приводит к нижнему регистру.

    Args:
        content (str): Строка для нормализации.

    Returns:
        str: Нормализованная строка.
    """
    content = str(content).replace(' ', '_').replace(':', '').lower().strip('_')
    return content
```

**Описание**:
Нормализует строку для использования в качестве ключа словаря. Заменяет пробелы на подчеркивания, убирает двоеточия и приводит к нижнему регистру.

**Параметры**:
- `content` (str): Строка для нормализации.

**Возвращает**:
- `str`: Нормализованная строка.

**Пример**:
```python
normalized_key = parser._normalize_dict_key(content='Пример строки: ')
```

### `_get_estimated_results`

```python
def _get_estimated_results(self) -> int:
    """
    Получение количества результатов поиска.

    Возвращает количество найденных результатов для десктопной версии Google Search.

    Returns:
        int: Число результатов поиска.
    """
    estimated_results = 0
    estimated_el = self.tree.xpath('//*[@id="result-stats"]/text()')
    if len(estimated_el) > 0:
        estimated_results = int(estimated_el[0].split()[1].replace(',', ''))
    return estimated_results
```

**Описание**:
Извлекает количество результатов поиска из HTML-кода (только для десктопной версии).

**Возвращает**:
- `int`: Число результатов поиска.

**Пример**:
```python
estimated_results = parser._get_estimated_results()
```

### `_get_organic`

```python
def _get_organic(self) -> list:
    """
    Получение органических результатов поиска.

    Возвращает список органических результатов без дополнительных фич (snippet, featured snippet и т.д.).

    Returns:
        list: Список словарей с органическими результатами.
    """
    organic = []
    for g in self.tree.xpath('//div[@class="g"]'):
        snippets = g.xpath('.//div/div/div[2]/div')
        snippet, rich_snippet = None, None
        if len(snippets) == 1:
            snippet = snippets[0].text_content()
        elif len(snippets) > 1:
            if snippets[1].xpath('.//g-review-stars'):
                rich_snippet = snippets[1].text_content()
                snippet = snippets[0].text_content()
            else:
                snippet = snippets[1].text_content()
                rich_snippet = snippets[0].text_content()

        res = {
            'url': self._clean(g.xpath('.//@href[1]')[0]),
            'title': self._clean(g.xpath('.//h3/text()')[0]),
            'snippet': self._clean(snippet),
            'rich_snippet': self._clean(rich_snippet),
        }
        organic.append(res)
    return organic
```

**Описание**:
Извлекает органические результаты поиска из HTML-кода.

**Возвращает**:
- `list`: Список словарей с органическими результатами (URL, заголовок, snippet, rich snippet).

**Пример**:
```python
organic_results = parser._get_organic()
```

### `_get_featured_snippet`

```python
def _get_featured_snippet(self) -> dict | None:
    """
    Получение featured snippet.

    Если существует, возвращает featured snippet с заголовком и URL.

    Returns:
        dict | None: Словарь с заголовком и URL или None.
    """
    fs = None
    snippet_el = self.tree.xpath('//div[contains(@class, "kp-blk")]')
    if snippet_el:
        snippet_el = snippet_el[0]
        heading = snippet_el.xpath('.//h3/text()')
        url = snippet_el.xpath('.//a/@href')
        if heading and url:
            fs = {'title': heading[0], 'url': url[-1]}
    return fs
```

**Описание**:
Извлекает featured snippet из HTML-кода.

**Возвращает**:
- `dict | None`: Словарь с заголовком и URL featured snippet, или `None`, если featured snippet отсутствует.

**Пример**:
```python
featured_snippet = parser._get_featured_snippet()
```

### `_get_knowledge_card`

```python
def _get_knowledge_card(self) -> dict | None:
    """
    Получение карточки знаний.

    Возвращает карточку знаний с заголовком, подзаголовком и описанием, если существует.

    Returns:
        dict | None: Словарь с данными карточки знаний или None.
    """
    kc_el = self.tree.xpath('//div[contains(@class, "kp-wholepage")]')
    if kc_el:
        kc_el = kc_el[0]
        more_info = []
        for el in kc_el.xpath('.//div[contains(@data-attrid, ":/")]'):
            el_parts = el.xpath('.//span')
            if len(el_parts) == 2:
                more_info.append({self._normalize_dict_key(el_parts[0].text_content()): el_parts[1].text_content()})
        return {
            'title': kc_el.xpath('.//h2/span')[0].text_content(),
            'subtitle': kc_el.xpath('.//div[contains(@data-attrid, "subtitle")]')[0].text_content(),
            'description': kc_el.xpath('.//div[@class="kno-rdesc"]/span')[0].text_content(),
            'more_info': more_info
        }
    return None
```

**Описание**:
Извлекает карточку знаний из HTML-кода.

**Возвращает**:
- `dict | None`: Словарь с данными карточки знаний (заголовок, подзаголовок, описание, дополнительная информация) или `None`, если карточка знаний отсутствует.

**Пример**:
```python
knowledge_card = parser._get_knowledge_card()
```

### `_get_scrolling_sections`

```python
def _get_scrolling_sections(self) -> list:
    """
    Получение данных из скроллируемых виджетов.

    Возвращает список данных из виджетов, например, топовые истории или твиты.

    Returns:
        list: Список словарей с данными из виджетов.
    """
    sections = self.tree.xpath('//g-section-with-header')
    data = []
    for section in sections:
        title = section.xpath('.//h3')[0].text_content()
        section_data = []
        for data_section in section.xpath('.//g-inner-card'):
            data_title = data_section.xpath('.//div[@role="heading"]/text()')[0]
            data_url = data_section.xpath('.//a/@href')[0]
            section_data.append({'title': self._clean(data_title), 'url': self._clean(data_url)})
        data.append({'section_title': title, 'section_data': section_data})
    return data
```

**Описание**:
Извлекает данные из скроллируемых виджетов (например, топовые истории или твиты) из HTML-кода.

**Возвращает**:
- `list`: Список словарей с данными из виджетов (заголовок секции, данные секции).

**Пример**:
```python
scrolling_sections = parser._get_scrolling_sections()
```

### `get_data`

```python
def get_data(self) -> dict:
    """
    Получение итоговых данных с поисковой страницы.

    Собирает данные с результатов поиска: органические результаты, карточка знаний и др.

    Returns:
        dict: Словарь с данными поисковой страницы.
    """
    data = {}
    if self.user_agent == 'desktop':
        data = {
            'estimated_results': self._get_estimated_results(),
            'featured_snippet': self._get_featured_snippet(),
            'knowledge_card': self._get_knowledge_card(),
            'organic_results': self._get_organic(),
            'scrolling_widgets': self._get_scrolling_sections()
        }
    return data
```

**Описание**:
Собирает все данные с поисковой страницы и возвращает их в виде словаря.

**Возвращает**:
- `dict`: Словарь с данными поисковой страницы (количество результатов, featured snippet, карточка знаний, органические результаты, скроллируемые виджеты).

**Пример**:
```python
search_data = parser.get_data()
```