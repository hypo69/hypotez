### **Анализ кода модуля `ToolBox_requests.py`**

**Расположение файла в проекте:** `hypotez/src/endpoints/bots/telegram/ToolBoxbot-main/ToolBox/ToolBox_requests.py`

**Назначение модуля:** Модуль содержит основной функционал для обработки запросов от Telegram-бота, включая обработку текста, изображений и тарифных планов.

**Описание структуры:**

*   Модуль включает импорты необходимых библиотек, таких как `telebot`, `os`, `json`, `concurrent.futures`, `time`, `base64`, `random`.
*   Используются классы `PromptsCompressor` и `keyboards` из `BaseSettings.AuxiliaryClasses`.
*   Используется класс `neural_networks` из `ToolBox_n_networks`.
*   Определен класс `ToolBox`, который наследует `keyboards` и `neural_networks`. Этот класс содержит основные методы для обработки запросов от пользователей Telegram-бота.

**Качество кода:**

*   **Соответствие стандартам**: 6/10
*   **Плюсы**:
    *   Код разбит на функции и классы, что улучшает читаемость.
    *   Используется наследование для повторного использования функциональности.
    *   Присутствуют комментарии, объясняющие некоторые части кода.
*   **Минусы**:
    *   Не все функции и методы имеют docstring.
    *   Используются lambda-функции для определения методов класса, что ухудшает читаемость.
    *   Не используются аннотации типов для параметров и возвращаемых значений функций.
    *   Не везде используется логирование ошибок.
    *   Некоторые участки кода выглядят сложными и требуют упрощения.
    *   Не все комментарии достаточно информативны.
    *   Многочисленные лямбда-функции усложняют понимание кода.

**Рекомендации по улучшению:**

1.  **Добавить docstring для всех функций и методов.** Docstring должен содержать описание назначения функции, аргументов, возвращаемых значений и возможных исключений.
2.  **Заменить lambda-функции на обычные функции.** Это улучшит читаемость и позволит добавить docstring для каждой функции.
3.  **Добавить аннотации типов для параметров и возвращаемых значений функций.** Это улучшит читаемость и позволит статическим анализаторам кода проверять типы.
4.  **Добавить логирование ошибок.** Это поможет отлаживать код и выявлять проблемы.
5.  **Упростить сложные участки кода.** Разбить сложные функции на более мелкие и простые.
6.  **Улучшить информативность комментариев.** Комментарии должны объяснять назначение кода и логику его работы.
7.  **Использовать более осмысленные имена переменных и функций.**
8.  **Заменить множественное использование `self` в lambda-функциях на переменные, передаваемые как параметры.** Это сделает код более читаемым и понятным.
9.  **Перевести все комментарии и docstring на русский язык.**
10. **Изменить способ открытия JSON файлов. Использовать `j_loads`**

**Оптимизированный код:**

```python
import telebot
import os
import json
import concurrent.futures
import time
import base64
from random import randint
from telebot import types
from BaseSettings.AuxiliaryClasses import PromptsCompressor, keyboards
from ToolBox_n_networks import neural_networks
from src.logger import logger  # Добавлен импорт logger
from typing import List, Optional, Dict, Tuple, Callable, Any

# Class initialization
pc = PromptsCompressor()

# Main functions class
class ToolBox(keyboards, neural_networks):
    def __init__(self):
        """
        Инициализация класса ToolBox.

        Args:
            None

        Returns:
            None
        """
        # Start buttons
        self.name: List[str] = ["Текст 📝", "Изображения 🎨", "Свободный режим 🗽", "Тарифы 💸"]
        self.data: List[str] = ["text", "images", "free", "tariff"]

        # Promts texts load
        self.prompts_text: Dict[str, Any] = j_loads("ToolBox/BaseSettings/prompts.json") #Используем j_loads

        # Telegram bot initialization
        self.bot: telebot.TeleBot = telebot.TeleBot(token=os.environ['TOKEN'])
        # Inline keyboard blank lambda
        self.keyboard_blank: Callable[[Any, List[str], List[str]], types.InlineKeyboardMarkup] = lambda self, name, data: super()._keyboard_two_blank(data, name)
        # Markup keyboard
        self.reply_keyboard: Callable[[Any, List[str]], types.ReplyKeyboardMarkup] = lambda self, name: super()._reply_keyboard(name)
        # Request delay
        self.__delay: Callable[[Any], Any] = lambda message, self=self: self.bot.send_message(message.chat.id, "Подождите, это должно занять несколько секунд . . .", parse_mode='html')
        # Start request
        self.start_request: Callable[[Any], Any] = lambda message, self=self: self.bot.send_message(message.chat.id, self.prompts_text['hello'], reply_markup=self.keyboard_blank(self, self.name, self.data), parse_mode='html')
        # Restart request
        self.restart: Callable[[Any], Any] = lambda message, self=self: self.bot.send_message(message.chat.id, "Выберите нужную вам задачу", reply_markup=self.keyboard_blank(self, self.name, self.data), parse_mode='html')
        # Restart murkup
        self.restart_markup: Callable[[Any], Any] = lambda message, self=self: self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Выберите нужную вам задачу", reply_markup=self.keyboard_blank(self, self.name, self.data), parse_mode='html')
        # One text request
        self.OneTextArea: Callable[[Any, int], Any] = lambda message, ind, self=self: self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=self.prompts_text['text_list'][ind] if type(self.prompts_text['text_list'][ind]) == str else self.prompts_text['text_list'][ind][0], reply_markup=self.keyboard_blank(self, ["Назад"], ["text_exit"]))
        # Some texts request
        self.SomeTextsArea: Callable[[Any, int], Any] = lambda message, ind, self=self: self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=self.prompts_text['few_texts_list'][ind][0], reply_markup=self.keyboard_blank(self, ["Назад"], ["text_exit"]))
        # Image size
        self.ImageSize: Callable[[Any], Any] = lambda message, self=self: self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Выберите разрешение изображения", reply_markup=self.keyboard_blank(self, ["9:16", "1:1", "16:9", "В меню"], ["576x1024", "1024x1024", "1024x576", "exit"]), parse_mode='html')
        # Image request
        self.ImageArea: Callable[[Any], Any] = lambda message, self=self: self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Введите ваш запрос для изображений 🖼", reply_markup=self.keyboard_blank(self, ["В меню"], ["exit"]), parse_mode='html')
        # Image change
        self.ImageChange: Callable[[Any], Any] = lambda message, self=self: self.bot.send_message(chat_id=message.chat.id, text="Выберите следующее действие", reply_markup=self.keyboard_blank(self, ["Улучшить 🪄", "🔁", "Новая 🖼", "В меню"], ["upscale", "regenerate", "images", "exit"]), parse_mode='html')
        # Message before upscale
        self.BeforeUpscale: Callable[[Any], Any] = lambda message, self=self: self.bot.send_message(chat_id=message.chat.id, text="Выберите следующее действие", reply_markup=self.keyboard_blank(self, ["🔁", "Новая 🖼", "В меню"], ["regenerate", "images", "exit"]), parse_mode='html')
        # Free mode request
        self.FreeArea: Callable[[Any], Any] = lambda message, self=self: self.bot.send_message(chat_id=message.chat.id, text="Введите ваш запрос", reply_markup=self.reply_keyboard(self, ["В меню"]), parse_mode='html')
        # Tariff request
        self.TariffArea: Callable[[Any], Any] = lambda message, self=self: self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Тарифы", reply_markup=self.keyboard_blank(self, ["BASIC", "PRO", "Промокод", "Реферальная программа", "В меню"], ["basic", "pro", "promo", "ref", "exit"]))
        # Tariffs area exit
        self.TariffExit: Callable[[Any], Any] = lambda message, self=self: self.bot.send_message(chat_id=message.chat.id, text="Тарифы", reply_markup=self.keyboard_blank(self, ["BASIC", "PRO", "Промокод", "В меню"], ["basic", "pro", "promo", "exit"]))
        # End tariff
        self.TarrifEnd: Callable[[Any], Any] = lambda message, self=self: self.bot.send_message(chat_id=message.chat.id, text="У вас закончились запросы, но вы можете продлить ваш тариф.", reply_markup=self.keyboard_blank(self, ["BASIC", "PRO", "Промокод", "Реферальная программа", "В меню"], ["basic", "pro", "promo", "ref", "exit"]))
        # Free tariff end
        self.FreeTariffEnd: Callable[[Any], Any] = lambda message, self=self: self.bot.send_message(chat_id=message.chat.id, text="Лимит бесплатных запросов, увы, исчерпан😢 Но вы можете выбрать один из наших платных тарифов. Просто нажмите на них и получите подробное описание", reply_markup=self.keyboard_blank(self, ["BASIC", "PRO", "Промокод", "Реферальная программа", "В меню"], ["basic", "pro", "promo", "ref", "exit"]))
        # Select one or some texts
        self.SomeTexts: Callable[[Any, int], Any] = lambda message, ind, self=self: self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Хотите сделать один текст или сразу несколько?", reply_markup=self.keyboard_blank(self, ["Один", "Несколько", "Назад"], [f"one_{ind}", f"some_{ind}", "text_exit"]))

    # Private
    # GPT 4o mini processing
    def __gpt_4o_mini(self, prompt: List[Dict[str, str]], message) -> Tuple[Dict[str, str], int, int]:
        """
        Обработка запроса к GPT 4o mini.

        Args:
            prompt (List[Dict[str, str]]): Список промптов.
            message: Объект сообщения Telegram.

        Returns:
            Tuple[Dict[str, str], int, int]: Ответ, количество входящих и исходящих токенов.
        """
        send = self.__delay(message)
        response, incoming_tokens, outgoing_tokens = super()._free_gpt_4o_mini(prompt=prompt)
        self.bot.edit_message_text(chat_id=send.chat.id, message_id=send.message_id, text=PromptsCompressor.html_tags_insert(response['content']), parse_mode='html')
        return response, incoming_tokens, outgoing_tokens

    # FLUX schnell processing
    def __FLUX_schnell(self, prompt: str, size: List[int], message, seed: int, num_inference_steps: int) -> None:
        """
        Обработка запроса к FLUX schnell.

        Args:
            prompt (str): Промпт.
            size (List[int]): Размер изображения.
            message: Объект сообщения Telegram.
            seed (int): Зерно для генерации.
            num_inference_steps (int): Количество шагов для генерации.

        Returns:
            None
        """
        send = self.__delay(message)
        while True:
            try:
                photo = super()._FLUX_schnell(prompt, size, seed, num_inference_steps)
            except Exception as ex:  # Используем ex вместо e
                logger.error('Ошибка при обработке FLUX schnell', ex, exc_info=True)  # Логируем ошибку
                continue
            else:
                break
        if photo:
            self.bot.send_photo(chat_id=message.chat.id, photo=photo)
            return self.bot.delete_message(chat_id=send.chat.id, message_id=send.message_id)
        self.bot.edit_message_text(chat_id=send.chat.id, message_id=send.message_id, text="При генерации возникла ошибка, попробуйте повторить позже")

    # Public
    # Text types
    def Text_types(self, message) -> None:
        """
        Обработка запроса на выбор типа текста.

        Args:
            message: Объект сообщения Telegram.

        Returns:
            None
        """
        name = ["Коммерческий  🛍️", "SMM 📱", "Брейншторм 💡", "Реклама 📺", "Заголовки 🔍", "SEO 🌐", "Новость 📰", "Редактура 📝", "В меню"]
        data = ["comm-text", "smm-text", "brainst-text", "advertising-text", "headlines-text", "seo-text", "news", "editing", "exit"]
        return self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="📝 Выберите тип текста", reply_markup=self.keyboard_blank(self, name, data))

    # Tariffs
    # Basic tariff
    def Basic_tariff(self, message) -> None:
        """
        Обработка запроса на подключение базового тарифа.

        Args:
            message: Объект сообщения Telegram.

        Returns:
            None
        """
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Подключить тариф BASIC", pay=True))
        keyboard.add(types.InlineKeyboardButton("К тарифам", callback_data="tariff_exit"))
        price = [types.LabeledPrice(label='BASIC', amount=99 * 100)]
        self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        self.bot.send_invoice(chat_id=message.chat.id, title='BASIC',
                            description="Безлимитная генерация текста, в том числе по готовым промптам.",
                            invoice_payload='basic_invoice_payload',
                            start_parameter='subscription',
                            provider_token=os.environ['PROVIDE_TOKEN'],
                            currency='RUB', prices=price, reply_markup=keyboard)

    # Pro tariff
    def Pro_tariff(self, message) -> None:
        """
        Обработка запроса на подключение профессионального тарифа.

        Args:
            message: Объект сообщения Telegram.

        Returns:
            None
        """
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Подключить тариф PRO", pay=True))
        keyboard.add(types.InlineKeyboardButton("К тарифам", callback_data="tariff_exit"))
        price = [types.LabeledPrice(label='PRO', amount=199 * 100)]
        self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        self.bot.send_invoice(chat_id=message.chat.id, title='PRO',
                            description="Безлимитная генерация текста (в том числе по готовым промптам) и изображений.",
                            invoice_payload='pro_invoice_payload',
                            start_parameter='subscription',
                            provider_token=os.environ['PROVIDE_TOKEN'],
                            currency='RUB', prices=price, reply_markup=keyboard)

    # One text processing
    def TextCommands(self, message, ind: int) -> Tuple[int, int, int]:
        """
        Обработка текстовых команд.

        Args:
            message: Объект сообщения Telegram.
            ind (int): Индекс команды.

        Returns:
            Tuple[int, int, int]: Количество входящих и исходящих токенов, а также количество обработанных текстов.
        """
        info = []
        incoming_tokens = 0
        outgoing_tokens = 0
        response = None
        if 'TEXT' in pc.commands_size[ind]:
            info.append(message.text)
            msg = self.bot.send_message(chat_id=message.chat.id, text=self.prompts_text['text_list'][ind][1])

            def Text_next_step(message):
                """
                Обработка следующего шага для текстовой команды.

                Args:
                    message: Объект сообщения Telegram.

                Returns:
                    None
                """
                nonlocal info, incoming_tokens, outgoing_tokens, response
                info += message.text.split(';')
                while len(info) < len(pc.commands_size[ind]):
                    info.append("Параметр отсутствует")
                prompt = pc.get_prompt(ind=ind, info=info)
                response, incoming_tokens, outgoing_tokens = self.__gpt_4o_mini(prompt=[{"role": "user", "content": prompt}], message=message)
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
            response, incoming_tokens, outgoing_tokens = self.__gpt_4o_mini(prompt=[{"role": "user", "content": prompt}], message=message)
            self.restart(message)
            return incoming_tokens, outgoing_tokens, 1

    # Some texts processing
    def SomeTextsCommand(self, message, ind: int, tokens: Dict[str, int]) -> Tuple[int, int, int]:
        """
        Обработка нескольких текстовых команд.

        Args:
            message: Объект сообщения Telegram.
            ind (int): Индекс команды.
            tokens (Dict[str, int]): Словарь с количеством токенов.

        Returns:
            Tuple[int, int, int]: Количество входящих и исходящих токенов, а также количество обработанных текстов.
        """
        n = int(message.text)
        avalib = [0, 1, 3, 5, 6]
        ans = []

        for i in range(n):
            ans.append([])
            if "TEXT" in pc.commands_size[ind]:
                msg = self.bot.send_message(chat_id=message.chat.id, text=f"Введите текст источника {i+1}")
                text = None

                def Text_next_step(message):
                    """
                    Обработка следующего шага для ввода текста.

                    Args:
                        message: Объект сообщения Telegram.

                    Returns:
                        None
                    """
                    nonlocal text, ans
                    text = message.text
                    ans[i].append(text)

                self.bot.register_next_step_handler(msg, Text_next_step)
                while text is None:
                    time.sleep(0.5)

        index = avalib.index(ind)
        for el in range(1, len(self.prompts_text["few_texts_list"][index])):
            msg = self.bot.send_message(chat_id=message.chat.id, text=self.prompts_text["few_texts_list"][index][el])
            params = None

            def Params_addition(message):
                """
                Добавление параметров для обработки текста.

                Args:
                    message: Объект сообщения Telegram.

                Returns:
                    None
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

        def process_prompt(i):
            """
            Обработка промпта для одного текста.

            Args:
                i (int): Индекс текста.

            Returns:
                Tuple[int, int]: Количество входящих и исходящих токенов.
            """
            nonlocal incoming_tokens, outgoing_tokens
            prompt = pc.get_prompt(ind=ind, info=ans[i])
            if tokens['incoming_tokens'] - incoming_tokens > 0 and tokens['outgoing_tokens'] - outgoing_tokens > 0 or tokens['free_requests'] - i > 0:
                try:
                    response, in_tokens, out_tokens = self.__gpt_4o_mini(prompt=[{"role": "user", "content": prompt}], message=message)
                except Exception as ex:
                    logger.error("Ошибка при обработке промпта", ex, exc_info=True)
                    return 0, 0
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
    def ImageCommand(self, message, prompt: str, size: List[int]) -> int:
        """
        Обработка команды для генерации изображений.

        Args:
            message: Объект сообщения Telegram.
            prompt (str): Промпт для генерации изображения.
            size (List[int]): Размер изображения.

        Returns:
            int: Зерно для генерации изображения.
        """
        seed = randint(1, 1000000)
        self.__FLUX_schnell(prompt=prompt, size=size, message=message, seed=seed, num_inference_steps=4)
        self.ImageChange(message)
        return seed

    # Image regeneration and upscaling
    def Image_Regen_And_Upscale(self, message, prompt: str, size: List[int], seed: int, num_inference_steps: int = 4) -> None:
        """
        Обработка команды для регенерации и увеличения изображения.

        Args:
            message: Объект сообщения Telegram.
            prompt (str): Промпт для генерации изображения.
            size (List[int]): Размер изображения.
            seed (int): Зерно для генерации изображения.
            num_inference_steps (int): Количество шагов для генерации.

        Returns:
            None
        """
        return self.__FLUX_schnell(prompt=prompt, size=size, message=message, seed=seed, num_inference_steps=num_inference_steps)

    # Free mode processing
    def FreeCommand(self, message, prompts: List[Dict[str, str]]) -> Tuple[int, int, List[Dict[str, str]]]:
        """
        Обработка команды для свободного режима.

        Args:
            message: Объект сообщения Telegram.
            prompts (List[Dict[str, str]]): Список промптов.

        Returns:
            Tuple[int, int, List[Dict[str, str]]]: Количество входящих и исходящих токенов, а также обновленный список промптов.
        """
        try:
            if type(prompts[-1].get('content', False)) != list:
                prompts.append({"content": message.text, "role": "user"})
        except Exception as ex:
            logger.error("Ошибка при обработке FreeCommand", ex, exc_info=True)
            pass
        response, incoming_tokens, outgoing_tokens = self.__gpt_4o_mini(prompt=prompts, message=message)
        prompts.append(response)
        return incoming_tokens, outgoing_tokens, prompts