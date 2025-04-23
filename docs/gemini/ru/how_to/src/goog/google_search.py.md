### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код представляет собой класс `GoogleHtmlParser`, предназначенный для парсинга HTML-кода, полученного из поисковой выдачи Google. Он позволяет извлекать различные элементы, такие как органические результаты поиска, featured snippet, карточку знаний и данные из скроллируемых виджетов.

Шаги выполнения
-------------------------
1. **Инициализация класса `GoogleHtmlParser`**:
   - Создается экземпляр класса `GoogleHtmlParser`, которому передается HTML-код страницы поисковой выдачи Google и тип пользовательского агента (desktop или mobile).
   - Функция `__init__` инициализирует парсер, создавая дерево документа из HTML-строки с использованием `html.fromstring` и устанавливая `user_agent`.

2. **Очистка и нормализация данных**:
   - Используются методы `_clean` и `_normalize_dict_key` для очистки и нормализации строк, извлеченных из HTML.
   - `_clean` удаляет лишние пробелы и символы из строки.
   - `_normalize_dict_key` преобразует строку для использования в качестве ключа словаря, заменяя пробелы на подчеркивания, удаляя двоеточия и приводя к нижнему регистру.

3. **Извлечение данных**:
   - Методы `_get_estimated_results`, `_get_organic`, `_get_featured_snippet`, `_get_knowledge_card` и `_get_scrolling_sections` используются для извлечения различных частей поисковой выдачи.
   - `_get_estimated_results` извлекает количество результатов поиска.
   - `_get_organic` извлекает список органических результатов поиска.
   - `_get_featured_snippet` извлекает featured snippet (если он есть).
   - `_get_knowledge_card` извлекает карточку знаний (если она есть).
   - `_get_scrolling_sections` извлекает данные из скроллируемых виджетов (например, топовые истории или твиты).

4. **Сбор итоговых данных**:
   - Метод `get_data` собирает все извлеченные данные и возвращает их в виде словаря.
   - В зависимости от типа пользовательского агента (`desktop` или `mobile`) собираются разные наборы данных.

Пример использования
-------------------------

```python
from src.goog.google_search import GoogleHtmlParser

# Пример HTML-кода страницы поисковой выдачи Google (desktop версия)
html_str = """
<div id="result-stats">
    пример результата поиска
    Результатов: примерно 1 230 000 (0,37 сек.)
</div>
<div class="g">
    <a href="https://example.com">
        <h3>Пример заголовка</h3>
    </a>
    <div>
        <div>
            <div>
                <div>Пример сниппета</div>
            </div>
        </div>
    </div>
</div>
<div class="kp-blk">
    <div>
        <h3>Пример featured snippet</h3>
    </div>
    <a href="https://example.com/snippet">Ссылка на snippet</a>
</div>
<div class="kp-wholepage">
    <h2><span>Пример карточки знаний</span></h2>
    <div data-attrid="subtitle">Пример подзаголовка</div>
    <div class="kno-rdesc"><span>Пример описания</span></div>
    <div data-attrid="пример:/">
        <span>Пример ключа</span>
        <span>Пример значения</span>
    </div>
</div>
<g-section-with-header>
    <h3>Пример заголовка секции</h3>
    <g-inner-card>
        <div role="heading">Пример заголовка данных</div>
        <a href="https://example.com/data"></a>
    </g-inner-card>
</g-section-with-header>
"""

# Создание экземпляра класса GoogleHtmlParser
parser = GoogleHtmlParser(html_str, user_agent='desktop')

# Получение данных
data = parser.get_data()

# Вывод полученных данных
print(data)
#  {
#     'estimated_results': 1230000,
#     'featured_snippet': {'title': 'Пример featured snippet', 'url': 'https://example.com/snippet'},
#     'knowledge_card': {
#         'title': 'Пример карточки знаний',
#         'subtitle': 'Пример подзаголовка',
#         'description': 'Пример описания',
#         'more_info': [{'пример_ключа': 'Пример значения'}]
#     },
#     'organic_results': [{'url': 'https://example.com', 'title': 'Пример заголовка', 'snippet': 'Пример сниппета', 'rich_snippet': None}],
#     'scrolling_widgets': [{'section_title': 'Пример заголовка секции', 'section_data': [{'title': None, 'url': 'https://example.com/data'}]}]
# }