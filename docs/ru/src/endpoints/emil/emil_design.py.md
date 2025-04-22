# Модуль `emil_design`

## Обзор

Модуль предназначен для управления и обработки изображений, а также для продвижения товаров в Facebook и PrestaShop для магазина `emil-design.com`.

## Подробнее

Модуль предоставляет функциональность для:

-   Генерации описаний изображений с использованием Gemini AI.
-   Загрузки описаний продуктов в PrestaShop.

## Классы

### `Config`

**Описание**: Класс конфигурации для `EmilDesign`.

**Атрибуты**:

-   `ENDPOINT` (str): Конечная точка API, по умолчанию `'emil'`.
-   `MODE` (str): Определяет конечную точку API, принимает значения: `'dev'`, `'dev8'`, `'prod'`. По умолчанию `'dev'`.
-   `POST_FORMAT` (str): Формат данных для отправки, по умолчанию `'XML'`.
-   `API_DOMAIN` (str): Домен API. Значение определяется в зависимости от `MODE` или переменных окружения.
-   `API_KEY` (str): Ключ API. Значение определяется в зависимости от `MODE` или переменных окружения.
-   `suppliers` (list): Список поставщиков, загружается из файла `emil.json`.

**Принцип работы**:

Класс `Config` предназначен для хранения и управления конфигурационными параметрами, необходимыми для работы с API PrestaShop и другими сервисами. Он определяет значения параметров в зависимости от выбранного режима (`MODE`) или использует переменные окружения, если они доступны.

### `EmilDesign`

**Описание**: Класс для проектирования и продвижения изображений через различные платформы.

**Атрибуты**:

-   `gemini` (Optional\[GoogleGenerativeAi]): Экземпляр класса `GoogleGenerativeAi` для работы с Gemini AI.
-   `openai` (Optional\[OpenAIModel]): Экземпляр класса `OpenAIModel` для работы с OpenAI.
-   `base_path` (Path): Базовый путь к каталогу модуля.
-   `config` (SimpleNamespace): Конфигурация, загруженная из файла `emil.json`.
-   `data_path` (Path): Путь к каталогу с данными модуля.
-   `gemini_api` (str): Ключ API для Gemini.
-   `presta_api` (str): Ключ API для PrestaShop.
-   `presta_domain` (str): Домен PrestaShop.

**Методы**:

-   `process_suppliers(supplier_prefix: Optional[str | List[str, str]] = '') -> bool`
-   `describe_images(lang: str, models: dict = {'gemini': {'model_name': 'gemini-1.5-flash'}, 'openai': {'model_name': 'gpt-4o-mini', 'assistant_id': 'asst_uDr5aVY3qRByRwt5qFiMDk43'}}) -> None`
-   `promote_to_facebook() -> None`
-   `upload_described_products_to_prestashop(products_list: Optional[List[SimpleNamespace]] = None, id_lang: Optional[int | str] = 2, *args, **kwards) -> bool`

## Методы класса

### `process_suppliers`

```python
async def process_suppliers(self, supplier_prefix: Optional[str | List[str, str]] = '') -> bool:
    """
    Обрабатывает поставщиков на основе предоставленного префикса.

    Args:
        supplier_prefix (Optional[str | List[str, str]], optional): Префикс для поставщиков. По умолчанию ''.

    Returns:
        bool: `True`, если обработка выполнена успешно, `False` в противном случае.

    Raises:
        Exception: Если возникает ошибка во время обработки поставщика.

    Как работает функция:
    - Проверяет, передан ли префикс поставщика. Если да, то преобразует его в список, если это строка.
    - Если префикс не передан, то использует список поставщиков из конфигурации.
    - Для каждого префикса получает граббер (graber) с помощью функции `get_graber_by_supplier_prefix`.
    - Если граббер не найден, выводит предупреждение в лог и переходит к следующему префиксу.
    - Вызывает асинхронные методы граббера `process_scenarios_async` и `process_supplier_scenarios_async` для обработки сценариев.
    - Логирует информацию об обработке поставщика с указанным префиксом.

    Примеры:
        >>> emil = EmilDesign()
        >>> asyncio.run(emil.process_suppliers('prefix1'))
        True
        >>> asyncio.run(emil.process_suppliers(['prefix1', 'prefix2']))
        True
    """
    ...
```

### `describe_images`

```python
def describe_images(
    self,
    lang: str,
    models: dict = {
        'gemini': {'model_name': 'gemini-1.5-flash'},
        'openai': {'model_name': 'gpt-4o-mini', 'assistant_id': 'asst_uDr5aVY3qRByRwt5qFiMDk43'},
    },
) -> None:
    """Описывает изображения на основе предоставленной инструкции и примеров.

    Args:
        lang (str): Язык для описания.
        models (dict, optional): Конфигурация моделей. По умолчанию использует модели Gemini и OpenAI.

    Returns:
        None

    Raises:
        FileNotFoundError: Если файлы инструкций не найдены.
        Exception: Если возникает ошибка во время обработки изображения.

    Как работает функция:
    - Читает системные инструкции и подсказки для указанного языка из файлов.
    - Формирует общую системную инструкцию, объединяя инструкции и категории мебели.
    - Определяет пути к файлам вывода JSON и списку описанных изображений.
    - Считывает список уже описанных изображений из файла.
    - Получает список файлов изображений для обработки из указанного каталога.
    - Фильтрует список изображений, исключая те, которые уже были описаны.
    - Инициализирует модели Gemini и/или OpenAI в зависимости от конфигурации.
    - Для каждого изображения:
        - Считывает необработанные данные изображения.
        - Получает описание изображения с помощью выбранной модели (Gemini или OpenAI).
        - Сохраняет описание в JSON-файл.
        - Добавляет путь к изображению в список описанных изображений и сохраняет его в файл.
        - Делает задержку в 15 секунд между запросами.

    Примеры:
        >>> emil = EmilDesign()
        >>> emil.describe_images('he')
    """
    ...
```

### `promote_to_facebook`

```python
async def promote_to_facebook(self) -> None:
    """Продвигает изображения и их описания в Facebook.

    Args:
        None

    Returns:
        None

    Raises:
        Exception: Если возникает ошибка во время продвижения в Facebook.

    Как работает функция:
    - Инициализирует драйвер Chrome для управления браузером.
    - Открывает указанный URL группы Facebook.
    - Загружает описания изображений из JSON-файла.
    - Для каждого сообщения (описания):
        - Формирует объект SimpleNamespace с данными сообщения, включая заголовок, описание и путь к изображению.
        - Вызывает функцию `post_message` для публикации сообщения в Facebook.

    Примеры:
        >>> emil = EmilDesign()
        >>> asyncio.run(emil.promote_to_facebook())
    """
    ...
```

### `upload_described_products_to_prestashop`

```python
def upload_described_products_to_prestashop(
    self, products_list: Optional[List[SimpleNamespace]] = None, id_lang: Optional[int | str] = 2, *args, **kwards
) -> bool:
    """Загружает информацию о продуктах в PrestaShop.

    Args:
        products_list (Optional[List[SimpleNamespace]], optional): Список информации о продуктах. По умолчанию `None`.
        id_lang (Optional[int | str], optional): ID языка для базы данных PrestaShop.
            Обычно назначается в таком порядке: 1 - en, 2 - he, 3 - ru.
            Важно проверить порядок языков в целевой базе данных.
            Вот образец кода для получения словаря языков из конкретной базы данных:
            `import language`
            `lang_class = PrestaLanguage()`
            `print(lang_class.get_languages_schema())`
            По умолчанию 2.
        *args: Произвольные позиционные аргументы.
        **kwards: Произвольные именованные аргументы.

    Returns:
        bool: `True`, если загрузка выполнена успешно, `False` в противном случае.

    Raises:
        FileNotFoundError: Если файл локалей не найден.
        Exception: Если возникает ошибка во время загрузки в PrestaShop.

    Как работает функция:
    - Получает список файлов с информацией о продуктах из указанного каталога.
    - Загружает информацию о продуктах из JSON-файлов.
    - Создает экземпляр класса `PrestaProduct` для взаимодействия с API PrestaShop.
    - Загружает локали из файла `locales.json`.
    - Для каждого продукта:
        - Создает экземпляр класса `ProductFields` и заполняет его данными из информации о продукте.
        - Добавляет новый продукт в PrestaShop с помощью метода `add_new_product` класса `PrestaProduct`.

    Примеры:
        >>> emil = EmilDesign()
        >>> emil.upload_described_products_to_prestashop(id_lang=2)
        True
    """
    ...
```

## Параметры класса

-   `ENDPOINT` (str): Конечная точка API.
-   `MODE` (str): Определяет конечную точку API.
-   `POST_FORMAT` (str): Формат данных для отправки.
-   `API_DOMAIN` (str): Домен API.
-   `API_KEY` (str): Ключ API.
-   `products_list` (Optional[List[SimpleNamespace]], optional): Список информации о товарах. По умолчанию `None`.
-   `id_lang` (Optional[str], optional): Языковой идентификатор для баз данных PrestaShop.

```