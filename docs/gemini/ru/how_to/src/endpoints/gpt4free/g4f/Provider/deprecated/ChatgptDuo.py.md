### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет асинхронного провайдера `ChatgptDuo` для взаимодействия с API `chatgptduo.com`. Он позволяет отправлять запросы к модели GPT-3.5 Turbo и получать ответы. Класс `ChatgptDuo` предоставляет методы для создания асинхронного запроса и получения источников, использованных для генерации ответа.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются `Messages` для работы с сообщениями, `StreamSession` для асинхронных HTTP-запросов, `AsyncProvider` как базовый класс для асинхронных провайдеров и `format_prompt` для форматирования запроса.

2. **Определение класса `ChatgptDuo`**:
   - Устанавливаются атрибуты класса:
     - `url`: URL API `chatgptduo.com`.
     - `supports_gpt_35_turbo`: Указывает, что провайдер поддерживает модель GPT-3.5 Turbo.
     - `working`: Флаг, указывающий на работоспособность провайдера (изначально `False`).

3. **Определение асинхронного метода `create_async`**:
   - Метод принимает следующие аргументы:
     - `model` (str): Название модели.
     - `messages` (Messages): Список сообщений для отправки.
     - `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
     - `timeout` (int, optional): Время ожидания запроса в секундах. По умолчанию `120`.
     - `**kwargs`: Дополнительные аргументы.
   - Функция выполняет:
     - Создание асинхронной сессии с использованием `StreamSession` с настройками `impersonate="chrome107"` и прокси.
     - Форматирование запроса с использованием `format_prompt(messages)`.
     - Формирование данных запроса в виде словаря, включающего `prompt`, `search` и `purpose`.
     - Отправка POST-запроса к `f"{cls.url}/"` с данными.
     - Обработка ответа:
       - Проверка статуса ответа с помощью `response.raise_for_status()`.
       - Преобразование JSON-ответа в словарь.
       - Извлечение источников (`title`, `url`, `snippet`) из данных ответа и сохранение их в `cls._sources`.
       - Возврат ответа (`data["answer"]`).

4. **Определение метода `get_sources`**:
   - Метод возвращает список источников, сохраненных в `cls._sources`.

Пример использования
-------------------------

```python
from typing import List, Dict
from src.endpoints.gpt4free.g4f.Provider.deprecated.ChatgptDuo import ChatgptDuo
from src.endpoints.gpt4free.g4f.typing import Messages
import asyncio

async def main():
    # Подготовка сообщений для отправки
    messages: Messages = [
        {"role": "user", "content": "Напиши небольшое стихотворение о весне."}
    ]

    try:
        # Отправка запроса к ChatgptDuo
        answer = await ChatgptDuo.create_async(model="gpt-3.5-turbo", messages=messages)
        print(f"Ответ: {answer}")

        # Получение источников
        sources: List[Dict[str, str]] = ChatgptDuo.get_sources()
        print("Источники:")
        for source in sources:
            print(f"  - Title: {source['title']}")
            print(f"    URL: {source['url']}")
            print(f"    Snippet: {source['snippet']}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())