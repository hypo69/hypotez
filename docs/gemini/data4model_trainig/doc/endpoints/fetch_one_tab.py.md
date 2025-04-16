# Модуль для разбора ссылок из OneTab

## Обзор

Модуль `src.endpoints.fetch_one_tab` предназначен для извлечения целевых URL-адресов из сервиса OneTab. Он использует библиотеки `BeautifulSoup` и `requests` для обработки HTML-контента и выполнения HTTP-запросов.

## Подробней

Этот модуль предоставляет функциональность для автоматического извлечения списка URL-адресов, цены и описания из OneTab, что может быть полезно для автоматизации сбора данных и анализа информации, хранящейся в OneTab.

## Функции

### `fetch_target_urls_onetab`

```python
def fetch_target_urls_onetab(one_tab_url: str) -> tuple[str, str, list[str]] | bool:
    """
    Функция паресит целевые URL из полученного OneTab.

    Args:
        one_tab_url (str): URL OneTab для парсинга.

    Returns:
        tuple[str, str, list[str]] | bool: Возвращает кортеж, содержащий цену (price), описание (description) и список URL-адресов, или `False`, `False`, `False` в случае ошибки.

    Raises:
        requests.exceptions.RequestException: Возникает при ошибках HTTP-запроса.

    """
```

**Назначение**: Извлекает целевые URL-адреса, цену и описание из указанной страницы OneTab.

**Параметры**:
- `one_tab_url` (str): URL страницы OneTab для парсинга.

**Возвращает**:
- `tuple[str, str, list[str]] | bool`: Кортеж, содержащий:
    - `price` (str): Цена, извлеченная из данных OneTab.
    - `description` (str): Описание, извлеченное из данных OneTab. Если описание отсутствует, возвращает текущую дату и время.
    - `urls` (list[str]): Список URL-адресов, извлеченных со страницы OneTab.
    В случае ошибки возвращает `False`, `False`, `False`.

**Вызывает исключения**:
- `requests.exceptions.RequestException`: Если возникает ошибка при выполнении HTTP-запроса.

**Как работает функция**:
1. Функция выполняет HTTP-запрос к указанному `one_tab_url` с таймаутом в 10 секунд.
2. Если запрос завершается с ошибкой (например, HTTP 404), функция логирует ошибку и возвращает `False`, `False`, `False`.
3. В случае успешного запроса функция использует `BeautifulSoup` для парсинга HTML-содержимого ответа.
4. Извлекает все URL-адреса из элементов `<a>` с классом `tabLink`.
5. Извлекает данные из элемента `<div>` с классом `tabGroupLabel`.
6. Если данные из `tabGroupLabel` отсутствуют, устанавливает цену в пустую строку, а описание в текущую дату и время.
7. Если данные присутствуют, разбивает их на части, предполагая, что первая часть — это цена, а остальное — описание. Если цена является числом, она преобразуется в целое число.
8. Функция возвращает извлеченные цену, описание и список URL-адресов.

**Примеры**:

Пример успешного извлечения данных:

```python
one_tab_url = "https://www.one-tab.com/..."
price, description, urls = fetch_target_urls_onetab(one_tab_url)
if price and description and urls:
    print(f"Цена: {price}, Описание: {description}")
    print(f"Количество URL: {len(urls)}")
```

Пример обработки ошибки запроса:

```python
one_tab_url = "https://www.one-tab.com/invalid_url"
price, description, urls = fetch_target_urls_onetab(one_tab_url)
if not price and not description and not urls:
    print("Не удалось извлечь данные из OneTab.")