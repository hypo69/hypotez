### **Анализ кода модуля `ToolBox_requests.py`**

**Расположение файла:** `hypotez/src/endpoints/bots/telegram/ToolBoxbot-main/ToolBox/ToolBox_requests.py`

**Назначение модуля:** Модуль содержит класс `ToolBox`, который обрабатывает запросы от Telegram-бота, включая текстовые и графические запросы, запросы тарифов и свободный режим.

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код структурирован в классы и методы, что облегчает его понимание.
    - Используются лямбда-функции для упрощения создания клавиатур и обработки запросов.
- **Минусы**:
    - Не все переменные аннотированы типами.
    - Использование `Union` отсутствует.
    - Многие docstring отсутствуют или не соответствуют требуемому формату.
    - Жестко заданные значения (`99*100`, `199*100`) без объяснения в коде.

**Рекомендации по улучшению:**

1.  **Добавить docstring к классам и методам:**
    - Описать назначение каждого класса и метода, а также параметры и возвращаемые значения.
    - Добавить примеры использования.

2.  **Добавить аннотации типов для переменных и параметров функций:**
    - Это улучшит читаемость и облегчит отладку кода.

3.  **Заменить лямбда-функции на обычные функции, если они сложны для понимания:**
    - Лямбда-функции должны быть простыми и понятными.

4.  **Улучшить обработку исключений:**
    - Добавить логирование ошибок с использованием `logger.error`.

5.  **Удалить неиспользуемые переменные и импорты:**
    - Это сделает код чище и понятнее.

6.  **Использовать более понятные имена для переменных:**
    - Имена переменных должны отражать их назначение.

7.  **Добавить комментарии для сложных участков кода:**
    - Комментарии должны объяснять логику работы кода.

8.  **Использовать f-строки вместо конкатенации строк:**
    - F-строки более читаемы и эффективны.

9. **Обработка `...` в коде**:
    - Оставляйте `...` как указатели в коде без изменений.
    - Не документируйте строки с `...`.

**Оптимизированный код:**

```python
import telebot
import os
import json
import concurrent.futures
import time
from random import randint
from telebot import types
from src.logger import logger #Лоргер
from BaseSettings.AuxiliaryClasses import PromptsCompressor, keyboards
from ToolBox_n_networks import neural_networks
from typing import List, Dict, Tuple, Callable, Optional

# Class initialization
pc = PromptsCompressor()

# Main functions class
class ToolBox(keyboards, neural_networks):
    """
    Класс для обработки запросов Telegram-бота.

    Args:
        keyboards: Класс для работы с клавиатурами.
        neural_networks: Класс для работы с нейронными сетями.

    """
    def __init__(self):
        """
        Инициализация класса ToolBox.
        """
        # Start buttons
        self.name: List[str] = ["Текст 📝", "Изображения 🎨", "Свободный режим 🗽", "Тарифы 💸"]
        self.data: List[str] = ["text", "images", "free", "tariff"]

        # Promts texts load
        with open("ToolBox/BaseSettings/prompts.json", 'r') as file:
            self.prompts_text: Dict = json.load(file)

        # Telegram bot initialization
        self.bot: telebot.TeleBot = telebot.TeleBot(token=os.environ['TOKEN'])
        # Inline keyboard blank lambda
        self.keyboard_blank: Callable = lambda self, name, data: super()._keyboard_two_blank(data, name)
        # Markup keyboard
        self.reply_keyboard: Callable = lambda self, name: super()._reply_keyboard(name)
        # Request delay
        self.__delay: Callable = lambda message, self=self: self.bot.send_message(message.chat.id, "Подождите, это должно занять несколько секунд . . .", parse_mode='html')
        # Start request
        self.start_request: Callable = lambda message, self=self: self.bot.send_message(message.chat.id, self.prompts_text['hello'], reply_markup=self.keyboard_blank(self, self.name, self.data), parse_mode='html')
        # Restart request
        self.restart: Callable = lambda message, self=self: self.bot.send_message(message.chat.id, "Выберите нужную вам задачу", reply_markup=self.keyboard_blank(self, self.name, self.data), parse_mode='html')
        # Restart murkup
        self.restart_markup: Callable = lambda message, self=self: self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Выберите нужную вам задачу", reply_markup=self.keyboard_blank(self, self.name, self.data), parse_mode='html')
        # One text request
        self.OneTextArea: Callable = lambda message, ind, self=self: self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=self.prompts_text['text_list'][ind] if type(self.prompts_text['text_list'][ind]) == str else self.prompts_text['text_list'][ind][0], reply_markup=self.keyboard_blank(self, ["Назад"], ["text_exit"]))
        # Some texts request
        self.SomeTextsArea: Callable = lambda message, ind, self=self: self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=self.prompts_text['few_texts_list'][ind][0], reply_markup=self.keyboard_blank(self, ["Назад"], ["text_exit"]))
        # Image size
        self.ImageSize: Callable = lambda message, self=self: self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Выберите разрешение изображения", reply_markup=self.keyboard_blank(self, ["9:16", "1:1", "16:9", "В меню"], ["576x1024", "1024x1024", "1024x576", "exit"]), parse_mode='html')
        # Image request
        self.ImageArea: Callable = lambda message, self=self: self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Введите ваш запрос для изображений 🖼", reply_markup=self.keyboard_blank(self, ["В меню"], ["exit"]), parse_mode='html')
        # Image change
        self.ImageChange: Callable = lambda message, self=self: self.bot.send_message(chat_id=message.chat.id, text="Выберите следующее действие", reply_markup=self.keyboard_blank(self, ["Улучшить 🪄", "🔁", "Новая 🖼", "В меню"], ["upscale", "regenerate", "images", "exit"]), parse_mode='html')
        # Message before upscale
        self.BeforeUpscale: Callable = lambda message, self=self: self.bot.send_message(chat_id=message.chat.id, text="Выберите следующее действие", reply_markup=self.keyboard_blank(self, ["🔁", "Новая 🖼", "В меню"], ["regenerate", "images", "exit"]), parse_mode='html')
        # Free mode request
        self.FreeArea: Callable = lambda message, self=self: self.bot.send_message(chat_id=message.chat.id, text="Введите ваш запрос", reply_markup=self.reply_keyboard(self, ["В меню"]), parse_mode='html')
        # Tariff request
        self.TariffArea: Callable = lambda message, self=self: self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Тарифы", reply_markup=self.keyboard_blank(self, ["BASIC", "PRO", "Промокод", "Реферальная программа", "В меню"], ["basic", "pro", "promo", "ref", "exit"]))
        # Tariffs area exit
        self.TariffExit: Callable = lambda message, self=self: self.bot.send_message(chat_id=message.chat.id, text="Тарифы", reply_markup=self.keyboard_blank(self, ["BASIC", "PRO", "Промокод", "В меню"], ["basic", "pro", "promo", "exit"]))
        # End tariff
        self.TarrifEnd: Callable = lambda message, self=self: self.bot.send_message(chat_id=message.chat.id, text="У вас закончились запросы, но вы можете продлить ваш тариф.", reply_markup=self.keyboard_blank(self, ["BASIC", "PRO", "Промокод", "Реферальная программа", "В меню"], ["basic", "pro", "promo", "ref", "exit"]))
        # Free tariff end
        self.FreeTariffEnd: Callable = lambda message, self=self: self.bot.send_message(chat_id=message.chat.id, text="Лимит бесплатных запросов, увы, исчерпан😢 Но вы можете выбрать один из наших платных тарифов. Просто нажмите на них и получите подробное описание", reply_markup=self.keyboard_blank(self, ["BASIC", "PRO", "Промокод", "Реферальная программа", "В меню"], ["basic", "pro", "promo", "ref", "exit"]))
        # Select one or some texts
        self.SomeTexts: Callable = lambda message, ind, self=self: self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Хотите сделать один текст или сразу несколько?", reply_markup=self.keyboard_blank(self, ["Один", "Несколько", "Назад"], [f"one_{ind}", f"some_{ind}", "text_exit"]))

#Private
    # GPT 4o mini processing
    def __gpt_4o_mini(self, prompt: List[Dict[str, str]], message: telebot.types.Message) -> Tuple[Dict[str, str], int, int]:
        """
        Обрабатывает запрос к GPT 4o mini.

        Args:
            prompt (List[Dict[str, str]]): Список промптов.
            message (telebot.types.Message): Объект сообщения Telegram.

        Returns:
            Tuple[Dict[str, str], int, int]: Кортеж, содержащий ответ, количество входящих и исходящих токенов.
        """
        send: telebot.types.Message = self.__delay(message)
        response, incoming_tokens, outgoing_tokens = super()._free_gpt_4o_mini(prompt=prompt)
        self.bot.edit_message_text(chat_id=send.chat.id, message_id=send.message_id, text=PromptsCompressor.html_tags_insert(response['content']), parse_mode='html')
        return response, incoming_tokens, outgoing_tokens

    # FLUX schnell processing
    def __FLUX_schnell(self, prompt: str, size: List[int], message: telebot.types.Message, seed: int, num_inference_steps: int) -> None:
        """
        Обрабатывает запрос к FLUX schnell.

        Args:
            prompt (str): Промпт.
            size (List[int]): Размер изображения.
            message (telebot.types.Message): Объект сообщения Telegram.
            seed (int): Зерно для генерации.
            num_inference_steps (int): Количество шагов для генерации.
        """
        send: telebot.types.Message = self.__delay(message)
        while True:
            try:
                photo: bytes = super()._FLUX_schnell(prompt, size, seed, num_inference_steps)
            except Exception as ex:
                logger.error('Error while processing FLUX schnell', ex, exc_info=True)
                continue
            else:
                break
        if photo:
            self.bot.send_photo(chat_id=message.chat.id, photo=photo)
            return self.bot.delete_message(chat_id=send.chat.id, message_id=send.message_id)
        self.bot.edit_message_text(chat_id=send.chat.id, message_id=send.message_id, text="При генерации возникла ошибка, попробуйте повторить позже")

#Public
    # Text types
    def Text_types(self, message: telebot.types.Message) -> None:
        """
        Выводит типы текстов.

        Args:
            message (telebot.types.Message): Объект сообщения Telegram.
        """
        name: List[str] = ["Коммерческий  🛍️", "SMM 📱", "Брейншторм 💡", "Реклама 📺", "Заголовки 🔍", "SEO 🌐", "Новость 📰", "Редактура 📝", "В меню"]
        data: List[str] = ["comm-text", "smm-text", "brainst-text", "advertising-text", "headlines-text", "seo-text", "news", "editing", "exit"]
        return self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="📝 Выберите тип текста", reply_markup=self.keyboard_blank(self, name, data))

    # Tariffs
    # Basic tariff
    def Basic_tariff(self, message: telebot.types.Message) -> None:
        """
        Выводит информацию о базовом тарифе.

        Args:
            message (telebot.types.Message): Объект сообщения Telegram.
        """
        keyboard: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Подключить тариф BASIC", pay=True))
        keyboard.add(types.InlineKeyboardButton("К тарифам", callback_data="tariff_exit"))
        price: List[types.LabeledPrice] = [types.LabeledPrice(label='BASIC', amount=99*100)] #Цена в копейках
        self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        self.bot.send_invoice(chat_id=message.chat.id, title='BASIC',
            description="Безлимитная генерация текста, в том числе по готовым промптам.",
            invoice_payload='basic_invoice_payload',
            start_parameter='subscription',
            provider_token=os.environ['PROVIDE_TOKEN'],
            currency='RUB', prices=price, reply_markup=keyboard)

    # Pro tariff
    def Pro_tariff(self, message: telebot.types.Message) -> None:
        """
        Выводит информацию о профессиональном тарифе.

        Args:
            message (telebot.types.Message): Объект сообщения Telegram.
        """
        keyboard: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Подключить тариф PRO", pay=True))
        keyboard.add(types.InlineKeyboardButton("К тарифам", callback_data="tariff_exit"))
        price: List[types.LabeledPrice] = [types.LabeledPrice(label='PRO', amount=199*100)] #Цена в копейках
        self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        self.bot.send_invoice(chat_id=message.chat.id, title='PRO',
            description="Безлимитная генерация текста (в том числе по готовым промптам) и изображений.",
            invoice_payload='pro_invoice_payload',
            start_parameter='subscription',
            provider_token=os.environ['PROVIDE_TOKEN'],
            currency='RUB', prices=price, reply_markup=keyboard)

    # One text processing
    def TextCommands(self, message: telebot.types.Message, ind: int) -> Tuple[int, int, int]:
        """
        Обрабатывает текстовые команды.

        Args:
            message (telebot.types.Message): Объект сообщения Telegram.
            ind (int): Индекс команды.

        Returns:
            Tuple[int, int, int]: Кортеж, содержащий количество входящих и исходящих токенов, и 1.
        """
        info: List[str] = []
        incoming_tokens: int = 0
        outgoing_tokens: int = 0
        response: Optional[Dict] = None
        if 'TEXT' in pc.commands_size[ind]:
            info.append(message.text)
            msg: telebot.types.Message = self.bot.send_message(chat_id=message.chat.id, text=self.prompts_text['text_list'][ind][1])

            def Text_next_step(message: telebot.types.Message) -> None:
                """
                Следующий шаг обработки текста.

                Args:
                    message (telebot.types.Message): Объект сообщения Telegram.
                """
                nonlocal info, incoming_tokens, outgoing_tokens, response
                info += message.text.split(';')
                while len(info) < len(pc.commands_size[ind]):
                    info.append("Параметр отсутствует")
                prompt: str = pc.get_prompt(ind=ind, info=info)
                response, incoming_tokens, outgoing_tokens = self.__gpt_4o_mini(prompt=[{ "role": "user", "content": prompt }], message=message)
                self.restart(message)
            self.bot.register_next_step_handler(msg, Text_next_step)
            while response is None:
                time.sleep(0.5)
            return incoming_tokens, outgoing_tokens, 1
        else:
            info = message.text.split(';')
            while len(info) < len(pc.commands_size[ind]):
                info.append("Параметр отсутствует")
            prompt = pc.get_prompt(ind=ind, info=info)
            response, incoming_tokens, outgoing_tokens = self.__gpt_4o_mini(prompt=[{ "role": "user", "content": prompt }], message=message)
            self.restart(message)
            return incoming_tokens, outgoing_tokens, 1

    # Some texts processing
    def SomeTextsCommand(self, message: telebot.types.Message, ind: int, tokens: Dict[str, int]) -> Tuple[int, int, int]:
        """
        Обрабатывает несколько текстовых команд.

        Args:
            message (telebot.types.Message): Объект сообщения Telegram.
            ind (int): Индекс команды.
            tokens (Dict[str, int]): Словарь токенов.

        Returns:
            Tuple[int, int, int]: Кортеж, содержащий количество входящих и исходящих токенов, и количество текстов.
        """
        n: int = int(message.text)
        avalib: List[int] = [0, 1, 3, 5, 6]
        ans: List[List[str]] = []

        for i in range(n):
            ans.append([])
            if "TEXT" in pc.commands_size[ind]:
                msg: telebot.types.Message = self.bot.send_message(chat_id=message.chat.id, text=f"Введите текст источника {i+1}")
                text: Optional[str] = None

                def Text_next_step(message: telebot.types.Message) -> None:
                    """
                    Следующий шаг обработки текста.

                    Args:
                        message (telebot.types.Message): Объект сообщения Telegram.
                    """
                    nonlocal text, ans
                    text = message.text
                    ans[i].append(text)
                self.bot.register_next_step_handler(msg, Text_next_step)
                while text is None:
                    time.sleep(0.5)

        index: int = avalib.index(ind)
        for el in range(1, len(self.prompts_text["few_texts_list"][index])):
            msg = self.bot.send_message(chat_id=message.chat.id, text=self.prompts_text["few_texts_list"][index][el])
            params: Optional[str] = None

            def Params_addition(message: telebot.types.Message) -> None:
                """
                Добавляет параметры.

                Args:
                    message (telebot.types.Message): Объект сообщения Telegram.
                """
                nonlocal params, ans
                params = message.text
                params = params.split(';')
                if len(params) < len(pc.commands_size[ind]):
                    while len(params) < len(pc.commands_size[ind]):
                        params.append(None)
                param = params[0]
                [ans[i].append(param) if params[i] is None else ans[i].append(params[i]) for i in range(len(ans))]
            self.bot.register_next_step_handler(msg, Params_addition)
            while params is None:
                time.sleep(0.5)

        incoming_tokens = 0
        outgoing_tokens = 0

        def process_prompt(i: int) -> Tuple[int, int]:
            """
            Обрабатывает промпт.

            Args:
                i (int): Индекс промпта.

            Returns:
                Tuple[int, int]: Кортеж, содержащий количество входящих и исходящих токенов.
            """
            nonlocal incoming_tokens, outgoing_tokens
            prompt = pc.get_prompt(ind=ind, info=ans[i])
            if tokens['incoming_tokens'] - incoming_tokens > 0 and tokens['outgoing_tokens'] - outgoing_tokens > 0 or tokens['free_requests'] - i > 0:
                response, in_tokens, out_tokens = self.__gpt_4o_mini(prompt=[{"role": "user", "content": prompt}], message=message)
                return in_tokens, out_tokens
            return 0, 0

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(process_prompt, range(n)))

        for in_tokens, out_tokens in results:
            incoming_tokens += in_tokens
            outgoing_tokens += out_tokens

        self.restart(message)
        return incoming_tokens, outgoing_tokens, n

    # Images processing
    def ImageCommand(self, message: telebot.types.Message, prompt: str, size: List[int]) -> int:
        """
        Обрабатывает команду для генерации изображений.

        Args:
            message (telebot.types.Message): Объект сообщения Telegram.
            prompt (str): Промпт для генерации изображения.
            size (List[int]): Размер изображения.

        Returns:
            int: Зерно для генерации изображения.
        """
        seed: int = randint(1, 1000000)
        self.__FLUX_schnell(prompt=prompt, size=size, message=message, seed=seed, num_inference_steps=4)
        self.ImageChange(message)
        return seed

    # Image regeneration and upscaling
    def Image_Regen_And_Upscale(self, message: telebot.types.Message, prompt: str, size: List[int], seed: int, num_inference_steps: int = 4) -> None:
        """
        Обрабатывает регенерацию и увеличение изображения.

        Args:
            message (telebot.types.Message): Объект сообщения Telegram.
            prompt (str): Промпт для генерации изображения.
            size (List[int]): Размер изображения.
            seed (int): Зерно для генерации изображения.
            num_inference_steps (int, optional): Количество шагов для генерации. По умолчанию 4.
        """
        return self.__FLUX_schnell(prompt=prompt, size=size, message=message, seed=seed, num_inference_steps=num_inference_steps)

    # Free mode processing
    def FreeCommand(self, message: telebot.types.Message, prompts: List[Dict[str, str]]) -> Tuple[int, int, List[Dict[str, str]]]:
        """
        Обрабатывает команду для свободного режима.

        Args:
            message (telebot.types.Message): Объект сообщения Telegram.
            prompts (List[Dict[str, str]]): Список промптов.

        Returns:
            Tuple[int, int, List[Dict[str, str]]]: Кортеж, содержащий количество входящих и исходящих токенов, и список промптов.
        """
        try:
            if type(prompts[-1].get('content', False)) != list:
                prompts.append({"content": message.text, "role": "user"})
        except Exception as ex:
            logger.error('Error while processing FreeCommand', ex, exc_info=True)
            pass
        response, incoming_tokens, outgoing_tokens = self.__gpt_4o_mini(prompt=prompts, message=message)
        prompts.append(response)
        return incoming_tokens, outgoing_tokens, prompts