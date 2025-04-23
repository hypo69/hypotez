### **Инструкция: Обработка успешной оплаты**

=========================================================================================

Описание
-------------------------
Обработчик `successful_payment` обрабатывает успешные платежи от пользователей, обновляет их подписку и начисляет токены.

Шаги выполнения
-------------------------
1.  Определяется `user_id` из `message.chat.id`.
2.  Проверяется `invoice_payload` для определения типа подписки (`basic` или `pro`).
3.  Если `invoice_payload` равен `'basic_invoice_payload'`, то пользователю устанавливается `db[user_id]['basic'] = True`.
4.  Если `invoice_payload` равен `'pro_invoice_payload'`, то пользователю устанавливается `db[user_id]['pro'] = True` и `db[user_id]['basic'] = True`.
5.  Пользователю начисляются токены: `db[user_id]['incoming_tokens'] = 1.7*10**5` и `db[user_id]['outgoing_tokens'] = 5*10**5`.
6.  Устанавливается дата окончания подписки: `db[user_id]['datetime_sub'] = datetime.now().replace(microsecond=0)+relativedelta(months=1)`.
7.  Обновляются данные пользователя в базе данных.
8.  Отправляется сообщение пользователю об успешной активации подписки.
9.  Вызывается функция `tb.restart(message)` для перезапуска бота.

Пример использования
-------------------------

```python
@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    global db
    user_id = str(message.chat.id)
    # Проверяется тип подписки
    if message.successful_payment.invoice_payload == 'basic_invoice_payload':
        db[user_id]['basic'] = True
    elif message.successful_payment.invoice_payload == 'pro_invoice_payload':
        db[user_id]['pro'] = True
        db[user_id]['basic'] = True

    # Начисляются токены
    db[user_id]['incoming_tokens'] = 1.7*10**5
    db[user_id]['outgoing_tokens'] = 5*10**5

    # Устанавливается дата окончания подписки
    db[user_id]['datetime_sub'] = datetime.now().replace(microsecond=0)+relativedelta(months=1)
    base.insert_or_update_data(user_id, db[user_id])
    bot.send_message(user_id, "Спасибо за оплату! Ваша подписка активирована.")
    tb.restart(message)
```

### **Инструкция: Обработка команды /start**

=========================================================================================

Описание
-------------------------
Функция `StartProcessing` обрабатывает команду `/start`, инициализирует данные пользователя, если их нет в базе данных, или восстанавливает их, если они есть.

Шаги выполнения
-------------------------
1.  Извлекается `user_id` из `message.chat.id`.
2.  Проверяется, существует ли пользователь в базе данных:
    *   Если пользователя нет в базе данных (`not db.get(user_id, False)`), создается новый шаблон данных пользователя `DATA_PATTERN()`.
    *   Если пользователь существует, восстанавливаются его данные из базы данных, сохраняя значения `basic`, `pro`, `incoming_tokens`, `outgoing_tokens`, `free_requests`, `datetime_sub`, `promocode` и `ref`.
3.  Данные пользователя добавляются или обновляются в базе данных.
4.  Вызывается функция `tb.start_request(message)` для отправки стартового запроса пользователю.

Пример использования
-------------------------

```python
@bot.message_handler(commands=['start'])
def StartProcessing(message):
    global db
    user_id = str(message.chat.id)
    # Проверяется наличие пользователя в базе данных и инициализируются данные
    db[user_id] = DATA_PATTERN() if not db.get(user_id, False) else DATA_PATTERN(basic=db[user_id]['basic'], pro=db[user_id]['pro'], incoming_tokens=db[user_id]['incoming_tokens'],
                                                                                outgoing_tokens=db[user_id]['outgoing_tokens'], free_requests=db[user_id]['free_requests'], datetime_sub=db[user_id]['datetime_sub'],
                                                                                promocode=db[user_id]['promocode'], ref=db[user_id]['ref']
                                                                                )
    base.insert_or_update_data(user_id, db[user_id])
    tb.start_request(message)
```

### **Инструкция: Обработка команды /profile**

=========================================================================================

Описание
-------------------------
Функция `personal_account` обрабатывает команду `/profile` и отображает информацию о подписке пользователя.

Шаги выполнения
-------------------------
1.  Извлекается `user_id` из `message.chat.id`.
2.  Проверяется наличие подписки `BASIC` и отсутствие подписки `PRO`:
    *   Если у пользователя подписка `BASIC`, но нет `PRO`, отправляется сообщение "Подписка: BASIC\nТекстовые генерации: безлимит\nГенерация изображений: нет".
3.  Проверяется наличие обеих подписок `BASIC` и `PRO`:
    *   Если у пользователя обе подписки, отправляется сообщение "Подписка: PRO\nТекстовые генерации: безлимит\nГенерация изображений: безлимит".
4.  Если у пользователя нет подписки:
    *   Отправляется сообщение "У вас нет подписки\nТекстовые генерации: 10 в день, осталось:{db[user_id]['free_requests']}\nГенерация изображений: нет".

Пример использования
-------------------------

```python
@bot.message_handler(commands=['profile'])
def personal_account(message):
    global db
    user_id = str(message.chat.id)
    # Проверяется тип подписки и отправляется соответствующее сообщение
    if db[user_id]['basic'] and (not db[user_id]['pro']):
        bot.send_message(chat_id=user_id, text="Подписка: BASIC\nТекстовые генерации: безлимит\nГенерация изображений: нет", parse_mode='html')
    elif db[user_id]['basic'] and db[user_id]['pro']:
        bot.send_message(chat_id=user_id, text="Подписка: PRO\nТекстовые генерации: безлимит\nГенерация изображений: безлимит", parse_mode='html')
    else:
        bot.send_message(chat_id=user_id, text=f"У вас нет подписки\nТекстовые генерации: 10 в день, осталось:{db[user_id]['free_requests']}\nГенерация изображений: нет", parse_mode='html')
```

### **Инструкция: Обработка команды /stat**

=========================================================================================

Описание
-------------------------
Функция `show_stat` обрабатывает команду `/stat` и отображает статистику по пользователям бота (доступно только для определенных user_id).

Шаги выполнения
-------------------------
1.  Извлекается `user_id` из `message.chat.id`.
2.  Проверяется, входит ли `user_id` в список доверенных (`['2004851715', '206635551']`):
    *   Если `user_id` входит в список доверенных, отправляется сообщение со статистикой: общее количество пользователей и количество пользователей с промокодом.

Пример использования
-------------------------

```python
@bot.message_handler(commands=['stat'])
def show_stat(message):
    global db
    user_id = str(message.chat.id)
    # Проверяется, является ли пользователь доверенным, и отправляется статистика
    if user_id in ['2004851715', '206635551']:
        bot.send_message(chat_id=user_id, text=f"Всего пользователей: {len(db)}\nС промокодом: {len([1 for el in db.values() if el['promocode']])}")
```

### **Инструкция: Генерация промокода**

=========================================================================================

Описание
-------------------------
Функция `generate_promo_code` генерирует случайный промокод заданной длины.

Шаги выполнения
-------------------------
1.  Определяется набор символов для генерации промокода, включающий буквы и цифры.
2.  Генерируется случайная строка заданной длины из набора символов.
3.  Возвращается сгенерированный промокод.

Пример использования
-------------------------

```python
def generate_promo_code(length):
    # Определяется набор символов для генерации
    characters = string.ascii_letters + string.digits
    # Генерируется промокод
    promo_code = ''.join(random.choices(characters, k=length))
    return promo_code
```

### **Инструкция: Обработка callback запросов**

=========================================================================================

Описание
-------------------------
Функция `CallsProcessing` обрабатывает callback запросы от нажатий на кнопки в боте, выполняя различные действия в зависимости от данных callback.

Шаги выполнения
-------------------------
1.  Извлекается `user_id` из `call.message.chat.id`.
2.  Определяется список `text_buttons` с идентификаторами кнопок для текстовых задач.
3.  Проверяется, существует ли пользователь в базе данных, и если нет, создает запись.
4.  Обрабатываются callback данные:
    *   Если `call.data` содержится в `tb.data`, вызываются соответствующие функции из `ToolBox` (например, `tb.Text_types`, `tb.ImageSize`, `tb.FreeArea`, `tb.TariffArea`).
    *   Если `call.data` соответствует одному из размеров изображения (`"576x1024"`, `"1024x1024"`, `"1024x576"`), сохраняется размер изображения и вызывается функция `tb.ImageArea`.
    *   Если `call.data` равно `"upscale"` или `"regenerate"`, выполняется масштабирование или перегенерация изображения.
    *   Если `call.data` соответствует одному из тарифов (`"basic"`, `"pro"`, `"promo"`, `"ref"`), обрабатывается выбор тарифа, активация промокода или отображение реферального кода.
    *   Если `call.data` содержится в `text_buttons`, вызываются функции для обработки текстовых задач (`tb.SomeTexts`, `tb.OneTextArea`).
    *   Если `call.data` соответствует одной из кнопок выхода (`"exit"`, `"text_exit"`, `"tariff_exit"`), выполняется выход из текущего раздела.
    *   Если `call.data` соответствует кнопкам для одной текстовой области (`f"one_{ind}"`), вызывается функция `tb.OneTextArea`.
    *   Если `call.data` соответствует кнопкам для нескольких текстовых областей (`f"some_{ind}"`), вызывается функция `tb.SomeTextsArea`.
5.  Обновляются данные пользователя в базе данных после каждого изменения.

Пример использования
-------------------------

```python
@bot.callback_query_handler(func=lambda call: True)
def CallsProcessing(call):
    global db
    user_id = str(call.message.chat.id)

    text_buttons = [
        "comm-text", "smm-text", "brainst-text",
        "advertising-text", "headlines-text", 
        "seo-text", "news", "editing"
    ]
    # Проверяется наличие пользователя в базе данных и инициализируются данные
    if not db.get(user_id):
        db[user_id] = DATA_PATTERN()
        base.insert_or_update_data(user_id, db[user_id])

    # Обрабатываются callback данные в зависимости от нажатой кнопки
    if call.data in tb.data:
        match call.data:
            # Text button
            case "text":
                tb.Text_types(call.message)
            # Image button
            case "images":
                if db[user_id]["pro"]:
                    tb.ImageSize(call.message)
                else:
                    bot.send_message(chat_id=user_id, text="Обновите ваш тариф до PRO")
                    tb.restart(call.message)
            # Free mode button
            case "free":
                db[user_id]['free'] = True
                base.insert_or_update_data(user_id, db[user_id])
                bot.delete_message(user_id, message_id=call.message.message_id)
                tb.FreeArea(call.message)
            # Tariff button
            case "tariff":
                tb.TariffArea(call.message)
    # ... (остальные обработчики callback данных)
```

### **Инструкция: Шаблон отмены токенов**

=========================================================================================

Описание
-------------------------
Функция `TokensCancelletionPattern` — это шаблон для обработки списания токенов у пользователя при выполнении текстовых задач.

Шаги выполнения
-------------------------
1.  Извлекаются значения `incoming_tokens`, `outgoing_tokens` и `free_requests` из базы данных для данного `user_id`.
2.  Проверяется, достаточно ли токенов (`incoming_tokens > 0 and outgoing_tokens > 0`) или есть ли еще бесплатные запросы (`free_requests > 0`).
3.  Если токенов или бесплатных запросов достаточно:
    *   Вызывается переданная функция `func` для выполнения задачи (например, генерации текста). Функция может быть `tb.TextCommands` или `tb.SomeTextsCommand`.
    *   Если функция вернула значения токенов, они списываются. Если функция вернула количество использованных бесплатных запросов, они списываются.
4.  Если бесплатных запросов больше нет (`db[user_id]['free_requests'] == 0`), вызывается функция `tb.FreeTariffEnd` для уведомления пользователя.
5.  Если токенов недостаточно, вызывается функция `tb.TarrifEnd` для уведомления пользователя о необходимости пополнения баланса.

Пример использования
-------------------------

```python
def TokensCancelletionPattern(user_id: str, func, message, i: int = None) -> None:
    global db
    in_tokens = db[user_id]['incoming_tokens']
    out_tokens = db[user_id]['outgoing_tokens']
    free_requests = db[user_id]['free_requests']

    # Проверяется наличие токенов или бесплатных запросов
    if in_tokens > 0 and out_tokens > 0 or free_requests > 0:
        if i is None:
            incoming_tokens, outgoing_tokens, db[user_id]['sessions_messages'] = func(message, db[user_id]['sessions_messages']); cnt = 1
        else:
            incoming_tokens, outgoing_tokens, cnt = func(message, i) if func == tb.TextCommands else func(message, i, {"incoming_tokens": in_tokens,
                                                                                                                        "outgoing_tokens": out_tokens,
                                                                                                                        "free_requests": free_requests})
        # Списываются токены или бесплатные запросы
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

### **Инструкция: Обработка входящих сообщений**

=========================================================================================

Описание
-------------------------
Функция `TasksProcessing` обрабатывает входящие текстовые сообщения и фотографии от пользователя.

Шаги выполнения
-------------------------
1.  Извлекается `user_id` из `message.chat.id`.
2.  Если пользователь находится в режиме генерации изображений (`db[user_id]['images'] != ""`) и это первый шаг (`len(db[user_id]['images'].split('|')) == 1`):
    *   Извлекается размер изображения из `db[user_id]['images']`.
    *   Текст сообщения используется как `prompt` для генерации изображения.
    *   Вызывается функция `tb.ImageCommand` для генерации изображения и получения `seed`.
    *   Сохраняются `prompt` и `seed` в `db[user_id]['images']`.
3.  Если пользователь находится в бесплатном режиме (`db[user_id]['free']`) и отправил команду "В меню":
    *   Очищается история сессии (`db[user_id]['sessions_messages'] = []`).
    *   Выключается бесплатный режим (`db[user_id]['free'] = False`).
    *   Отправляется сообщение "Сессия завершена" и вызывается функция `tb.restart(message)`.
4.  Если пользователь находится в бесплатном режиме (`db[user_id]['free']`):
    *   Если сообщение является фотографией, она кодируется в base64 и добавляется в историю сессии.
    *   Вызывается функция `TokensCancelletionPattern` для обработки запроса в бесплатном режиме.
    *   Если сообщение является текстом, вызывается функция `TokensCancelletionPattern` для обработки текстового запроса в бесплатном режиме.
5.  Если пользователь не находится в бесплатном режиме, обрабатываются текстовые задачи:
    *   Перебираются все активные текстовые задачи (`db[user_id]['text'][i]`).
    *   Если задача не требует нескольких текстов (`not db[user_id]['some']`), вызывается функция `tb.TextCommands`.
    *   Если задача требует несколько текстов (`db[user_id]['some']`), вызывается функция `tb.SomeTextsCommand`.
    *   После выполнения задачи ее статус сбрасывается.
6.  Обновляются данные пользователя в базе данных после каждого изменения.

Пример использования
-------------------------

```python
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo'])
def TasksProcessing(message):
    global db
    user_id = str(message.chat.id)

    # Обрабатывается генерация изображений
    if db[user_id]['images'] != "" and len(db[user_id]['images'].split('|')) == 1:
        size = [int(el) for el in db[user_id]['images'].split('x')]
        prompt = message.text
        seed = tb.ImageCommand(message, prompt, size)
        db[user_id]['images']+="|"+prompt+"|"+str(int(seed))
    
    # Обрабатывается выход из бесплатного режима
    elif db[user_id]['free'] and message.text == 'В меню':
        db[user_id]['sessions_messages'] = []
        db[user_id]['free'] = False
        bot.send_message(chat_id=user_id, text='Сессия завершена', reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
        tb.restart(message)

    # Обрабатываются запросы в бесплатном режиме
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
    # Обрабатываются текстовые задачи
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

### **Инструкция: Проверка окончания тарифа**

=========================================================================================

Описание
-------------------------
Асинхронная функция `end_check_tariff_time` проверяет время окончания действия тарифа у пользователей и сбрасывает их данные, если время истекло.

Шаги выполнения
-------------------------
1.  Запускается бесконечный цикл.
2.  Перебираются все пользователи в базе данных `db`.
3.  Для каждого пользователя вычисляется разница между датой окончания тарифа (`data['datetime_sub']`) и текущим временем.
4.  Если разница меньше или равна нулю и у пользователя активен тариф (`basic` или `pro`) или осталось меньше 10 бесплатных запросов (`data['free_requests'] < 10`):
    *   Данные пользователя сбрасываются к начальному состоянию, сохраняя только `text`, `images`, `free`, `promocode` и `ref`.
    *   Обновленные данные пользователя записываются в базу данных.
5.  Цикл засыпает на 10 секунд.

Пример использования
-------------------------

```python
async def end_check_tariff_time():
    while True:
        global db
        for user_id, data in db.items():
            deltaf = data['datetime_sub'] - datetime.now().replace(microsecond=0)
            # Проверяется время окончания тарифа
            if int(deltaf.total_seconds()) <= 0 and (data['basic'] or data['pro'] or data['free_requests']<10):
                db[user_id] = DATA_PATTERN(text=data['text'], images=data['images'],
                                        free=data['free'], promocode=data['promocode'], ref=data['ref'])
                base.insert_or_update_data(user_id, db[user_id])
        await asyncio.sleep(10)
```

### **Инструкция: Запуск бота**

=========================================================================================

Описание
-------------------------
Блок `if __name__ == "__main__":` запускает бота и асинхронную задачу проверки времени окончания тарифа.

Шаги выполнения
-------------------------
1.  Запускается бот в отдельном потоке с помощью `Thread(target=bot.infinity_polling).start()`.
2.  Запускается асинхронная задача `end_check_tariff_time` с помощью `asyncio.run(end_check_tariff_time())`.

Пример использования
-------------------------

```python
if __name__ == "__main__":
    Thread(target=bot.infinity_polling).start()
    asyncio.run(end_check_tariff_time())