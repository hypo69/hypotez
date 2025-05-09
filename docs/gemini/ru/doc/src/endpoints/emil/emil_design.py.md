# Модуль `src.endpoints.emil.emil_design`

## Обзор

Модуль предназначен для управления и обработки изображений, а также продвижения в Facebook и PrestaShop. Относится к магазину `emil-design.com`.

## Подробнее

Данный модуль предоставляет функционал для работы с изображениями, описаниями продуктов и их загрузкой в PrestaShop. 
Он использует Google Gemini AI для описания изображений и модели OpenAI для генерации текстов. 
Модуль также включает в себя функции для публикации изображений и их описаний в Facebook.

**Ключевые особенности:**

- **Описание изображений:**  Модуль использует Google Gemini AI для генерации описаний изображений. 
- **Загрузка в PrestaShop:** После описания изображения, модуль может загружать их в PrestaShop.
- **Продвижение в Facebook:** Модуль может публиковать изображения и их описания в Facebook-группы.

## Классы

### `Config`

**Описание**:  Класс конфигурации для `EmilDesign`. Содержит параметры для различных сервисов, включая API-ключи, адреса доменных имен, а также настройки языка и формата.

**Атрибуты**:

- **`ENDPOINT` (str):** Конечная точка API (например, `emil`).
- **`MODE` (str):** Режим работы (например, `dev`, `dev8`, `prod`). Определяет конечную точку API (например, `dev.emil_design.com` - `dev`, `dev8.emil_design.com` - `dev8`, `emil_design.com` - `prod`).
- **`POST_FORMAT` (str):** Формат для отправки запросов (например, `XML`).
- **`API_DOMAIN` (str):** Доменное имя API.
- **`API_KEY` (str):** Ключ API для доступа к PrestaShop.
- **`suppliers` (list):** Список поставщиков.
- **`gemini_api` (str):** Ключ API для Google Gemini AI.
- **`presta_api` (str):** Ключ API для PrestaShop.
- **`presta_domain` (str):** Доменное имя PrestaShop.


### `EmilDesign`

**Описание**: Класс `EmilDesign` используется для работы с изображениями, описаниями продуктов и их загрузкой в PrestaShop. 
Он использует Google Gemini AI для описания изображений и модели OpenAI для генерации текстов. 
Модуль также включает в себя функции для публикации изображений и их описаний в Facebook.

**Атрибуты**:

- **`gemini` (Optional[GoogleGenerativeAi]):** Объект GoogleGenerativeAi для взаимодействия с Gemini AI.
- **`openai` (Optional[OpenAIModel]):** Объект OpenAIModel для взаимодействия с моделями OpenAI.
- **`base_path` (Path):** Путь к корневой папке модуля.
- **`config` (SimpleNamespace):**  Конфигурация модуля, полученная из файла `emil.json`.
- **`data_path` (Path):** Путь к папке с данными.
- **`gemini_api` (str):** Ключ API для Google Gemini AI.
- **`presta_api` (str):** Ключ API для PrestaShop.
- **`presta_domain` (str):** Доменное имя PrestaShop.


## Методы класса

### `process_suppliers`

```python
    async def process_suppliers(self, supplier_prefix: Optional[str | List[str, str]] = '') -> bool:
        """
        Обрабатывает поставщиков на основе предоставленного префикса.
        Args:
            supplier_prefix (Optional[str | List[str, str]], optional): Префикс для поставщиков. По умолчанию ''.
        Returns:
            bool: True, если обработка прошла успешно, False в противном случае.
        Raises:
            Exception: Если во время обработки поставщиков возникла ошибка.
        """
```
- **Назначение**: Обрабатывает поставщиков на основе предоставленного префикса. 
- **Параметры**:
    - `supplier_prefix` (Optional[str | List[str, str]], optional): Префикс для поставщиков. По умолчанию ''.
- **Возвращает**:
    - `bool`: True, если обработка прошла успешно, False в противном случае.
- **Вызывает исключения**:
    - `Exception`: Если во время обработки поставщиков возникла ошибка.
- **Как работает функция**:
    - Функция `process_suppliers` получает список поставщиков из конфигурационного файла. 
    - Затем она итерирует по списку поставщиков и для каждого из них получает соответствующий грабер (`graber`) из модуля `src.suppliers.get_graber_by_supplier`. 
    - После получения грабера, функция запускает асинхронные функции `process_scenarios_async` и `process_supplier_scenarios_async` для обработки сценариев и обработки поставщиков. 
    - В случае ошибки функция записывает сообщение об ошибке в лог и возвращает `False`.
- **Примеры**:
    ```python
    # Обработка всех поставщиков из конфигурационного файла
    emil = EmilDesign()
    asyncio.run(emil.process_suppliers())

    # Обработка поставщиков с префиксом 'clothes'
    emil = EmilDesign()
    asyncio.run(emil.process_suppliers(supplier_prefix='clothes'))
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
        """
        Описывает изображения на основе предоставленной инструкции и примеров.
        Args:
            lang (str): Язык для описания.
            models (dict, optional): Конфигурация моделей. По умолчанию - Gemini и OpenAI модели.
        Returns:
            None
        Raises:
            FileNotFoundError: Если файлы инструкций не найдены.
            Exception: Если во время обработки изображения возникла ошибка.
        Example:
            >>> emil = EmilDesign()
            >>> emil.describe_images('he')
        """
```
- **Назначение**: Описывает изображения на основе предоставленной инструкции и примеров. 
- **Параметры**:
    - `lang` (str): Язык для описания.
    - `models` (dict, optional): Конфигурация моделей. По умолчанию - Gemini и OpenAI модели.
- **Возвращает**:
    - `None`
- **Вызывает исключения**:
    - `FileNotFoundError`: Если файлы инструкций не найдены.
    - `Exception`: Если во время обработки изображения возникла ошибка.
- **Как работает функция**:
    - Функция `describe_images` считывает инструкции для Google Gemini AI из файла `system_instruction.{lang}.md`. 
    - Она также считывает примеры описания изображений из файла `hand_made_furniture.{lang}.md`.
    - Далее функция получает список изображений из папки `images/furniture_images` и итерирует по каждому из них.
    - Для каждого изображения функция получает описание с помощью модели Gemini. 
    - Полученное описание сохраняется в файл JSON с именем, соответствующим имени изображения.
- **Примеры**:
    ```python
    emil = EmilDesign()
    emil.describe_images(lang='he')
    ```

### `promote_to_facebook`

```python
    async def promote_to_facebook(self) -> None:
        """
        Продвигает изображения и их описания в Facebook.
        Args:
            None
        Returns:
            None
        Raises:
            Exception: Если во время продвижения в Facebook возникла ошибка.
        """
```
- **Назначение**: Продвигает изображения и их описания в Facebook. 
- **Параметры**:
    - `None`
- **Возвращает**:
    - `None`
- **Вызывает исключения**:
    - `Exception`: Если во время продвижения в Facebook возникла ошибка.
- **Как работает функция**:
    - Функция `promote_to_facebook` открывает страницу Facebook-группы с помощью веб-драйвера (Chrome).
    - Затем она итерирует по списку изображений и их описаний, полученных из файла `images_descritions_he.json`.
    - Для каждого изображения функция создает сообщение с описанием, которое будет опубликовано в Facebook. 
    - В случае ошибки функция записывает сообщение об ошибке в лог.
- **Примеры**:
    ```python
    emil = EmilDesign()
    asyncio.run(emil.promote_to_facebook())
    ```

### `upload_described_products_to_prestashop`

```python
    def upload_described_products_to_prestashop(
        self, products_list: Optional[List[SimpleNamespace]] = None, id_lang: Optional[int | str] = 2, *args, **kwargs
    ) -> bool:
        """
        Загружает информацию о продуктах в PrestaShop.
        Args:
            products_list (Optional[List[SimpleNamespace]], optional): Список информации о продуктах. По умолчанию None.
            id_lang (Optional[str], optional): Идентификатор языка для баз данных PrestaShop.
            Обычно я назначаю языки в таком порядке 1 - en;2 - he; 3 - ru. 
            Важно проверить порядок якыков целевой базе данных.
            Вот образец кода для получения слопваря языков из конкретной базы данных
            >>import language
            >>lang_class = PrestaLanguage()
            >>print(lang_class.get_languages_schema())
        Returns:
            bool: True, если загрузка прошла успешно, False в противном случае.
        Raises:
            FileNotFoundError: Если файл локалей не найден.
            Exception: Если во время загрузки в PrestaShop возникла ошибка.
        """
```
- **Назначение**: Загружает информацию о продуктах в PrestaShop. 
- **Параметры**:
    - `products_list` (Optional[List[SimpleNamespace]], optional): Список информации о продуктах. По умолчанию None.
    - `id_lang` (Optional[int | str], optional): Идентификатор языка для баз данных PrestaShop.
- **Возвращает**:
    - `bool`: True, если загрузка прошла успешно, False в противном случае.
- **Вызывает исключения**:
    - `FileNotFoundError`: Если файл локалей не найден.
    - `Exception`: Если во время загрузки в PrestaShop возникла ошибка.
- **Как работает функция**:
    - Функция `upload_described_products_to_prestashop` считывает информацию о продуктах из файлов JSON в папке `data_path`.
    - Затем она создает объект `PrestaProduct` для взаимодействия с API PrestaShop.
    - Для каждого продукта функция заполняет поля с помощью объекта `ProductFields` и добавляет продукт в PrestaShop с помощью метода `add_new_product`.
    - В случае ошибки функция записывает сообщение об ошибке в лог и возвращает `False`.
- **Примеры**:
    ```python
    emil = EmilDesign()
    emil.upload_described_products_to_prestashop(id_lang=2)
    ```


##  Примеры использования

```python
if __name__ == '__main__':
    emil = EmilDesign()
    asyncio.run(emil.process_suppliers())
    # emil.describe_images(lang='he')
    # emil.upload_described_products_to_prestashop(id_lang = 2)
    # asyncio.run(emil.upload_described_products_to_prestashop_async(lang='he'))
    # emil.describe_images('he')