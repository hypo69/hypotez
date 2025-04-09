# Модуль `emil_design`

## Обзор

Модуль `emil_design.py` предназначен для управления и обработки изображений, а также для продвижения контента на платформах Facebook и PrestaShop. Он используется в контексте магазина `emil-design.com` для автоматизации задач, связанных с описанием товаров и их публикацией.

## Подробнее

Этот модуль предоставляет функциональность для:

*   Генерации описаний изображений с использованием AI (Gemini и OpenAI).
*   Загрузки сгенерированных описаний продуктов в PrestaShop.
*   Продвижения продуктов в Facebook.

Основная цель модуля - автоматизировать рутинные задачи, связанные с наполнением контента и продвижением товаров в интернет-магазине `emil-design.com`.

## Классы

### `Config`

**Описание**: Класс `Config` предназначен для хранения конфигурационных параметров, необходимых для работы с API PrestaShop и другими сервисами. Он определяет настройки для различных режимов работы (dev, dev8, prod) и предоставляет доступ к API ключам и доменам.

**Принцип работы**:

Класс `Config` содержит статические атрибуты, которые определяют параметры подключения к API PrestaShop. В зависимости от значения атрибута `MODE`, класс выбирает соответствующие значения для `API_DOMAIN` и `API_KEY`. Если используется переменная окружения `USE_ENV`, класс загружает значения из переменных окружения, в противном случае использует значения, хранящиеся в `gs.credentials`.

```ascii
    USE_ENV == True?  -->  load_dotenv() --> API_DOMAIN, API_KEY from env
    |
    NO
    |
    MODE --> 'dev'/'dev8'/'prod'? --> API_DOMAIN, API_KEY from gs.credentials
```

### `EmilDesign`

**Описание**: Класс `EmilDesign` предназначен для управления процессом описания изображений, их загрузки в PrestaShop и продвижения в Facebook. Он содержит методы для взаимодействия с AI-моделями (Gemini и OpenAI), API PrestaShop и драйвером веб-браузера.

**Принцип работы**:

Класс `EmilDesign` инициализируется с конфигурацией, загруженной из JSON-файла. Он предоставляет методы для описания изображений с использованием Gemini или OpenAI, загрузки информации о продуктах в PrestaShop и продвижения контента в Facebook. Класс использует другие модули и классы, такие как `GoogleGenerativeAI`, `OpenAIModel`, `PrestaProduct` и `Driver`, для выполнения конкретных задач.

**Аттрибуты**:

*   `gemini` (Optional\[GoogleGenerativeAI]): Экземпляр класса `GoogleGenerativeAI` для работы с моделью Gemini.
*   `openai` (Optional\[OpenAIModel]): Экземпляр класса `OpenAIModel` для работы с моделью OpenAI.
*   `base_path` (Path): Путь к базовой директории модуля (`gs.path.endpoints / Config.ENDPOINT`).
*   `config` (SimpleNamespace): Конфигурация, загруженная из JSON-файла (`emil.json`).
*   `data_path` (Path): Путь к директории с данными (`getattr(gs.path, config.storage, 'external_storage') / Config.ENDPOINT`).
*   `gemini_api` (str): API ключ для Gemini.
*   `presta_api` (str): API ключ для PrestaShop.
*   `presta_domain` (str): Доменное имя PrestaShop.

**Методы**:

*   `describe_images(lang: str, models: dict = {'gemini': {'model_name': 'gemini-1.5-flash'}, 'openai': {'model_name': 'gpt-4o-mini', 'assistant_id': 'asst_uDr5aVY3qRByRwt5qFiMDk43'}})`: Описывает изображения на основе инструкций и примеров с использованием моделей Gemini и OpenAI.
*   `promote_to_facebook()`: Продвигает изображения и их описания в Facebook.
*   `upload_described_products_to_prestashop(products_list: Optional[List[SimpleNamespace]] = None, id_lang: Optional[int | str] = 2, *args, **kwards)`: Загружает информацию о продуктах в PrestaShop.

## Функции

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
    """Описывает изображения на основе предоставленных инструкций и примеров.

    Args:
        lang (str): Язык для описания.
        models (dict, optional): Конфигурация моделей. По умолчанию используются модели Gemini и OpenAI.

    Returns:
        None

    Raises:
        FileNotFoundError: Если файлы инструкций не найдены.
        Exception: Если возникает ошибка во время обработки изображений.
    """
```

**Назначение**: Описывает изображения, используя модели Gemini и OpenAI, на основе предоставленных инструкций и примеров.

**Параметры**:

*   `lang` (str): Язык, на котором будет сгенерировано описание изображения.
*   `models` (dict, optional): Словарь с конфигурациями моделей. По умолчанию использует Gemini и OpenAI.

**Возвращает**:

*   `None`

**Вызывает исключения**:

*   `FileNotFoundError`: Возникает, если не найдены файлы с инструкциями.
*   `Exception`: Возникает при любых других ошибках в процессе обработки изображений.

**Как работает функция**:

1.  **Загрузка инструкций**: Функция пытается прочитать файлы инструкций (`system_instruction.{lang}.md` и `hand_made_furniture.{lang}.md`) и файл категорий (`main_categories_furniture.json`) из директории `instructions` и `categories` соответственно.
2.  **Подготовка данных**: Подготавливает список изображений для обработки, исключая те, которые уже были обработаны и записаны в файл `described_images.txt`.
3.  **Использование AI моделей**: В зависимости от флагов `use_openai` и `use_gemini`, функция использует либо OpenAI, либо Gemini для генерации описаний изображений.
4.  **Генерация описаний**: Для каждого изображения функция вызывает метод `describe_image` у соответствующей AI-модели, передавая данные изображения и промпт.
5.  **Сохранение результатов**: Результаты сохраняются в JSON-файл с именем изображения, а также добавляются в список обработанных изображений.

```ascii
    Загрузка инструкций и категорий
    |
    Подготовка списка изображений для обработки
    |
    Выбор AI модели (Gemini или OpenAI)
    |
    Для каждого изображения:
        |
        Получение необработанных данных изображения
        |
        Запрос к AI модели на описание изображения
        |
        Если получен ответ:
            |
            Сохранение описания в JSON файл
            |
            Добавление изображения в список обработанных
        |
        Задержка
    |
    Сохранение списка обработанных изображений
```

**Примеры**:

```python
emil = EmilDesign()
emil.describe_images('he')
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
    """
```

**Назначение**: Продвигает изображения и сгенерированные описания в Facebook.

**Параметры**:

*   `None`

**Возвращает**:

*   `None`

**Вызывает исключения**:

*   `Exception`: Возникает при любых ошибках, связанных с продвижением в Facebook.

**Как работает функция**:

1.  **Инициализация драйвера**: Создает экземпляр драйвера Chrome и открывает страницу Facebook.
2.  **Загрузка сообщений**: Загружает JSON-файл с описаниями изображений.
3.  **Публикация**: Для каждого сообщения создает объект `SimpleNamespace` с данными для публикации и вызывает функцию `post_message` для отправки сообщения в Facebook.

```ascii
    Инициализация драйвера Chrome и открытие страницы Facebook
    |
    Загрузка сообщений из JSON файла
    |
    Для каждого сообщения:
        |
        Создание объекта SimpleNamespace с данными для публикации
        |
        Вызов функции post_message для отправки сообщения в Facebook
```

**Примеры**:

```python
emil = EmilDesign()
asyncio.run(emil.promote_to_facebook())
```

### `upload_described_products_to_prestashop`

```python
def upload_described_products_to_prestashop(
    self, products_list: Optional[List[SimpleNamespace]] = None, id_lang: Optional[int | str] = 2, *args, **kwards
) -> bool:
    """Загружает информацию о продуктах в PrestaShop.

    Args:
        products_list (Optional[List[SimpleNamespace]], optional): Список информации о продуктах. По умолчанию None.
        id_lang (Optional[str], optional): ID языка для базы данных PrestaShop.
        Обычно я назначаю языки в таком порядке 1 - en;2 - he; 3 - ru.
        Важно проверить порядок якыков целевой базе данных.
        Вот образец кода для получения слопваря языков из конкретной базы данных
        >>import language
        >>lang_class = PrestaLanguage()
        >>print(lang_class.get_languages_schema())

    Returns:
        bool: True, если загрузка прошла успешно, False в противном случае.

    Raises:
        FileNotFoundError: Если файл locales не найден.
        Exception: Если возникает ошибка во время загрузки в PrestaShop.
    """
```

**Назначение**: Загружает информацию о продуктах, включая названия, описания и изображения, в PrestaShop.

**Параметры**:

*   `products_list` (Optional\[List\[SimpleNamespace]], optional): Список объектов `SimpleNamespace`, содержащих информацию о продуктах. Если не указан, функция загружает данные из JSON-файлов в директории `data_path`. По умолчанию `None`.
*   `id_lang` (Optional\[int | str], optional): ID языка, на котором будет загружена информация о продукте. Значение по умолчанию: `2`. Обычно `1` - английский, `2` - иврит, `3` - русский.
*   `*args`: Произвольные позиционные аргументы.
*   `**kwards`: Произвольные именованные аргументы.

**Возвращает**:

*   `bool`: `True`, если загрузка прошла успешно, `False` в противном случае.

**Вызывает исключения**:

*   `FileNotFoundError`: Возникает, если файл `locales.json` не найден.
*   `Exception`: Возникает при любых других ошибках в процессе загрузки данных в PrestaShop.

**Как работает функция**:

1.  **Подготовка данных**: Если `products_list` не указан, функция загружает список JSON-файлов из директории `self.data_path` и преобразует их в список объектов `SimpleNamespace`.
2.  **Инициализация PrestaProduct**: Создает экземпляр класса `PrestaProduct` для взаимодействия с API PrestaShop.
3.  **Определение языка**: Определяет ID языка для загрузки данных. Если `id_lang` является строкой (`'en'`, `'he'`, `'ru'`), функция преобразует его в соответствующий числовой ID из файла `locales.json`.
4.  **Загрузка продуктов**: Для каждого продукта из списка создает экземпляр класса `ProductFields`, заполняет его данными из `product_ns` и вызывает метод `add_new_product` у экземпляра `PrestaProduct` для загрузки продукта в PrestaShop.

```ascii
    products_list is None?
    |
    YES --> Загрузка JSON-файлов из data_path и преобразование в SimpleNamespace
    |
    Инициализация PrestaProduct
    |
    Определение ID языка (id_lang)
    |
    Для каждого product_ns в products_list:
        |
        Создание ProductFields и заполнение данными из product_ns
        |
        Вызов p.add_new_product(f)
    |
    Возврат True
```

**Примеры**:

```python
emil = EmilDesign()
emil.upload_described_products_to_prestashop(id_lang=2)