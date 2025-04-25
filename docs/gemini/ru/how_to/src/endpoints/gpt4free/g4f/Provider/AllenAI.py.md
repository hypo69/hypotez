## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода представляет класс `AllenAI`, который реализует асинхронный генератор текста с использованием модели AllenAI. 
Он предоставляет функциональность для отправки запросов к API AllenAI и обработки полученных ответов.

Шаги выполнения
-------------------------
1. **Инициализация**:
   - Создание экземпляра класса `AllenAI` с указанием модели (`model`) для генерации текста.
   - Создание объекта `Conversation`, который хранит историю сообщений.
   - Форматирование запроса (`prompt`) в соответствии с требованиями API AllenAI.
2. **Отправка запроса**:
   - Формирование `multipart/form-data` для отправки запроса к API.
   - Установка необходимых заголовков запроса, включая `x-anonymous-user-id`.
   - Отправка запроса к API AllenAI с использованием `aiohttp` и обработка ответа.
3. **Обработка ответа**:
   - Декодирование полученного ответа в JSON-формат.
   - Обработка `children` в ответе для обновления `parent` в `conversation`.
   - Извлечение и обработка текстового содержимого от `assistant`.
   - Обновление `conversation` с новыми сообщениями.
   - Возврат `conversation` и `FinishReason` после завершения генерации.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.AllenAI import AllenAI, Conversation

# Создание экземпляра AllenAI с моделью 'tulu3-405b'
provider = AllenAI(model='tulu3-405b')

# Создание объекта Conversation
conversation = Conversation(model='tulu3-405b')

# Формирование запроса
prompt = "Напиши стихотворение про кошку."

# Генерация текста с использованием async_generator
async for chunk in provider.create_async_generator(model='tulu3-405b', messages=[{'role': 'user', 'content': prompt}], conversation=conversation):
    print(chunk)

# Получение final_response
final_response = conversation.messages[-1]['content']
print(f"Final response: {final_response}")
```