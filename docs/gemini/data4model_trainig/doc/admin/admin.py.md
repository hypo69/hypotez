## \\file /src/endpoints/bots/telegram/digital_market/bot/admin/admin.py

# Модуль админ-панели Telegram-бота

```rst
.. module:: src.endpoints.bots.telegram.digital_market.bot.admin.admin
```

Этот модуль содержит обработчики для админ-панели Telegram-бота, предназначенного для управления цифровым магазином.

## Обзор

Модуль предоставляет инструменты для администраторов бота, позволяющие управлять товарами, просматривать статистику и выполнять другие административные действия.

## Классы

### `AddProduct`

**Описание**: Класс состояний для добавления нового товара.

**Наследует**:

*   `StatesGroup` из библиотеки `aiogram.fsm.state`.

**Атрибуты**:

*   `name` (State): Состояние для ввода имени товара.
*   `description` (State): Состояние для ввода описания товара.
*   `price` (State): Состояние для ввода цены товара.
*   `file_id` (State): Состояние для ввода ID файла товара.
*   `category_id` (State): Состояние для выбора категории товара.
*   `hidden_content` (State): Состояние для ввода скрытого контента товара.
*   `confirm_add` (State): Состояние для подтверждения добавления товара.

## Функции

### `start_admin`

```python
@admin_router.callback_query(F.data == "admin_panel", F.from_user.id.in_(settings.ADMIN_IDS))
async def start_admin(call: CallbackQuery):
```

**Назначение**: Обрабатывает нажатие кнопки "admin_panel" для входа в админ-панель.

**Как работает функция**:

1.  Проверяет, является ли пользователь администратором, используя `settings.ADMIN_IDS`.
2.  Отправляет сообщение с клавиатурой админ-панели.

### `admin_statistic`

```python
@admin_router.callback_query(F.data == 'statistic', F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_statistic(call: CallbackQuery, session_without_commit: AsyncSession):
```

**Назначение**: Обрабатывает нажатие кнопки "statistic" для получения статистики.

**Параметры**:

*   `call` (CallbackQuery): Объект обратного вызова.
*   `session_without_commit` (AsyncSession): Асинхронная сессия базы данных без коммита.

**Как работает функция**:

1.  Проверяет, является ли пользователь администратором.
2.  Извлекает статистику пользователей и платежей из базы данных, используя `UserDAO.get_statistics` и `PurchaseDao.get_payment_stats`.
3.  Формирует сообщение со статистикой и отправляет его пользователю.

### `admin_process_cancel`

```python
@admin_router.callback_query(F.data == "cancel", F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_cancel(call: CallbackQuery, state: FSMContext):
```

**Назначение**: Обрабатывает нажатие кнопки "cancel" для отмены сценария добавления товара.

**Параметры**:

*   `call` (CallbackQuery): Объект обратного вызова.
*   `state` (FSMContext): Контекст машины состояний.

**Как работает функция**:

1.  Очищает состояние машины состояний, используя `state.clear()`.
2.  Отправляет сообщение об отмене добавления товара.

### `admin_process_start_dell`

```python
@admin_router.callback_query(F.data == 'delete_product', F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_start_dell(call: CallbackQuery, session_without_commit: AsyncSession):
```

**Назначение**: Обрабатывает нажатие кнопки "delete\_product" для запуска процесса удаления товара.

**Параметры**:

*   `call` (CallbackQuery): Объект обратного вызова.
*   `session_without_commit` (AsyncSession): Асинхронная сессия базы данных без коммита.

**Как работает функция**:

1.  Извлекает все товары из базы данных, используя `ProductDao.find_all`.
2.  Отправляет пользователю сообщение со списком товаров и кнопками для удаления.

### `admin_process_start_dell` (с префиксом `dell_`)

```python
@admin_router.callback_query(F.data.startswith('dell_'), F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_start_dell(call: CallbackQuery, session_with_commit: AsyncSession):
```

**Назначение**: Обрабатывает нажатие кнопки для удаления конкретного товара.

**Параметры**:

*   `call` (CallbackQuery): Объект обратного вызова.
*   `session_with_commit` (AsyncSession): Асинхронная сессия базы данных с коммитом.

**Как работает функция**:

1.  Извлекает ID товара из данных обратного вызова.
2.  Удаляет товар из базы данных, используя `ProductDao.delete`.
3.  Отправляет пользователю сообщение об успешном удалении.

### `admin_process_products`

```python
@admin_router.callback_query(F.data == 'process_products', F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_products(call: CallbackQuery, session_without_commit: AsyncSession):
```

**Назначение**: Обрабатывает нажатие кнопки "process\_products" для перехода в режим управления товарами.

**Параметры**:

*   `call` (CallbackQuery): Объект обратного вызова.
*   `session_without_commit` (AsyncSession): Асинхронная сессия базы данных без коммита.

**Как работает функция**:

1.  Извлекает количество всех товаров из базы данных, используя `ProductDao.count`.
2.  Отправляет пользователю сообщение с клавиатурой для управления товарами.

### `admin_process_add_product`

```python
@admin_router.callback_query(F.data == 'add_product', F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_add_product(call: CallbackQuery, state: FSMContext):
```

**Назначение**: Обрабатывает нажатие кнопки "add\_product" для запуска сценария добавления товара.

**Параметры**:

*   `call` (CallbackQuery): Объект обратного вызова.
*   `state` (FSMContext): Контекст машины состояний.

**Как работает функция**:

1.  Инициирует процесс добавления товара, переходя в состояние `AddProduct.name`.
2.  Запрашивает у пользователя имя товара.

### `admin_process_name`

```python
@admin_router.message(F.text, F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.name)
async def admin_process_name(message: Message, state: FSMContext):
```

**Назначение**: Обрабатывает ввод имени товара.

**Параметры**:

*   `message` (Message): Объект сообщения.
*   `state` (FSMContext): Контекст машины состояний.

**Как работает функция**:

1.  Сохраняет имя товара в состоянии машины состояний.
2.  Запрашивает у пользователя короткое описание товара.

### `admin_process_description`

```python
@admin_router.message(F.text, F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.description)
async def admin_process_description(message: Message, state: FSMContext, session_without_commit: AsyncSession):
```

**Назначение**: Обрабатывает ввод описания товара.

**Параметры**:

*   `message` (Message): Объект сообщения.
*   `state` (FSMContext): Контекст машины состояний.
*    `session_without_commit` (AsyncSession): Асинхронная сессия базы данных без коммита.

**Как работает функция**:

1.  Сохраняет описание товара в состоянии машины состояний.
2.  Предлагает пользователю выбрать категорию товара.

### `admin_process_category`

```python
@admin_router.callback_query(F.data.startswith("add_category_"),
                             F.from_user.id.in_(settings.ADMIN_IDS),
                             AddProduct.category_id)
async def admin_process_category(call: CallbackQuery, state: FSMContext):
```

**Назначение**: Обрабатывает выбор категории товара.

**Параметры**:

*   `call` (CallbackQuery): Объект обратного вызова.
*   `state` (FSMContext): Контекст машины состояний.

**Как работает функция**:

1.  Извлекает ID категории из данных обратного вызова.
2.  Сохраняет ID категории в состоянии машины состояний.
3.  Запрашивает у пользователя цену товара.

### `admin_process_price`

```python
@admin_router.message(F.text, F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.price)
async def admin_process_price(message: Message, state: FSMContext):
```

**Назначение**: Обрабатывает ввод цены товара.

**Параметры**:

*   `message` (Message): Объект сообщения.
*   `state` (FSMContext): Контекст машины состояний.

**Как работает функция**:

1.  Пытается преобразовать введенный текст в число.
2.  Сохраняет цену товара в состоянии машины состояний.
3.  Предлагает пользователю отправить файл товара или отказаться от его отправки.

### `admin_process_without_file` (callback_query)

```python
@admin_router.callback_query(F.data == "without_file", F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.file_id)
async def admin_process_without_file(call: CallbackQuery, state: FSMContext):
```

**Назначение**: Обрабатывает отказ от отправки файла товара.

**Параметры**:

*   `call` (CallbackQuery): Объект обратного вызова.
*   `state` (FSMContext): Контекст машины состояний.

**Как работает функция**:

1.  Сохраняет `None` в качестве ID файла товара.
2.  Предлагает пользователю отправить контент, который будет отображаться после покупки товара.

### `admin_process_without_file` (message)

```python
@admin_router.message(F.document, F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.file_id)
async def admin_process_without_file(message: Message, state: FSMContext):
```

**Назначение**: Обрабатывает отправку файла товара.

**Параметры**:

*   `message` (Message): Объект сообщения.
*   `state` (FSMContext): Контекст машины состояний.

**Как работает функция**:

1.  Сохраняет ID файла товара.
2.  Предлагает пользователю отправить контент, который будет отображаться после покупки товара.

### `admin_process_hidden_content`

```python
@admin_router.message(F.text, F.from_user.id.in_(settings.ADMIN_IDS), AddProduct.hidden_content)
async def admin_process_hidden_content(message: Message, state: FSMContext, session_without_commit: AsyncSession):
```

**Назначение**: Обрабатывает ввод скрытого контента товара.

**Параметры**:

*   `message` (Message): Объект сообщения.
*   `state` (FSMContext): Контекст машины состояний.
*    `session_without_commit` (AsyncSession): Асинхронная сессия базы данных без коммита.

**Как работает функция**:

1.  Сохраняет скрытый контент товара в состоянии машины состояний.
2.  Формирует сообщение с информацией о товаре и предлагает подтвердить добавление.

### `admin_process_confirm_add`

```python
@admin_router.callback_query(F.data == "confirm_add", F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_process_confirm_add(call: CallbackQuery, state: FSMContext, session_with_commit: AsyncSession):
```

**Назначение**: Обрабатывает подтверждение добавления товара.

**Параметры**:

*   `call` (CallbackQuery): Объект обратного вызова.
*   `state` (FSMContext): Контекст машины состояний.
*   `session_with_commit` (AsyncSession): Асинхронная сессия базы данных с коммитом.

**Как работает функция**:

1.  Извлекает данные о товаре из состояния машины состояний.
2.  Добавляет товар в базу данных, используя `ProductDao.add`.
3.  Отправляет пользователю сообщение об успешном добавлении товара.