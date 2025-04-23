# Модуль `admin`

## Обзор

Модуль `admin` содержит функциональность для администрирования Telegram-бота, включая обработку команд администратора, добавление и удаление товаров, получение статистики и управление категориями. Он использует библиотеку `aiogram` для обработки входящих запросов и `SQLAlchemy` для взаимодействия с базой данных.

## Более подробно

Модуль предоставляет набор обработчиков для различных действий администратора, таких как просмотр статистики, управление товарами и добавление новых товаров. Он также определяет конечные автоматы (FSM) для упрощения процесса добавления товаров.

## Классы

### `AddProduct`

**Описание**: Класс `AddProduct` представляет собой конечный автомат (FSM) для процесса добавления нового товара.

**Наследует**:
- `StatesGroup` из `aiogram.fsm.state`.

**Атрибуты**:
- `name` (`State`): Состояние для ввода имени товара.
- `description` (`State`): Состояние для ввода описания товара.
- `price` (`State`): Состояние для ввода цены товара.
- `file_id` (`State`): Состояние для загрузки файла товара.
- `category_id` (`State`): Состояние для выбора категории товара.
- `hidden_content` (`State`): Состояние для ввода скрытого содержимого товара.
- `confirm_add` (`State`): Состояние для подтверждения добавления товара.

**Принцип работы**:
Класс определяет состояния, через которые проходит процесс добавления товара. Каждое состояние соответствует определенному шагу, например, вводу имени, описания, цены и т.д. Это позволяет организовать процесс добавления товара в виде последовательности шагов, что упрощает его реализацию и поддержку.

## Маршрутизаторы

### `admin_router`

- Маршрутизатор для обработки административных команд.

## Функции

### `start_admin`

```python
async def start_admin(call: CallbackQuery):
    """Функция предоставляет доступ в админ-панель Telegram-бота.

    Args:
        call (CallbackQuery): Объект, содержащий информацию о нажатой кнопке.

    Raises:
        Exception: Если происходит ошибка при открытии админ-панели.

    """
```

**Назначение**:

Функция обрабатывает нажатие кнопки "admin_panel" и предоставляет доступ в админ-панель администраторам, чьи идентификаторы указаны в `settings.ADMIN_IDS`.

**Параметры**:

- `call` (`CallbackQuery`): Объект, содержащий информацию о нажатой кнопке.

**Как работает функция**:

- Проверяет, является ли пользователь администратором.
- Отправляет подтверждение доступа в админ-панель.
- Пытается отредактировать сообщение с кнопками администратора.
- В случае ошибки удаляет исходное сообщение и отправляет новое сообщение с кнопками администратора.

**Примеры**:

```python
# Пример вызова функции при нажатии кнопки "admin_panel"
@admin_router.callback_query(F.data == "admin_panel", F.from_user.id.in_(settings.ADMIN_IDS))
async def start_admin(call: CallbackQuery):
    ...
```

### `admin_statistic`

```python
async def admin_statistic(call: CallbackQuery, session_without_commit: AsyncSession):
    """Функция получает и отображает статистику по пользователям и заказам.

    Args:
        call (CallbackQuery): Объект, содержащий информацию о нажатой кнопке.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов к базе данных без коммита.

    """
```

**Назначение**:

Функция обрабатывает нажатие кнопки "statistic" и отображает статистику по пользователям и заказам.

**Параметры**:

- `call` (`CallbackQuery`): Объект, содержащий информацию о нажатой кнопке.
- `session_without_commit` (`AsyncSession`): Асинхронная сессия SQLAlchemy для выполнения запросов к базе данных без коммита.

**Как работает функция**:

- Отправляет подтверждение запроса на получение статистики.
- Получает статистику пользователей и общую статистику по заказам из базы данных.
- Формирует сообщение со статистикой.
- Редактирует сообщение с кнопками администратора, заменяя его сообщением со статистикой.

**Примеры**:

```python
# Пример вызова функции при нажатии кнопки "statistic"
@admin_router.callback_query(F.data == 'statistic', F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_statistic(call: CallbackQuery, session_without_commit: AsyncSession):
    ...
```

### `admin_process_cancel`

```python
async def admin_process_cancel(call: CallbackQuery, state: FSMContext):
    """Функция отменяет сценарий добавления товара.

    Args:
        call (CallbackQuery): Объект, содержащий информацию о нажатой кнопке.
        state (FSMContext): Объект, содержащий состояние конечного автомата.

    """
```

**Назначение**:

Функция обрабатывает нажатие кнопки "cancel" и отменяет сценарий добавления товара.

**Параметры**:

- `call` (`CallbackQuery`): Объект, содержащий информацию о нажатой кнопке.
- `state` (`FSMContext`): Объект, содержащий состояние конечного автомата.

**Как работает функция**:

- Очищает состояние конечного автомата.
- Отправляет подтверждение отмены сценария добавления товара.
- Удаляет исходное сообщение и отправляет новое сообщение с кнопками администратора.

**Примеры**:

```python
# Пример вызова функции при нажатии кнопки "cancel"
@admin_router.callback_query(F.data == "cancel", F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_cancel(call: CallbackQuery, state: FSMContext):
    ...
```

### `admin_process_start_dell`

```python
async def admin_process_start_dell(call: CallbackQuery, session_without_commit: AsyncSession):
    """Функция запускает режим удаления товаров.

    Args:
        call (CallbackQuery): Объект, содержащий информацию о нажатой кнопке.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов к базе данных без коммита.

    """
```

**Назначение**:

Функция обрабатывает нажатие кнопки "delete_product" и запускает режим удаления товаров.

**Параметры**:

- `call` (`CallbackQuery`): Объект, содержащий информацию о нажатой кнопке.
- `session_without_commit` (`AsyncSession`): Асинхронная сессия SQLAlchemy для выполнения запросов к базе данных без коммита.

**Как работает функция**:

- Получает список всех товаров из базы данных.
- Отправляет сообщение с информацией о количестве товаров.
- Для каждого товара формирует текстовое описание и отправляет его вместе с кнопкой для удаления товара.

**Примеры**:

```python
# Пример вызова функции при нажатии кнопки "delete_product"
@admin_router.callback_query(F.data == 'delete_product', F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_start_dell(call: CallbackQuery, session_without_commit: AsyncSession):
    ...
```

### `admin_process_start_dell` (удаление товара)

```python
async def admin_process_start_dell(call: CallbackQuery, session_with_commit: AsyncSession):
    """Функция удаляет выбранный товар из базы данных.

    Args:
        call (CallbackQuery): Объект, содержащий информацию о нажатой кнопке.
        session_with_commit (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов к базе данных с коммитом.

    """
```

**Назначение**:

Функция обрабатывает нажатие кнопки удаления товара (кнопки, начинающиеся с "dell_") и удаляет выбранный товар из базы данных.

**Параметры**:

- `call` (`CallbackQuery`): Объект, содержащий информацию о нажатой кнопке.
- `session_with_commit` (`AsyncSession`): Асинхронная сессия SQLAlchemy для выполнения запросов к базе данных с коммитом.

**Как работает функция**:

- Извлекает ID товара из данных обратного вызова.
- Удаляет товар из базы данных.
- Отправляет подтверждение удаления товара.
- Удаляет сообщение с информацией о товаре.

**Примеры**:

```python
# Пример вызова функции при нажатии кнопки удаления товара
@admin_router.callback_query(F.data.startswith('dell_'), F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_start_dell(call: CallbackQuery, session_with_commit: AsyncSession):
    ...
```

### `admin_process_products`

```python
async def admin_process_products(call: CallbackQuery, session_without_commit: AsyncSession):
    """Функция предоставляет меню управления товарами.

    Args:
        call (CallbackQuery): Объект, содержащий информацию о нажатой кнопке.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов к базе данных без коммита.

    """
```

**Назначение**:

Функция обрабатывает нажатие кнопки "process_products" и предоставляет меню управления товарами.

**Параметры**:

- `call` (`CallbackQuery`): Объект, содержащий информацию о нажатой кнопке.
- `session_without_commit` (`AsyncSession`): Асинхронная сессия SQLAlchemy для выполнения запросов к базе данных без коммита.

**Как работает функция**:

- Получает количество всех товаров из базы данных.
- Редактирует сообщение с кнопками администратора, заменяя его сообщением с меню управления товарами.

**Примеры**:

```python
# Пример вызова функции при нажатии кнопки "process_products"
@admin_router.callback_query(F.data == 'process_products', F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_products(call: CallbackQuery, session_without_commit: AsyncSession):
    ...
```

### `admin_process_add_product`

```python
async def admin_process_add_product(call: CallbackQuery, state: FSMContext):
    """Функция запускает сценарий добавления товара.

    Args:
        call (CallbackQuery): Объект, содержащий информацию о нажатой кнопке.
        state (FSMContext): Объект, содержащий состояние конечного автомата.

    """
```

**Назначение**:

Функция обрабатывает нажатие кнопки "add_product" и запускает сценарий добавления товара.

**Параметры**:

- `call` (`CallbackQuery`): Объект, содержащий информацию о нажатой кнопке.
- `state` (`FSMContext`): Объект, содержащий состояние конечного автомата.

**Как работает функция**:

- Отправляет подтверждение запуска сценария добавления товара.
- Удаляет исходное сообщение и отправляет новое сообщение с запросом имени товара.
- Устанавливает состояние `AddProduct.name`.

**Примеры**:

```python
# Пример вызова функции при нажатии кнопки "add_product"
@admin_router.callback_query(F.data == 'add_product', F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_add_product(call: CallbackQuery, state: FSMContext):
    ...
```

### `admin_process_name`

```python
async def admin_process_name(message: Message, state: FSMContext):
    """Функция обрабатывает введенное имя товара.

    Args:
        message (Message): Объект, содержащий информацию о сообщении пользователя.
        state (FSMContext): Объект, содержащий состояние конечного автомата.

    """
```

**Назначение**:

Функция обрабатывает введенное имя товара и переходит к следующему шагу - вводу описания товара.

**Параметры**:

- `message` (`Message`): Объект, содержащий информацию о сообщении пользователя.
- `state` (`FSMContext`): Объект, содержащий состояние конечного автомата.

**Как работает функция**:

- Сохраняет имя товара в состоянии конечного автомата.
- Удаляет предыдущее сообщение пользователя.
- Отправляет сообщение с запросом описания товара.
- Устанавливает состояние `AddProduct.description`.

**Примеры**:

```python
# Пример вызова функции при вводе имени товара
@admin_router.message(F.text, F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.name)
async def admin_process_name(message: Message, state: FSMContext):
    ...
```

### `admin_process_description`

```python
async def admin_process_description(message: Message, state: FSMContext, session_without_commit: AsyncSession):
    """Функция обрабатывает введенное описание товара.

    Args:
        message (Message): Объект, содержащий информацию о сообщении пользователя.
        state (FSMContext): Объект, содержащий состояние конечного автомата.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов к базе данных без коммита.

    """
```

**Назначение**:

Функция обрабатывает введенное описание товара и переходит к следующему шагу - выбору категории товара.

**Параметры**:

- `message` (`Message`): Объект, содержащий информацию о сообщении пользователя.
- `state` (`FSMContext`): Объект, содержащий состояние конечного автомата.
- `session_without_commit` (`AsyncSession`): Асинхронная сессия SQLAlchemy для выполнения запросов к базе данных без коммита.

**Как работает функция**:

- Сохраняет описание товара в состоянии конечного автомата.
- Удаляет предыдущее сообщение пользователя.
- Получает список категорий из базы данных.
- Отправляет сообщение с запросом выбора категории товара.
- Устанавливает состояние `AddProduct.category_id`.

**Примеры**:

```python
# Пример вызова функции при вводе описания товара
@admin_router.message(F.text, F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.description)
async def admin_process_description(message: Message, state: FSMContext, session_without_commit: AsyncSession):
    ...
```

### `admin_process_category`

```python
async def admin_process_category(call: CallbackQuery, state: FSMContext):
    """Функция обрабатывает выбранную категорию товара.

    Args:
        call (CallbackQuery): Объект, содержащий информацию о нажатой кнопке.
        state (FSMContext): Объект, содержащий состояние конечного автомата.

    """
```

**Назначение**:

Функция обрабатывает выбранную категорию товара и переходит к следующему шагу - вводу цены товара.

**Параметры**:

- `call` (`CallbackQuery`): Объект, содержащий информацию о нажатой кнопке.
- `state` (`FSMContext`): Объект, содержащий состояние конечного автомата.

**Как работает функция**:

- Извлекает ID категории из данных обратного вызова.
- Сохраняет ID категории в состоянии конечного автомата.
- Отправляет подтверждение выбора категории товара.
- Редактирует сообщение с запросом цены товара.
- Устанавливает состояние `AddProduct.price`.

**Примеры**:

```python
# Пример вызова функции при выборе категории товара
@admin_router.callback_query(F.data.startswith("add_category_"),
                             F.from_user.id.in_(settings.ADMIN_IDS),
                             AddProduct.category_id)
async def admin_process_category(call: CallbackQuery, state: FSMContext):
    ...
```

### `admin_process_price`

```python
async def admin_process_price(message: Message, state: FSMContext):
    """Функция обрабатывает введенную цену товара.

    Args:
        message (Message): Объект, содержащий информацию о сообщении пользователя.
        state (FSMContext): Объект, содержащий состояние конечного автомата.

    """
```

**Назначение**:

Функция обрабатывает введенную цену товара и переходит к следующему шагу - отправке файла товара (если требуется).

**Параметры**:

- `message` (`Message`): Объект, содержащий информацию о сообщении пользователя.
- `state` (`FSMContext`): Объект, содержащий состояние конечного автомата.

**Как работает функция**:

- Пытается преобразовать введенный текст в число.
- Сохраняет цену товара в состоянии конечного автомата.
- Удаляет предыдущее сообщение пользователя.
- Отправляет сообщение с запросом файла товара.
- Устанавливает состояние `AddProduct.file_id`.
- В случае ошибки отправляет сообщение об ошибке и остается в текущем состоянии.

**Примеры**:

```python
# Пример вызова функции при вводе цены товара
@admin_router.message(F.text, F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.price)
async def admin_process_price(message: Message, state: FSMContext):
    ...
```

### `admin_process_without_file` (без файла)

```python
async def admin_process_without_file(call: CallbackQuery, state: FSMContext):
    """Функция обрабатывает выбор товара без файла.

    Args:
        call (CallbackQuery): Объект, содержащий информацию о нажатой кнопке.
        state (FSMContext): Объект, содержащий состояние конечного автомата.

    """
```

**Назначение**:

Функция обрабатывает нажатие кнопки "without_file" и переходит к следующему шагу - вводу скрытого содержимого товара.

**Параметры**:

- `call` (`CallbackQuery`): Объект, содержащий информацию о нажатой кнопке.
- `state` (`FSMContext`): Объект, содержащий состояние конечного автомата.

**Как работает функция**:

- Сохраняет `None` в качестве ID файла в состоянии конечного автомата.
- Отправляет подтверждение выбора товара без файла.
- Редактирует сообщение с запросом скрытого содержимого товара.
- Устанавливает состояние `AddProduct.hidden_content`.

**Примеры**:

```python
# Пример вызова функции при выборе товара без файла
@admin_router.callback_query(F.data == "without_file", F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.file_id)
async def admin_process_without_file(call: CallbackQuery, state: FSMContext):
    ...
```

### `admin_process_without_file` (с файлом)

```python
async def admin_process_without_file(message: Message, state: FSMContext):
    """Функция обрабатывает отправленный файл товара.

    Args:
        message (Message): Объект, содержащий информацию о сообщении пользователя.
        state (FSMContext): Объект, содержащий состояние конечного автомата.

    """
```

**Назначение**:

Функция обрабатывает отправленный файл товара и переходит к следующему шагу - вводу скрытого содержимого товара.

**Параметры**:

- `message` (`Message`): Объект, содержащий информацию о сообщении пользователя.
- `state` (`FSMContext`): Объект, содержащий состояние конечного автомата.

**Как работает функция**:

- Сохраняет ID файла в состоянии конечного автомата.
- Удаляет предыдущее сообщение пользователя.
- Отправляет сообщение с запросом скрытого содержимого товара.
- Устанавливает состояние `AddProduct.hidden_content`.

**Примеры**:

```python
# Пример вызова функции при отправке файла товара
@admin_router.message(F.document, F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.file_id)
async def admin_process_without_file(message: Message, state: FSMContext):
    ...
```

### `admin_process_hidden_content`

```python
async def admin_process_hidden_content(message: Message, state: FSMContext, session_without_commit: AsyncSession):
    """Функция обрабатывает введенное скрытое содержимое товара.

    Args:
        message (Message): Объект, содержащий информацию о сообщении пользователя.
        state (FSMContext): Объект, содержащий состояние конечного автомата.
        session_without_commit (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов к базе данных без коммита.

    """
```

**Назначение**:

Функция обрабатывает введенное скрытое содержимое товара и переходит к следующему шагу - подтверждению добавления товара.

**Параметры**:

- `message` (`Message`): Объект, содержащий информацию о сообщении пользователя.
- `state` (`FSMContext`): Объект, содержащий состояние конечного автомата.
- `session_without_commit` (`AsyncSession`): Асинхронная сессия SQLAlchemy для выполнения запросов к базе данных без коммита.

**Как работает функция**:

- Сохраняет скрытое содержимое товара в состоянии конечного автомата.
- Получает данные о товаре из состояния конечного автомата.
- Получает информацию о категории товара из базы данных.
- Формирует текстовое описание товара с информацией о названии, описании, цене, скрытом содержимом и категории.
- Отправляет сообщение с информацией о товаре и кнопками подтверждения.
- Устанавливает состояние `AddProduct.confirm_add`.

**Примеры**:

```python
# Пример вызова функции при вводе скрытого содержимого товара
@admin_router.message(F.text, F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.hidden_content)
async def admin_process_hidden_content(message: Message, state: FSMContext, session_without_commit: AsyncSession):
    ...
```

### `admin_process_confirm_add`

```python
async def admin_process_confirm_add(call: CallbackQuery, state: FSMContext, session_with_commit: AsyncSession):
    """Функция подтверждает добавление товара в базу данных.

    Args:
        call (CallbackQuery): Объект, содержащий информацию о нажатой кнопке.
        state (FSMContext): Объект, содержащий состояние конечного автомата.
        session_with_commit (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения запросов к базе данных с коммитом.

    """
```

**Назначение**:

Функция обрабатывает нажатие кнопки "confirm_add" и добавляет товар в базу данных.

**Параметры**:

- `call` (`CallbackQuery`): Объект, содержащий информацию о нажатой кнопке.
- `state` (`FSMContext`): Объект, содержащий состояние конечного автомата.
- `session_with_commit` (`AsyncSession`): Асинхронная сессия SQLAlchemy для выполнения запросов к базе данных с коммитом.

**Как работает функция**:

- Отправляет подтверждение начала сохранения файла.
- Получает данные о товаре из состояния конечного автомата.
- Удаляет сообщение с информацией о товаре и кнопками подтверждения.
- Добавляет товар в базу данных.
- Отправляет сообщение об успешном добавлении товара.

**Примеры**:

```python
# Пример вызова функции при подтверждении добавления товара
@admin_router.callback_query(F.data == "confirm_add", F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_confirm_add(call: CallbackQuery, state: FSMContext, session_with_commit: AsyncSession):
    ...