### **Анализ кода модуля `training.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Использование аннотаций типов.
  - Логирование с использованием `logger`.
  - Четкое разделение на классы и методы.
- **Минусы**:
  - Отсутствие docstring для некоторых методов (например, `describe_image`).
  - Не все функции и классы имеют docstring на русском языке.
  - Использование `Union` вместо `|` для аннотаций типов.
  - Смешанный стиль кавычек (иногда используются двойные кавычки вместо одинарных).

#### **Рекомендации по улучшению**:
1. **Документация**:
   - Добавить docstring для метода `describe_image`.
   - Перевести существующие docstring на русский язык.
   - Убедиться, что все docstring соответствуют формату, указанному в инструкции.

2. **Форматирование**:
   - Использовать только одинарные кавычки (`'`) для строк.
   - Заменить `Union` на `|` в аннотациях типов.
   - Обеспечить наличие пробелов вокруг операторов присваивания.

3. **Обработка исключений**:
   - Убедиться, что все блоки `except` используют `ex` вместо `e`.

4. **Использование `j_loads` и `j_dumps`**:
   - Убедиться, что для чтения JSON файлов используется `j_loads` или `j_loads_ns`.
   - Убедиться, что для записи JSON файлов используется `j_dumps`.

5. **Логирование**:
   - Проверить, что все ошибки логируются с использованием `logger.error` и передачей исключения `ex` и `exc_info=True`.

6. **Аннотации типов**:
   - Убедиться, что все переменные и параметры функций аннотированы типами.

#### **Оптимизированный код**:

```python
## \file /src/ai/openai/model/training.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для работы с OpenAI Model
=================================================

Модуль содержит класс :class:`OpenAIModel`, который используется для взаимодействия с OpenAI API
и управления моделью.
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
    """OpenAI Model Class for interacting with the OpenAI API and managing the model."""

    model: str = 'gpt-4o-mini'
    # model: str = "gpt-4o-2024-08-06"
    client: OpenAI
    current_job_id: str
    assistant_id: str
    assistant = None
    thread = None
    system_instruction: str
    dialogue_log_path: str | Path = gs.path.google_drive / 'AI' / f'{model}_{gs.now}.json'
    dialogue: List[Dict[str, str]] = []
    assistants: List[SimpleNamespace]
    models_list: List[str]

    def __init__(self, api_key: str, system_instruction: str = None, model_name: str = 'gpt-4o-mini', assistant_id: str = None):
        """Инициализация объекта Model с API-ключом, ID ассистента и загрузка доступных моделей и ассистентов.

        Args:
            api_key (str): API ключ OpenAI.
            system_instruction (str, optional): Инструкция для модели. Defaults to None.
            model_name (str, optional): Имя модели. Defaults to 'gpt-4o-mini'.
            assistant_id (str, optional): ID ассистента. Defaults to None.
        """
        # self.client = OpenAI(api_key = gs.credentials.openai.project_api)
        self.client = OpenAI(api_key=api_key if api_key else gs.credentials.openai.api_key)
        self.current_job_id = None
        self.assistant_id = assistant_id or gs.credentials.openai.assistant_id.code_assistant
        self.system_instruction = system_instruction

        # Load assistant and thread during initialization
        self.assistant = self.client.beta.assistants.retrieve(self.assistant_id)
        self.thread = self.client.beta.threads.create()

    @property
    def list_models(self) -> List[str]:
        """Динамически получает и возвращает доступные модели из OpenAI API.

        Returns:
            List[str]: Список ID моделей, доступных через OpenAI API.
        """
        try:
            models = self.client.models.list()
            model_list = [model['id'] for model in models['data']]
            logger.info(f'Loaded models: {model_list}')
            return model_list
        except Exception as ex:
            logger.error('An error occurred while loading models:', ex, exc_info=True)
            return []

    @property
    def list_assistants(self) -> List[str]:
        """Динамически загружает доступных ассистентов из JSON файла.

        Returns:
            List[str]: Список имен ассистентов.
        """
        try:
            self.assistants = j_loads_ns(gs.path.src / 'ai' / 'openai' / 'model' / 'assistants' / 'assistants.json')
            assistant_list = [assistant.name for assistant in self.assistants]
            logger.info(f'Loaded assistants: {assistant_list}')
            return assistant_list
        except Exception as ex:
            logger.error('An error occurred while loading assistants:', ex, exc_info=True)
            return []

    def set_assistant(self, assistant_id: str):
        """Устанавливает ассистента, используя предоставленный ID ассистента.

        Args:
            assistant_id (str): ID ассистента для установки.
        """
        try:
            self.assistant_id = assistant_id
            self.assistant = self.client.beta.assistants.retrieve(assistant_id)
            logger.info(f'Assistant set successfully: {assistant_id}')
        except Exception as ex:
            logger.error('An error occurred while setting the assistant:', ex, exc_info=True)

    def _save_dialogue(self):
        """Сохраняет весь диалог в JSON файл."""
        j_dumps(self.dialogue, self.dialogue_log_path)

    def determine_sentiment(self, message: str) -> str:
        """Определяет тональность сообщения (положительная, отрицательная или нейтральная).

        Args:
            message (str): Сообщение для анализа.

        Returns:
            str: Тональность ('positive', 'negative' или 'neutral').
        """
        positive_words = ['good', 'great', 'excellent', 'happy', 'love', 'wonderful', 'amazing', 'positive']
        negative_words = ['bad', 'terrible', 'hate', 'sad', 'angry', 'horrible', 'negative', 'awful']
        neutral_words = ['okay', 'fine', 'neutral', 'average', 'moderate', 'acceptable', 'sufficient']

        message_lower = message.lower()

        if any(word in message_lower for word in positive_words):
            return 'positive'
        elif any(word in message_lower for word in negative_words):
            return 'negative'
        elif any(word in message_lower for word in neutral_words):
            return 'neutral'
        else:
            return 'neutral'

    def ask(self, message: str, system_instruction: str = None, attempts: int = 3) -> str:
        """Отправляет сообщение модели и возвращает ответ вместе с анализом тональности.

        Args:
            message (str): Сообщение для отправки модели.
            system_instruction (str, optional): Дополнительная системная инструкция.
            attempts (int, optional): Количество попыток повтора. Defaults to 3.

        Returns:
            str: Ответ от модели.
        """
        try:
            messages = []
            if self.system_instruction or system_instruction:
                system_instruction_escaped = (system_instruction or self.system_instruction).replace('"', r'\"')
                messages.append({'role': 'system', 'content': system_instruction_escaped})

            message_escaped = message.replace('"', r'\"')
            messages.append({
                'role': 'user',
                'content': message_escaped
            })

            # Отправка запроса к модели
            response = self.client.chat.completions.create(
                model=self.model,

                messages=messages,
                temperature=0,
                max_tokens=8000,
            )
            reply = response.choices[0].message.content.strip()

            # Анализ тональности
            sentiment = self.determine_sentiment(reply)

            # Добавление сообщений и тональности в диалог
            self.dialogue.append({'role': 'system', 'content': system_instruction or self.system_instruction})
            self.dialogue.append({'role': 'user', 'content': message_escaped})
            self.dialogue.append({'role': 'assistant', 'content': reply, 'sentiment': sentiment})

            # Сохранение диалога
            self._save_dialogue()

            return reply
        except Exception as ex:
            logger.debug(f'An error occurred while sending the message: \n-----\n {pprint(messages)} \n-----\n', ex, True)
            time.sleep(3)
            if attempts > 0:
                return self.ask(message, message, attempts - 1)
            return

    def describe_image(self, image_path: str | Path, prompt: Optional[str] = None, system_instruction: Optional[str] = None) -> str:
        """Описывает изображение, используя OpenAI API.

        Args:
            image_path (str | Path): Путь к изображению.
            prompt (Optional[str], optional): Запрос для описания изображения. По умолчанию None.
            system_instruction (Optional[str], optional): Системная инструкция. По умолчанию None.

        Returns:
            str: Описание изображения.
        """
        messages: list = []
        base64_image = base64encode(image_path)

        if system_instruction:
            messages.append({'role': 'system', 'content': system_instruction})

        messages.append(
            {
                'role': 'user',
                'content': [
                    {'type': 'text',
                     'text': prompt if prompt else 'What\'s in this image?'},
                    {
                        'type': 'image_url',
                        'image_url': {'url': f'data:image/jpeg;base64,{base64_image}'}
                    },
                ],
            }
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0,
                max_tokens=800,
            )

            reply = response
            ...
            try:
                raw_reply = response.choices[0].message.content.strip()
                return j_loads_ns(raw_reply)
            except Exception as ex:
                logger.error(f'Trouble in reponse {response}', ex, True)
                ...
                return

        except Exception as ex:
            logger.error(f'Ошибка openai', ex, True)
            ...
            return

    def describe_image_by_requests(self, image_path: str | Path, prompt: str = None) -> str:
        """Отправляет изображение в OpenAI API и получает описание.

        Args:
            image_path (str | Path): Путь к изображению.
            prompt (str, optional): Запрос для описания изображения. Defaults to None.
        """
        # Getting the base64 string
        base64_image = base64encode(image_path)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {gs.credentials.openai.project_api}'
        }

        payload = {
            'model': 'gpt-4o',
            'messages': [
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'text',
                            'text': prompt if prompt else 'What’s in this image?'
                        },
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': f'data:image/jpeg;base64,{base64_image}'
                            }
                        }
                    ]
                }
            ],
            'max_tokens': 300
        }
        try:
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=payload)
            response_json = response.json()
            ...
        except Exception as ex:
            logger.error(f'Error in image description {image_path=}\n', ex, exc_info=True)

    def dynamic_train(self):
        """Динамически загружает предыдущий диалог и дообучает модель на его основе."""
        try:
            messages = j_loads(gs.path.google_drive / 'AI' / 'conversation' / 'dailogue.json')

            if messages:
                response = self.client.chat.completions.create(
                    model=self.model,
                    assistant=self.assistant_id,
                    messages=messages,
                    temperature=0,
                )
                logger.info('Fine-tuning during the conversation was successful.')
            else:
                logger.info('No previous dialogue found for fine-tuning.')
        except Exception as ex:
            logger.error(f'Error during dynamic fine-tuning: {ex}', exc_info=True)

    def train(self, data: str = None, data_dir: Path | str = None, data_file: Path | str = None, positive: bool = True) -> str | None:
        """Обучает модель на указанных данных или директории.

        Args:
            data (str, optional): Путь к CSV файлу или CSV-форматированной строке с данными.
            data_dir (Path | str, optional): Директория, содержащая CSV файлы для обучения.
            data_file (Path | str, optional): Путь к отдельному CSV файлу с данными для обучения.
            positive (bool, optional): Указывает, являются ли данные положительными или отрицательными. Defaults to True.

        Returns:
            str | None: ID задания на обучение или None, если произошла ошибка.
        """
        if not data_dir:
            data_dir = gs.path.google_drive / 'AI' / 'training'

        try:
            documents = j_loads(data if data else data_file if data_file else data_dir)

            response = self.client.Training.create(
                model=self.model,
                documents=documents,
                labels=['positive' if positive else 'negative'] * len(documents),
                show_progress=True
            )
            self.current_job_id = response.id
            return response.id

        except Exception as ex:
            logger.error('An error occurred during training:', ex, exc_info=True)
            return

    def save_job_id(self, job_id: str, description: str, filename: str = 'job_ids.json'):
        """Сохраняет ID задания с описанием в файл.

        Args:
            job_id (str): ID задания для сохранения.
            description (str): Описание задания.
            filename (str, optional): Имя файла для сохранения ID заданий. Defaults to "job_ids.json".
        """
        job_data = {'id': job_id, 'description': description, 'created': time.time()}
        job_file = gs.path.google_drive / filename

        if not job_file.exists():
            j_dumps([job_data], job_file)
        else:
            existing_jobs = j_loads(job_file)
            existing_jobs.append(job_data)
            j_dumps(existing_jobs, job_file)


def main():
    """Main function to initialize the OpenAIModel and demonstrate usage.
    Explanation:
        Initialization of the Model:

        The OpenAIModel is initialized with a system instruction and an assistant ID. You can modify the parameters if necessary.
        Listing Models and Assistants:

        The list_models and list_assistants methods are called to print the available models and assistants.
        Asking the Model a Question:

        The ask() method is used to send a message to the model and retrieve its response.
        Dynamic Training:

        The dynamic_train() method performs dynamic fine-tuning based on past dialogue.
        Training the Model:

        The train() method trains the model using data from a specified file (in this case, 'training_data.csv').
        Saving the Training Job ID:

        After training, the job ID is saved with a description to a JSON file."""

    # Initialize the model with system instructions and assistant ID (optional)
    model = OpenAIModel(api_key = 'sk-', system_instruction='You are a helpful assistant.', assistant_id='asst_dr5AgQnhhhnef5OSMzQ9zdk9')

    # Example of listing available models
    print('Available Models:')
    models = model.list_models
    pprint(models)

    # Example of listing available assistants
    print('\nAvailable Assistants:')
    assistants = model.list_assistants
    pprint(assistants)

    # Example of asking the model a question
    user_input = 'Hello, how are you?'
    print('\nUser Input:', user_input)
    response = model.ask(user_input)
    print('Model Response:', response)

    # Example of dynamic training using past dialogue
    print('\nPerforming dynamic training...')
    model.dynamic_train()

    # Example of training the model using provided data
    print('\nTraining the model...')
    training_result = model.train(data_file=gs.path.google_drive / 'AI' / 'training_data.csv')
    print(f'Training job ID: {training_result}')

    # Example of saving a job ID
    if training_result:
        model.save_job_id(training_result, 'Training model with new data', filename='job_ids.json')
        print(f'Saved training job ID: {training_result}')

    # Пример описания изображения
    image_path = gs.path.google_drive / 'images' / 'example_image.jpg'
    print('\nDescribing Image:')
    description = model.describe_image(image_path)
    print(f'Image description: {description}')


if __name__ == '__main__':
    main()