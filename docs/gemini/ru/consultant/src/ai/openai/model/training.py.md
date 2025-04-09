### **Анализ кода модуля `training.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Использование `logger` для логирования.
  - Четкая структура классов и функций.
  - Наличие docstring для большинства функций и методов.
  - Использование `j_loads` и `j_dumps` для работы с JSON-файлами.
- **Минусы**:
  - Docstring не все переведены на русский язык.
  - Не все переменные аннотированы типами.
  - В некоторых местах используется английский язык в комментариях.
  - Не хватает примеров использования в docstring.
  - В блоках `try-except` не всегда обрабатываются исключения с использованием `logger.error(..., ex, exc_info=True)`.
  - Не везде используется `ex` вместо `e` в блоках `except`.

#### **Рекомендации по улучшению**:

1. **Документация**:
   - Перевести все docstring на русский язык.
   - Добавить примеры использования для каждой функции и класса.
   - Уточнить и расширить описания параметров и возвращаемых значений.

2. **Типизация**:
   - Добавить аннотации типов для всех переменных, где это возможно.

3. **Обработка исключений**:
   - Убедиться, что все исключения обрабатываются с использованием `logger.error(..., ex, exc_info=True)`.
   - Использовать `ex` вместо `e` в блоках `except`.

4. **Логирование**:
   - Добавить больше информативных сообщений в логи.
   - Проверить, чтобы логирование ошибок было полным и содержало всю необходимую информацию для отладки.

5. **Использование констант**:
   - Вынести строковые литералы (например, имена моделей) в константы.

6. **Комментарии**:
   - Убедиться, что все комментарии актуальны и полезны.
   - Избегать общих фраз типа "получаем" или "делаем", а использовать более конкретные: "извлекаем", "проверяем", "выполняем".
   - Документировать все внутренние функции.

#### **Оптимизированный код**:

```python
                
## \file /src/ai/openai/model/training.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для работы с OpenAI API и управления моделями.
========================================================

Модуль содержит класс :class:`OpenAIModel`, который используется для взаимодействия с OpenAI API и управления моделями,
включая их обучение и настройку.
"""

import time
from pathlib import Path
from types import SimpleNamespace
from typing import List, Dict, Optional
import pandas as pd
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

from src import gs
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.csv import save_csv_file  
from src.utils.printer import pprint
from src.utils.convertors.base64 import base64encode
from src.utils.convertors.md import md2dict
from src.logger.logger import logger

class OpenAIModel:
    """
    Класс для взаимодействия с OpenAI API и управления моделями.
    """

    model: str = 'gpt-4o-mini'
    #model: str = "gpt-4o-2024-08-06"
    client: OpenAI
    current_job_id: str
    assistant_id: str 
    assistant = None
    thread = None
    system_instruction: str
    dialogue_log_path: str | Path = gs.path.google_drive / 'AI' / f"{model}_{gs.now}.json"
    dialogue: List[Dict[str, str]] = []
    assistants: List[SimpleNamespace]
    models_list: List[str]

    def __init__(self, api_key: str, system_instruction: str = None, model_name: str = 'gpt-4o-mini', assistant_id: str = None) -> None:
        """
        Инициализирует объект Model с API-ключом, ID ассистента и загружает доступные модели и ассистенты.

        Args:
            api_key (str): API-ключ OpenAI.
            system_instruction (str, optional): Системная инструкция для модели. По умолчанию `None`.
            model_name (str, optional): Имя модели. По умолчанию `'gpt-4o-mini'`.
            assistant_id (str, optional): ID ассистента. По умолчанию `None`.
        """
        # self.client = OpenAI(api_key = gs.credentials.openai.project_api)
        self.client = OpenAI(api_key = api_key if api_key else gs.credentials.openai.api_key)
        self.current_job_id = None
        self.assistant_id = assistant_id or gs.credentials.openai.assistant_id.code_assistant
        self.system_instruction = system_instruction

        # Загрузка ассистента и потока при инициализации
        self.assistant = self.client.beta.assistants.retrieve(self.assistant_id)
        self.thread = self.client.beta.threads.create()

    @property
    def list_models(self) -> List[str]:
        """
        Динамически получает и возвращает доступные модели из OpenAI API.

        Returns:
            List[str]: Список ID моделей, доступных через OpenAI API.
        """
        try:
            models = self.client.models.list()
            model_list = [model['id'] for model in models['data']]
            logger.info(f"Загружены модели: {model_list}")
            return model_list
        except Exception as ex:
            logger.error("Произошла ошибка при загрузке моделей:", ex, exc_info=True)
            return []

    @property
    def list_assistants(self) -> List[str]:
        """
        Динамически загружает доступных ассистентов из JSON-файла.

        Returns:
            List[str]: Список имен ассистентов.
        """
        try:
            self.assistants = j_loads_ns(gs.path.src / 'ai' / 'openai' / 'model' / 'assistants' / 'assistants.json')
            assistant_list = [assistant.name for assistant in self.assistants]
            logger.info(f"Загружены ассистенты: {assistant_list}")
            return assistant_list
        except Exception as ex:
            logger.error("Произошла ошибка при загрузке ассистентов:", ex, exc_info=True)
            return []

    def set_assistant(self, assistant_id: str) -> None:
        """
        Устанавливает ассистента, используя предоставленный ID ассистента.

        Args:
            assistant_id (str): ID ассистента для установки.
        """
        try:
            self.assistant_id = assistant_id
            self.assistant = self.client.beta.assistants.retrieve(assistant_id)
            logger.info(f"Ассистент успешно установлен: {assistant_id}")
        except Exception as ex:
            logger.error("Произошла ошибка при установке ассистента:", ex, exc_info=True)

    def _save_dialogue(self) -> None:
        """
        Сохраняет весь диалог в JSON-файл.
        """
        j_dumps(self.dialogue, self.dialogue_log_path)

    def determine_sentiment(self, message: str) -> str:
        """
        Определяет тональность сообщения (положительную, отрицательную или нейтральную).

        Args:
            message (str): Сообщение для анализа.

        Returns:
            str: Тональность ('positive', 'negative' или 'neutral').
        """
        positive_words = ["good", "great", "excellent", "happy", "love", "wonderful", "amazing", "positive"]
        negative_words = ["bad", "terrible", "hate", "sad", "angry", "horrible", "negative", "awful"]
        neutral_words = ["okay", "fine", "neutral", "average", "moderate", "acceptable", "sufficient"]

        message_lower = message.lower()

        if any(word in message_lower for word in positive_words):
            return "positive"
        elif any(word in message_lower for word in negative_words):
            return "negative"
        elif any(word in message_lower for word in neutral_words):
            return "neutral"
        else:
            return "neutral"

    def ask(self, message: str, system_instruction: str = None, attempts: int = 3) -> str | None:
        """
        Отправляет сообщение модели и возвращает ответ вместе с анализом тональности.

        Args:
            message (str): Сообщение для отправки модели.
            system_instruction (str, optional): Системная инструкция. По умолчанию `None`.
            attempts (int, optional): Количество попыток повтора. По умолчанию 3.

        Returns:
            str | None: Ответ от модели или `None` в случае ошибки.
        """
        try:
            messages = []
            if self.system_instruction or system_instruction:
                system_instruction_escaped = (system_instruction or self.system_instruction).replace('"', r'\"')
                messages.append({"role": "system", "content": system_instruction_escaped})

            message_escaped = message.replace('"', r'\"')
            messages.append({
                            "role": "user", 
                             "content": message_escaped
                             })

            # Отправка запроса к модели
            response = self.client.chat.completions.create(
                model = self.model,
                
                messages = messages,
                temperature = 0,
                max_tokens=8000,
            )
            reply = response.choices[0].message.content.strip()

            # Анализ тональности
            sentiment = self.determine_sentiment(reply)

            # Добавление сообщений и тональности в диалог
            self.dialogue.append({"role": "system", "content": system_instruction or self.system_instruction})
            self.dialogue.append({"role": "user", "content": message_escaped})
            self.dialogue.append({"role": "assistant", "content": reply, "sentiment": sentiment})

            # Сохранение диалога
            self._save_dialogue()

            return reply
        except Exception as ex:
            logger.error(f"Произошла ошибка при отправке сообщения: \n-----\n {pprint(messages)} \n-----\n", ex, exc_info=True)
            time.sleep(3)
            if attempts > 0:
                return self.ask(message, attempts - 1)
            return None

    def describe_image(self, image_path: str | Path, prompt:Optional[str] = None, system_instruction:Optional[str] = None ) -> str | None:
        """
        Описывает изображение, используя OpenAI API.
        
        Args:
            image_path (str | Path): Путь к файлу изображения.
            prompt (Optional[str], optional): Дополнительный запрос для описания изображения. По умолчанию `None`.
            system_instruction (Optional[str], optional): Системная инструкция для модели. По умолчанию `None`.

        Returns:
            str | None: Описание изображения или `None` в случае ошибки.
        """
        ...
        
        messages:list = []
        base64_image = base64encode(image_path)

        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})

        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": prompt if prompt else "What's in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    },
                ],
            }
        )
        try:
            response = self.client.chat.completions.create(
                    model = self.model,
                    messages = messages,
                    temperature = 0,
                    max_tokens=800,
                )
        
            reply = response
            ...
            try:
                raw_reply = response.choices[0].message.content.strip()
                return j_loads_ns(raw_reply)
            except Exception as ex:
                logger.error(f"Ошибка в ответе {response}", ex, exc_info=True)
                ...
                return None

        except Exception as ex:
            logger.error(f"Ошибка openai", ex, exc_info=True)
            ...
            return None

    def describe_image_by_requests(self, image_path: str | Path, prompt:str = None) -> None:
        """
        Отправляет изображение в OpenAI API и получает описание, используя requests.

        Args:
            image_path (str | Path): Путь к файлу изображения.
            prompt (str, optional): Дополнительный запрос для описания изображения. По умолчанию `None`.
        """
        # Getting the base64 string
        base64_image = base64encode(image_path)

        headers = {
          "Content-Type": "application/json",
          "Authorization": f"Bearer {gs.credentials.openai.project_api}"
        }

        payload = {
          "model": "gpt-4o",
          "messages": [
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": prompt if prompt else "What’s in this image?"
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                  }
                }
              ]
            }
          ],
          "max_tokens": 300
        }
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            response_json = response.json()
            ...
        except Exception as ex:
            logger.error(f"Ошибка в описании изображения {image_path=}\n", ex, exc_info=True)


    def dynamic_train(self) -> None:
        """
        Динамически загружает предыдущий диалог и дообучает модель на его основе.
        """
        try:
            messages = j_loads(gs.path.google_drive / 'AI' / 'conversation' / 'dailogue.json')

            if messages:
                response = self.client.chat.completions.create(
                    model=self.model,
                    assistant=self.assistant_id,
                    messages=messages,
                    temperature=0,
                )
                logger.info("Дообучение во время разговора прошло успешно.")
            else:
                logger.info("Предыдущий диалог для дообучения не найден.")
        except Exception as ex:
            logger.error(f"Ошибка во время динамического дообучения: {ex}", exc_info=True)

    def train(self, data: str = None, data_dir: Path | str = None, data_file: Path | str = None, positive: bool = True) -> str | None:
        """
        Обучает модель на указанных данных или директории.

        Args:
            data (str, optional): Путь к CSV-файлу или CSV-форматированная строка с данными.
            data_dir (Path | str, optional): Директория, содержащая CSV-файлы для обучения.
            data_file (Path | str, optional): Путь к одному CSV-файлу с данными для обучения.
            positive (bool, optional): Указывает, являются ли данные положительными или отрицательными. По умолчанию `True`.

        Returns:
            str | None: ID задания на обучение или `None`, если произошла ошибка.
        """
        if not data_dir:
            data_dir = gs.path.google_drive / 'AI' / 'training'

        try:
            documents = j_loads(data if data else data_file if data_file else data_dir)

            response = self.client.Training.create(
                model=self.model,
                documents=documents,
                labels=["positive" if positive else "negative"] * len(documents),
                show_progress=True
            )
            self.current_job_id = response.id
            return response.id

        except Exception as ex:
            logger.error("Произошла ошибка во время обучения:", ex, exc_info=True)
            return None

    def save_job_id(self, job_id: str, description: str, filename: str = "job_ids.json") -> None:
        """
        Сохраняет ID задания с описанием в файл.

        Args:
            job_id (str): ID задания для сохранения.
            description (str): Описание задания.
            filename (str, optional): Имя файла для сохранения ID заданий. По умолчанию "job_ids.json".
        """
        job_data = {"id": job_id, "description": description, "created": time.time()}
        job_file = gs.path.google_drive / filename

        if not job_file.exists():
            j_dumps([job_data], job_file)
        else:
            existing_jobs = j_loads(job_file)
            existing_jobs.append(job_data)
            j_dumps(existing_jobs, job_file)

def main() -> None:
    """
    Главная функция для инициализации OpenAIModel и демонстрации использования.

    Описание:
        Инициализация модели:

        OpenAIModel инициализируется с системной инструкцией и ID ассистента (необязательно). Вы можете изменить параметры при необходимости.
        Просмотр списка моделей и ассистентов:

        Методы list_models и list_assistants вызываются для вывода доступных моделей и ассистентов.
        Запрос модели:

        Метод ask() используется для отправки сообщения модели и получения ее ответа.
        Динамическое обучение:

        Метод dynamic_train() выполняет динамическую донастройку на основе прошлого диалога.
        Обучение модели:

        Метод train() обучает модель, используя данные из указанного файла (в данном случае 'training_data.csv').
        Сохранение ID задания на обучение:

        После обучения ID задания сохраняется с описанием в JSON-файл.
    """
    
    # Инициализация модели с системными инструкциями и ID ассистента (необязательно)
    model = OpenAIModel(api_key = gs.credentials.openai.api_key, system_instruction="You are a helpful assistant.", assistant_id="asst_dr5AgQnhhhnef5OSMzQ9zdk9")
    
    # Пример просмотра доступных моделей
    print("Доступные модели:")
    models = model.list_models
    pprint(models)

    # Пример просмотра доступных ассистентов
    print("\nДоступные ассистенты:")
    assistants = model.list_assistants
    pprint(assistants)

    # Пример запроса модели
    user_input = "Hello, how are you?"
    print("\nВвод пользователя:", user_input)
    response = model.ask(user_input)
    print("Ответ модели:", response)

    # Пример динамического обучения с использованием прошлого диалога
    print("\nВыполнение динамического обучения...")
    model.dynamic_train()

    # Пример обучения модели с использованием предоставленных данных
    print("\nОбучение модели...")
    training_result = model.train(data_file=gs.path.google_drive / 'AI' / 'training_data.csv')
    print(f"ID задания на обучение: {training_result}")

    # Пример сохранения ID задания
    if training_result:
        model.save_job_id(training_result, "Обучение модели с новыми данными", filename="job_ids.json")
        print(f"Сохранен ID задания на обучение: {training_result}")

    # Пример описания изображения
    image_path = gs.path.google_drive / 'images' / 'example_image.jpg'
    print("\nОписание изображения:")
    description = model.describe_image(image_path)
    print(f"Описание изображения: {description}")

if __name__ == "__main__":
    main()