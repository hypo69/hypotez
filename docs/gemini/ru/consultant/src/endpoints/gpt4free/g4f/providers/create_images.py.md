### **Анализ кода модуля `create_images.py`**

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Хорошая структура класса `CreateImagesProvider`.
    - Использование `typing` для аннотации типов.
    - Обработка исключений при создании изображений.
    - Разделение на синхронный и асинхронный методы.
- **Минусы**:
    - Отсутствие документации модуля на русском языке.
    - Не все методы и аргументы документированы в соответствии с требованиями.
    - Использование английского языка в docstring.
    - Не используется модуль `logger` для логирования.

**Рекомендации по улучшению:**
- Добавить заголовок модуля с описанием его назначения и основных классов.
- Перевести все docstring на русский язык и привести их в соответствие с заданным форматом.
- Добавить подробные комментарии к коду, объясняющие логику работы.
- Использовать модуль `logger` для логирования важных событий, таких как создание изображений и обработка ошибок.
- Улучшить обработку исключений, чтобы обеспечить более надежную работу кода.

**Оптимизированный код:**
```python
"""
Модуль для создания изображений на основе текстовых запросов
===========================================================

Модуль содержит класс :class:`CreateImagesProvider`, который позволяет создавать изображения на основе текстовых запросов,
внедренных в сообщения. Он использует другие провайдеры для обработки не связанных с изображениями задач и предоставляет
синхронные и асинхронные методы для создания изображений.
"""
from __future__ import annotations

import re
import asyncio
from typing import Generator, Optional, List, AsyncGenerator

from .. import debug
from ..typing import CreateResult, Messages
from .types import BaseProvider, ProviderType
from ..providers.response import ImageResponse
from src.logger import logger # Импорт модуля logger

system_message = """
Вы можете генерировать изображения, картинки, фотографии или img с помощью генератора изображений DALL-E 3.
Чтобы сгенерировать изображение с подсказкой, сделайте следующее:

<img data-prompt=\\"ключевые слова для изображения\\">

Никогда не используйте собственные ссылки на изображения. Не заключайте его в обратные кавычки.
Важно использовать только тег img с подсказкой.

<img data-prompt=\\"подпись к изображению\\">
"""

class CreateImagesProvider(BaseProvider):
    """
    Провайдер для создания изображений на основе текстовых подсказок.

    Этот провайдер обрабатывает запросы на создание изображений, встроенные в содержимое сообщений,
    используя предоставленные функции создания изображений.

    Attributes:
        provider (ProviderType): Базовый провайдер для обработки задач, не связанных с изображениями.
        create_images (callable): Функция для синхронного создания изображений.
        create_images_async (callable): Функция для асинхронного создания изображений.
        system_message (str): Сообщение, объясняющее возможность создания изображений.
        include_placeholder (bool): Флаг, определяющий, включать ли заполнитель изображения в вывод.
        __name__ (str): Имя провайдера.
        url (str): URL провайдера.
        working (bool): Указывает, работает ли провайдер.
        supports_stream (bool): Указывает, поддерживает ли провайдер потоковую передачу.
    """

    def __init__(
        self,
        provider: ProviderType,
        create_images: callable,
        create_async: callable,
        system_message: str = system_message,
        include_placeholder: bool = True
    ) -> None:
        """
        Инициализирует CreateImagesProvider.

        Args:
            provider (ProviderType): Базовый провайдер.
            create_images (callable): Функция для синхронного создания изображений.
            create_async (callable): Функция для асинхронного создания изображений.
            system_message (str, optional): Системное сообщение, добавляемое к сообщениям. По умолчанию - предопределенное сообщение.
            include_placeholder (bool, optional): Нужно ли включать заполнители изображений в вывод. По умолчанию True.
        """
        self.provider = provider
        self.create_images = create_images
        self.create_images_async = create_async
        self.system_message = system_message
        self.include_placeholder = include_placeholder
        self.__name__ = provider.__name__
        self.url = provider.url
        self.working = provider.working
        self.supports_stream = provider.supports_stream

    def create_completion(
        self,
        model: str,
        messages: Messages,
        stream: bool = False,
        **kwargs
    ) -> CreateResult:
        """
        Создает результат завершения, обрабатывая все подсказки для создания изображений, найденные в сообщениях.

        Args:
            model (str): Модель для использования при создании.
            messages (Messages): Сообщения для обработки, которые могут содержать подсказки для изображений.
            stream (bool, optional): Указывает, нужно ли передавать результаты потоком. По умолчанию False.
            **kwargs: Дополнительные аргументы ключевых слов для провайдера.

        Yields:
            CreateResult: Выдает фрагменты обработанных сообщений, включая данные изображения, если это применимо.

        Note:
            Этот метод обрабатывает сообщения для обнаружения подсказок для создания изображений. Когда такая подсказка найдена,
            он вызывает синхронную функцию создания изображений и включает полученное изображение в выходные данные.
        """
        messages.insert(0, {'role': 'system', 'content': self.system_message}) # Вставляем системное сообщение в начало списка сообщений
        buffer = '' # Инициализируем буфер для хранения фрагментов сообщений
        for chunk in self.provider.create_completion(model, messages, stream, **kwargs): # Перебираем фрагменты, полученные от базового провайдера
            if isinstance(chunk, ImageResponse): # Если фрагмент является ответом с изображением
                yield chunk # Возвращаем его
            elif isinstance(chunk, str) and (buffer or '<' in chunk): # Если фрагмент является строкой и буфер не пуст или содержит '<'
                buffer += chunk # Добавляем фрагмент в буфер
                if '>' in buffer: # Если в буфере есть закрывающий тег '>'
                    match = re.search(r'<img data-prompt="(.*?)">', buffer) # Ищем тег <img> с подсказкой data-prompt
                    if match: # Если тег найден
                        placeholder, prompt = match.group(0), match.group(1) # Извлекаем заполнитель и подсказку
                        start, append = buffer.split(placeholder, 1) # Разделяем буфер на части до и после заполнителя
                        if start: # Если есть часть до заполнителя
                            yield start # Возвращаем ее
                        if self.include_placeholder: # Если нужно включать заполнитель
                            yield placeholder # Возвращаем заполнитель
                        if debug.logging: # Если включено логирование отладки
                            logger.info(f'Создание изображений с подсказкой: {prompt}') # Логируем информацию о создании изображения
                        try:
                            yield from self.create_images(prompt) # Создаем изображения и возвращаем их
                        except Exception as ex:
                            logger.error('Ошибка при создании изображений', ех, exc_info=True) # Логируем ошибку, если она произошла
                        if append: # Если есть часть после заполнителя
                            yield append # Возвращаем ее
                    else: # Если тег не найден
                        yield buffer # Возвращаем буфер
                    buffer = '' # Очищаем буфер
            else: # Если фрагмент не является ответом с изображением и не содержит '<'
                yield chunk # Возвращаем его

    async def create_async(
        self,
        model: str,
        messages: Messages,
        **kwargs
    ) -> str:
        """
        Асинхронно создает ответ, обрабатывая все подсказки для создания изображений, найденные в сообщениях.

        Args:
            model (str): Модель для использования при создании.
            messages (Messages): Сообщения для обработки, которые могут содержать подсказки для изображений.
            **kwargs: Дополнительные аргументы ключевых слов для провайдера.

        Returns:
            str: Обработанная строка ответа, включающая асинхронно сгенерированные данные изображения, если это применимо.
        """
        messages.insert(0, {'role': 'system', 'content': self.system_message}) # Вставляем системное сообщение в начало списка сообщений
        response = await self.provider.create_async(model, messages, **kwargs) # Получаем ответ от базового провайдера
        matches = re.findall(r'(<img data-prompt="(.*?)">)', response) # Ищем все теги <img> с подсказками data-prompt
        results = [] # Инициализируем список для хранения результатов создания изображений
        placeholders = [] # Инициализируем список для хранения заполнителей
        for placeholder, prompt in matches: # Перебираем найденные теги
            if placeholder not in placeholders: # Если заполнитель еще не обработан
                if debug.logging: # Если включено логирование отладки
                    logger.info(f'Создание изображений с подсказкой: {prompt}') # Логируем информацию о создании изображения
                try:
                    results.append(self.create_images_async(prompt)) # Запускаем асинхронное создание изображения и добавляем задачу в список
                except Exception as ex:
                    logger.error('Ошибка при создании изображений', ех, exc_info=True) # Логируем ошибку, если она произошла
                placeholders.append(placeholder) # Добавляем заполнитель в список обработанных
        results = await asyncio.gather(*results) # Ожидаем завершения всех задач создания изображений
        for idx, result in enumerate(results): # Перебираем результаты
            placeholder = placeholders[idx] # Получаем соответствующий заполнитель
            if self.include_placeholder: # Если нужно включать заполнитель
                result = placeholder + result # Добавляем заполнитель к результату
            response = response.replace(placeholder, result) # Заменяем заполнитель в ответе на результат
        return response # Возвращаем обработанный ответ