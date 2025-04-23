# ToolBox_main.py

## Обзор

Этот модуль является основным файлом для Telegram-бота ToolBox. Он включает в себя обработку команд, колбэков,
платежей, а также проверку времени окончания действия тарифа. Модуль использует библиотеки `telebot`,
`dotenv`, `datetime`, `threading`, `dateutil`, а также собственные модули `ToolBox_requests` и `ToolBox_DataBase`.

## Подробней

Этот код реализует Telegram-бота, который предоставляет пользователям различные функции,
такие как генерация текста и изображений. Бот поддерживает несколько тарифных планов,
включая бесплатный режим с ограниченным количеством запросов и платные подписки с расширенными возможностями.

## Классы

### `DataBase`

Описание класса для взаимодействия с базой данных.

**Наследует**:
Отсутствует

**Атрибуты**:
- `db_name` (str): Имя файла базы данных.
- `table_name` (str): Имя таблицы в базе данных.
- `titles` (dict): Словарь, определяющий структуру таблицы, включая имена столбцов и их типы данных.

**Методы**:
- `create()`: Создает таблицу в базе данных, если она не существует.
- `load_data_from_db()`: Загружает данные из базы данных в словарь.
- `insert_or_update_data(user_id, data)`: Вставляет или обновляет данные пользователя в базе данных.

### `ToolBox`
Описание класса с инструментами для работы с ботом.
Включает в себя методы для обработки различных запросов и команд от пользователей.

**Наследует**:
Отсутствует

**Атрибуты**:
- `bot`: Объект бота для обработки сообщений.
- `data`: Словарь с данными для обработки различных типов запросов.

**Методы**:
- `start_request(message)`: Обрабатывает команду `/start` и отправляет приветственное сообщение с основными кнопками.
- `Text_types(message)`: Отправляет сообщение с типами текстовых запросов.
- `ImageSize(message)`: Отправляет сообщение с вариантами размеров изображений для генерации.
- `FreeArea(message)`: Активирует бесплатный режим для пользователя.
- `TariffArea(message)`: Предоставляет информацию о доступных тарифах.
- `Basic_tariff(message)`: Предлагает пользователю подключить базовый тариф.
- `Pro_tariff(message)`: Предлагает пользователю подключить тариф PRO.
- `TariffExit(message)`: Выводит из меню тарифов.
- `ImageArea(message)`: Запрашивает текст для генерации изображения.
- `Image_Regen_And_Upscale(message, prompt, size, seed)`: Генерирует изображение на основе запроса пользователя.
- `BeforeUpscale(message)`: Выводит кнопки для масштабирования и повторной генерации изображения.
- `ImageChange(message)`: Обрабатывает выбор пользователя для масштабирования или повторной генерации изображения.
- `SomeTexts(message, index)`: Предоставляет варианты генерации нескольких текстов.
- `OneTextArea(message, index)`: Предоставляет интерфейс для генерации одного текста.
- `FreeCommand(message, sessions_messages)`: Обрабатывает запросы в бесплатном режиме.
- `TextCommands(message, i)`: Обрабатывает команды для генерации текста.
- `SomeTextsCommand(message, i)`: Обрабатывает команды для генерации нескольких текстов.
- `FreeTariffEnd(message)`: Сообщает об окончании бесплатного тарифа.
- `TarrifEnd(message)`: Сообщает об окончании платного тарифа.

## Функции

### `process_pre_checkout_query(pre_checkout_query)`

**Назначение**: Обрабатывает предварительный запрос перед совершением платежа.

**Параметры**:
- `pre_checkout_query` (telebot.types.PreCheckoutQuery): Объект запроса.

**Возвращает**:
- `None`

**Как работает функция**:
Функция отвечает на предварительный запрос перед совершением платежа, подтверждая возможность проведения транзакции.

**Примеры**:
```python
# Пример вызова функции
@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
```

### `successful_payment(message)`

**Назначение**: Обрабатывает успешное завершение платежа.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения, содержащий информацию об успешном платеже.

**Возвращает**:
- `None`

**Как работает функция**:
Функция определяет, какой тариф был оплачен (basic или pro), обновляет данные пользователя в базе данных,
начисляет токены и устанавливает дату окончания подписки.

**Примеры**:
```python
# Пример обработки успешного платежа
@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    global db
    user_id = str(message.chat.id)
    # Обработка успешного платежа для активации подписки
    if message.successful_payment.invoice_payload == 'basic_invoice_payload':
        db[user_id]['basic'] = True
    elif message.successful_payment.invoice_payload == 'pro_invoice_payload':
        db[user_id]['pro'] = True
        db[user_id]['basic'] = True

    # Начисление токенов
    db[user_id]['incoming_tokens'] = 1.7*10**5
    db[user_id]['outgoing_tokens'] = 5*10**5

    # Установка даты окончания подписки
    db[user_id]['datetime_sub'] = datetime.now().replace(microsecond=0)+relativedelta(months=1)
    base.insert_or_update_data(user_id, db[user_id])
    bot.send_message(user_id, "Спасибо за оплату! Ваша подписка активирована.")
    tb.restart(message)
```

### `StartProcessing(message)`

**Назначение**: Обрабатывает команду `/start`.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения.

**Возвращает**:
- `None`

**Как работает функция**:
Функция инициализирует данные пользователя, если их нет в базе данных, или обновляет их, если они уже существуют.
Затем вызывает метод `tb.start_request(message)` для отображения начального интерфейса бота.

**Примеры**:
```python
# Пример обработки команды /start
@bot.message_handler(commands=['start'])
def StartProcessing(message):
    global db
    user_id = str(message.chat.id)
    db[user_id] = DATA_PATTERN() if not db.get(user_id, False) else DATA_PATTERN(basic=db[user_id]['basic'], pro=db[user_id]['pro'], incoming_tokens=db[user_id]['incoming_tokens'],
                                                                                outgoing_tokens=db[user_id]['outgoing_tokens'], free_requests=db[user_id]['free_requests'], datetime_sub=db[user_id]['datetime_sub'],
                                                                                promocode=db[user_id]['promocode'], ref=db[user_id]['ref']
                                                                                )
    base.insert_or_update_data(user_id, db[user_id])
    tb.start_request(message)
```

### `personal_account(message)`

**Назначение**: Обрабатывает команду `/profile` и показывает информацию о тарифном плане пользователя.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения.

**Возвращает**:
- `None`

**Как работает функция**:
Функция определяет тарифный план пользователя на основе данных в базе данных и отправляет соответствующее сообщение.

**Примеры**:
```python
# Пример обработки команды /profile
@bot.message_handler(commands=['profile'])
def personal_account(message):
    global db
    user_id = str(message.chat.id)
    if db[user_id]['basic'] and (not db[user_id]['pro']):
        bot.send_message(chat_id=user_id, text="Подписка: BASIC\nТекстовые генерации: безлимит\nГенерация изображений: нет", parse_mode='html')
    elif db[user_id]['basic'] and db[user_id]['pro']:
        bot.send_message(chat_id=user_id, text="Подписка: PRO\nТекстовые генерации: безлимит\nГенерация изображений: безлимит", parse_mode='html')
    else:
        bot.send_message(chat_id=user_id, text=f"У вас нет подписки\nТекстовые генерации: 10 в день, осталось:{db[user_id]['free_requests']}\nГенерация изображений: нет", parse_mode='html')
```

### `show_stat(message)`

**Назначение**: Отображает статистику бота для администраторов.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения.

**Возвращает**:
- `None`

**Как работает функция**:
Функция проверяет, является ли пользователь администратором, и отправляет статистику о количестве пользователей и количестве пользователей с промокодом.

**Примеры**:
```python
# Пример обработки команды /stat
@bot.message_handler(commands=['stat'])
def show_stat(message):
    global db
    user_id = str(message.chat.id)
    if user_id in ['2004851715', '206635551']:
        bot.send_message(chat_id=user_id, text=f"Всего пользователей: {len(db)}\nС промокодом: {len([1 for el in db.values() if el['promocode']])}")
```

### `generate_promo_code(length)`

**Назначение**: Генерирует случайный промокод заданной длины.

**Параметры**:
- `length` (int): Длина промокода.

**Возвращает**:
- `str`: Сгенерированный промокод.

**Как работает функция**:
Функция генерирует случайный промокод, используя символы из `string.ascii_letters` и `string.digits`.

**Примеры**:
```python
# Пример генерации промокода
def generate_promo_code(length):
    characters = string.ascii_letters + string.digits
    promo_code = ''.join(random.choices(characters, k=length))
    return promo_code
```

### `CallsProcessing(call)`

**Назначение**: Обрабатывает callback-запросы от нажатий на кнопки в боте.

**Параметры**:
- `call` (telebot.types.CallbackQuery): Объект callback-запроса.

**Возвращает**:
- `None`

**Как работает функция**:
Функция обрабатывает различные callback-запросы, такие как выбор типа текста, размера изображения, тарифа,
ввод промокода и выход из меню. В зависимости от запроса, функция вызывает соответствующие методы класса `ToolBox`
или обновляет данные пользователя в базе данных.

**Примеры**:
```python
# Пример обработки callback-запроса
@bot.callback_query_handler(func=lambda call: True)
def CallsProcessing(call):
    global db
    user_id = str(call.message.chat.id)

    # Обработка различных callback-запросов
    if call.data in tb.data:
        match call.data:
            case "text":
                tb.Text_types(call.message)
            case "images":
                if db[user_id]["pro"]:
                    tb.ImageSize(call.message)
                else:
                    bot.send_message(chat_id=user_id, text="Обновите ваш тариф до PRO")
                    tb.restart(call.message)
            case "free":
                db[user_id]['free'] = True
                base.insert_or_update_data(user_id, db[user_id])
                bot.delete_message(user_id, message_id=call.message.message_id)
                tb.FreeArea(call.message)
            case "tariff":
                tb.TariffArea(call.message)
```

### `TokensCancelletionPattern(user_id: str, func, message, i: int = None)`

**Назначение**: Паттерн для списания токенов или запросов при выполнении задач.

**Параметры**:
- `user_id` (str): ID пользователя.
- `func`: Функция для выполнения задачи (генерация текста, изображения и т.д.).
- `message`: Объект сообщения.
- `i` (int, optional): Индекс для конкретных задач.

**Возвращает**:
- `None`

**Как работает функция**:
Функция проверяет наличие токенов или бесплатных запросов у пользователя, выполняет задачу, списывает токены/запросы
и обрабатывает ситуации, когда токены или запросы заканчиваются.

**Примеры**:
```python
# Пример использования паттерна для списания токенов
def TokensCancelletionPattern(user_id: str, func, message, i: int = None) -> None:
    global db
    in_tokens = db[user_id]['incoming_tokens']
    out_tokens = db[user_id]['outgoing_tokens']
    free_requests = db[user_id]['free_requests']

    if in_tokens > 0 and out_tokens > 0 or free_requests > 0:
        if i is None:
            incoming_tokens, outgoing_tokens, db[user_id]['sessions_messages'] = func(message, db[user_id]['sessions_messages']); cnt = 1
        else:
            incoming_tokens, outgoing_tokens, cnt = func(message, i) if func == tb.TextCommands else func(message, i, {"incoming_tokens": in_tokens,
                                                                                                                        "outgoing_tokens": out_tokens,
                                                                                                                        "free_requests": free_requests})
        if in_tokens > 0 and out_tokens > 0:
            db[user_id]['incoming_tokens'] -= incoming_tokens
            db[user_id]['outgoing_tokens'] -= outgoing_tokens

        elif free_requests > 0:
            db[user_id]['free_requests'] -= cnt

    elif db[user_id]['free_requests'] == 0:
        tb.FreeTariffEnd(message)

    else:
        tb.TarrifEnd(message)
        db[user_id]['incoming_tokens'] = 0 if in_tokens <= 0 else in_tokens
        db[user_id]['outgoing_tokens'] = 0 if out_tokens <= 0 else out_tokens
        tb.restart(message)
```

### `TasksProcessing(message)`

**Назначение**: Обрабатывает текстовые сообщения и фотографии, отправленные пользователем.

**Параметры**:
- `message` (telebot.types.Message): Объект сообщения.

**Возвращает**:
- `None`

**Как работает функция**:
Функция обрабатывает различные типы сообщений, такие как запросы на генерацию изображений, выход в главное меню,
запросы в бесплатном режиме и запросы на генерацию текста. В зависимости от типа сообщения, функция вызывает
соответствующие методы класса `ToolBox` или запускает потоки для обработки задач.

**Примеры**:
```python
# Пример обработки текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo'])
def TasksProcessing(message):
    global db
    user_id = str(message.chat.id)

    # Обработка запросов на генерацию изображений
    if db[user_id]['images'] != "" and len(db[user_id]['images'].split('|')) == 1:
        size = [int(el) for el in db[user_id]['images'].split('x')]
        prompt = message.text
        seed = tb.ImageCommand(message, prompt, size)
        db[user_id]['images']+="|"+prompt+"|"+str(int(seed))
    
    # Обработка кнопки выхода в главное меню
    elif db[user_id]['free'] and message.text == 'В меню':
        db[user_id]['sessions_messages'] = []
        db[user_id]['free'] = False
        bot.send_message(chat_id=user_id, text='Сессия завершена', reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
        tb.restart(message)

    # Обработка запросов в бесплатном режиме
    elif db[user_id]['free']:
        if message.content_type == 'photo':
            photo = base64.b64encode(bot.download_file(bot.get_file(message.photo[-1].file_id).file_path)).decode()
            if message.caption is not None:
                db[user_id]['sessions_messages'].append({"content": [{"type": "text", "text": message.caption}, {"type": "image_url", "image_url": f"data:image/jpeg;base64,{photo}"}], "role": "user"})
            else:
                db[user_id]['sessions_messages'].append({"content": [{"type": "image_url", "image_url": f"data:image/jpeg;base64,{photo}"}], "role": "user"})
            thr = Thread(target=TokensCancelletionPattern, args=(user_id, tb.FreeCommand, message))
            thr.start(); thr.join()
        else:
            thr = Thread(target=TokensCancelletionPattern, args=(user_id, tb.FreeCommand, message))
            thr.start(); thr.join()
    # Обработка запросов на генерацию текста
    else:
        for i in range(len(db[user_id]['text'])):
            if db[user_id]['text'][i] and not db[user_id]['some']:
                thr=Thread(target=TokensCancelletionPattern, args=(user_id, tb.TextCommands, message, i))
                thr.start()
                db[user_id]['text'][i] = 0
                thr.join()
            elif db[user_id]['text'][i] and db[user_id]['some']:
                thr=Thread(target=TokensCancelletionPattern, args=(user_id, tb.SomeTextsCommand, message, i))
                thr.start()
                db[user_id]['text'][i] = 0
                db[user_id]['some'] = False
                thr.join()
    base.insert_or_update_data(user_id, db[user_id])
```

### `end_check_tariff_time()`

**Назначение**: Асинхронная функция для проверки времени окончания действия тарифа у пользователей.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `None`

**Как работает функция**:
Функция в бесконечном цикле проверяет для каждого пользователя, не истекло ли время действия его тарифа.
Если время истекло, функция сбрасывает данные пользователя к значениям по умолчанию.

**Примеры**:
```python
# Пример асинхронной функции для проверки времени окончания тарифа
async def end_check_tariff_time():
    while True:
        global db
        for user_id, data in db.items():
            deltaf = data['datetime_sub'] - datetime.now().replace(microsecond=0)
            if int(deltaf.total_seconds()) <= 0 and (data['basic'] or data['pro'] or data['free_requests']<10):
                db[user_id] = DATA_PATTERN(text=data['text'], images=data['images'],
                                        free=data['free'], promocode=data['promocode'], ref=data['ref'])
                base.insert_or_update_data(user_id, db[user_id])
        await asyncio.sleep(10)
```

## Запуск бота

Бот запускается в основном блоке `if __name__ == "__main__":`. В одном потоке запускается `bot.infinity_polling()`,
а в другом - асинхронная функция `end_check_tariff_time()` для проверки времени окончания действия тарифа.
```python
# Запуск бота
if __name__ == "__main__":
    Thread(target=bot.infinity_polling).start()
    asyncio.run(end_check_tariff_time())