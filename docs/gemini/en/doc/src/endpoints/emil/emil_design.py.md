# Модуль `emil_design.py`

## Обзор

Модуль предназначен для управления и обработки изображений, а также для продвижения товаров в Facebook и PrestaShop. Он специфичен для магазина `emil-design.com`.

## Подробнее

Модуль предоставляет функциональность для:

- Описания изображений с использованием Gemini AI.
- Загрузки описаний товаров в PrestaShop.

## Классы

### `Config`

**Описание**: Класс конфигурации для `EmilDesign`. Он определяет параметры подключения к API PrestaShop, ключи API и список поставщиков.

**Атрибуты**:

- `ENDPOINT` (str): Конечная точка API, по умолчанию `'emil'`.
- `MODE` (str): Определяет конечную точку API. Возможные значения: `'dev'` (dev.emil_design.com prestashop 1.7), `'dev8'` (dev8.emil_design.com prestashop 8), `'prod'` (emil_design.com prestashop 1.7).
- `POST_FORMAT` (str): Формат POST-запросов, по умолчанию `'XML'`.
- `API_DOMAIN` (str): Домен API.
- `API_KEY` (str): Ключ API.
- `suppliers` (list): Список поставщиков, загружаемый из `emil.json`.

**Принцип работы**:
Класс `Config` отвечает за хранение и предоставление параметров конфигурации, необходимых для работы с API PrestaShop и другими сервисами. Он использует переменные окружения, если `USE_ENV` установлен в `True`, иначе загружает параметры из `gs.credentials.presta.client`. Если `MODE` невалиден, устанавливается значение по умолчанию `'dev'`.

### `EmilDesign`

**Описание**: Класс для управления изображениями и их продвижением через различные платформы.

**Атрибуты**:

- `gemini` (Optional[GoogleGenerativeAi]): Экземпляр класса `GoogleGenerativeAi` для работы с Gemini AI.
- `openai` (Optional[OpenAIModel]): Экземпляр класса `OpenAIModel` для работы с OpenAI.
- `base_path` (Path): Базовый путь к каталогу `emil` в структуре проекта.
- `config` (SimpleNamespace): Объект, содержащий конфигурацию, загруженную из файла `emil.json`.
- `data_path` (Path): Путь к каталогу для хранения данных, связанных с `emil`.
- `gemini_api` (str): Ключ API для Gemini AI.
- `presta_api` (str): Ключ API для PrestaShop.
- `presta_domain` (str): Домен PrestaShop.

**Принцип работы**:
Класс `EmilDesign` является основным классом для управления задачами, связанными с обработкой изображений, их описанием с использованием AI и загрузкой в PrestaShop, а также продвижением в Facebook. Он инициализирует необходимые API и пути к данным, а также предоставляет методы для выполнения этих задач.

## Методы класса `EmilDesign`

### `process_suppliers`

```python
    async def process_suppliers(self, supplier_prefix: Optional[str | List[str, str]] = '') -> bool:
        """
        Обрабатывает поставщиков на основе предоставленного префикса.
        Args:
            supplier_prefix (Optional[str | List[str, str]], optional): Префикс для поставщиков. По умолчанию ''.
        Returns:
            bool: True, если обработка выполнена успешно, False в противном случае.
        Raises:
            Exception: Если во время обработки поставщика возникает какая-либо ошибка.
        """
```

**Назначение**: Обрабатывает поставщиков на основе заданного префикса.

**Параметры**:

- `supplier_prefix` (Optional[str | List[str, str]], optional): Префикс или список префиксов поставщиков для обработки. По умолчанию пустая строка.

**Возвращает**:

- `bool`: `True`, если обработка завершена успешно, `False` в случае ошибки.

**Как работает**:

- Если `supplier_prefix` не указан, используются поставщики из `Config.suppliers`.
- Для каждого префикса ищется соответствующий граббер с помощью `get_graber_by_supplier_prefix`.
- Если граббер найден, запускается асинхронный процесс обработки сценариев (`graber.process_scenarios_async`) и обработки сценариев поставщика (`graber.process_supplier_scenarios_async`).
- В случае возникновения ошибки логируется сообщение и возвращается `False`.

**Примеры**:

```python
emil = EmilDesign()
asyncio.run(emil.process_suppliers('prefix1'))
asyncio.run(emil.process_suppliers(['prefix1', 'prefix2']))
asyncio.run(emil.process_suppliers())
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
            models (dict, optional): Конфигурация моделей. По умолчанию модели Gemini и OpenAI.

        Returns:
            None

        Raises:
            FileNotFoundError: Если файлы инструкций не найдены.
            Exception: Если во время обработки изображений возникает какая-либо ошибка.

        Example:
            >>> emil = EmilDesign()
            >>> emil.describe_images('he')
        """
```

**Назначение**: Описывает изображения, используя модели Gemini и OpenAI, на основе предоставленных инструкций и примеров.

**Параметры**:

- `lang` (str): Язык, на котором должно быть сгенерировано описание изображения.
- `models` (dict, optional): Словарь, содержащий конфигурации моделей Gemini и OpenAI. По умолчанию используются модели Gemini и OpenAI.

**Возвращает**:

- `None`

**Как работает**:

1. **Чтение инструкций**:
   - Функция извлекает системные инструкции и примеры для генерации описаний из файлов Markdown.
   - Формирует общий запрос, объединяя системные инструкции, категории мебели и примеры.
2. **Подготовка к обработке изображений**:
   - Определяет пути к файлам и каталогам, включая путь к файлу с описаниями изображений и папку с изображениями мебели.
   - Получает списки обработанных и необработанных изображений.
3. **Инициализация моделей**:
   - Инициализирует модели Gemini и/или OpenAI, если это указано в конфигурации.
4. **Обработка изображений**:
   - Перебирает список необработанных изображений.
   - Получает необработанные данные изображения.
   - Запрашивает у модели Gemini описание изображения.
   - Сохраняет описание изображения в файл JSON.
   - Обновляет список обработанных изображений.
   - Делает паузу между запросами.
5. **Обработка исключений**:
   - Обрабатывает исключения, такие как отсутствие файлов инструкций и общие ошибки при обработке изображений.

**Примеры**:

```python
emil = EmilDesign()
emil.describe_images(lang='he')
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
            Exception: Если во время продвижения в Facebook возникает какая-либо ошибка.
        """
```

**Назначение**: Публикует изображения и их описания в Facebook.

**Параметры**:

- Отсутствуют

**Возвращает**:

- `None`

**Как работает**:

1. **Инициализация драйвера**:
   - Инициализирует драйвер Chrome для управления браузером.
2. **Загрузка данных**:
   - Загружает сообщения из файла `images_descritions_he.json`.
3. **Публикация сообщений**:
   - Перебирает список сообщений.
   - Формирует сообщение для публикации, включая заголовок, описание и путь к изображению.
   - Вызывает функцию `post_message` для публикации сообщения в Facebook.
4. **Обработка исключений**:
   - Обрабатывает исключения, которые могут возникнуть во время продвижения в Facebook.

**Примеры**:

```python
emil = EmilDesign()
asyncio.run(emil.promote_to_facebook())
```

### `upload_described_products_to_prestashop`

```python
    def upload_described_products_to_prestashop(
        self, products_list: Optional[List[SimpleNamespace]] = None, id_lang: Optional[int | str] = 2, *args, **kwargs
    ) -> bool:
        """Загружает информацию о товарах в PrestaShop.

        Args:
            products_list (Optional[List[SimpleNamespace]], optional): Список информации о товарах. По умолчанию None.
            id_lang (Optional[str], optional): ID языка для баз данных PrestaShop.
            Обычно я назначаю языки в таком порядке 1 - en;2 - he; 3 - ru. 
            Важно проверить порядок якыков целевой базе данных.
            Вот образец кода для получения слопваря языков из конкретной базы данных
            >>import language
            >>lang_class = PrestaLanguage()
            >>print(lang_class.get_languages_schema())


        Returns:
            bool: True, если загрузка выполнена успешно, False в противном случае.

        Raises:
            FileNotFoundError: Если файл локалей не найден.
            Exception: Если во время загрузки в PrestaShop возникает какая-либо ошибка.
        """
```

**Назначение**: Загружает информацию о товарах в PrestaShop.

**Параметры**:

- `products_list` (Optional[List[SimpleNamespace]], optional): Список объектов `SimpleNamespace`, содержащих информацию о товарах. Если `None`, список формируется из JSON-файлов в каталоге данных.
- `id_lang` (Optional[int | str], optional): Идентификатор языка, используемый в PrestaShop. По умолчанию `2`.

**Возвращает**:

- `bool`: `True`, если загрузка выполнена успешно, `False` в случае ошибки.

**Как работает**:

1. **Получение списка товаров**:
   - Если `products_list` не предоставлен, функция получает список файлов JSON из каталога данных и загружает информацию о товарах из этих файлов.
2. **Инициализация PrestaProduct**:
   - Создает экземпляр класса `PrestaProduct` для взаимодействия с API PrestaShop.
3. **Определение идентификатора языка**:
   - Загружает файл локалей для определения идентификатора языка.
   - Преобразует строковый идентификатор языка (`en`, `he`, `ru`) в числовой.
4. **Загрузка товаров**:
   - Перебирает список товаров.
   - Создает экземпляр класса `ProductFields` для каждого товара.
   - Заполняет поля товара данными из объекта `product_ns`.
   - Добавляет товар в PrestaShop с помощью метода `p.add_new_product(f)`.
5. **Обработка исключений**:
   - Обрабатывает исключения, такие как отсутствие файла локалей и ошибки при загрузке в PrestaShop.

**Примеры**:

```python
emil = EmilDesign()
emil.upload_described_products_to_prestashop(id_lang=2)
```

```python
from types import SimpleNamespace

products = [
    SimpleNamespace(
        name='Товар 1',
        description='Описание товара 1',
        id_category_default=1,
        id_category_parent=2,
        local_image_path='/path/to/image1.jpg'
    ),
    SimpleNamespace(
        name='Товар 2',
        description='Описание товара 2',
        id_category_default=3,
        id_category_parent=4,
        local_image_path='/path/to/image2.jpg'
    )
]
emil = EmilDesign()
emil.upload_described_products_to_prestashop(products_list=products, id_lang=1)