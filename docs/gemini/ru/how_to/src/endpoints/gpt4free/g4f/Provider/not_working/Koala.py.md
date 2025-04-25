## Как использовать класс `Koala` 
=========================================================================================

Описание
-------------------------
Класс `Koala` реализует асинхронный генератор, который позволяет взаимодействовать с API сервиса `koala.sh` для получения ответов от моделей искусственного интеллекта.  Он предоставляет функции для отправки запросов с текстом и историей сообщений, а также  обработки ответов в виде потока данных.

Шаги выполнения
-------------------------
1. **Инициализация**: Создайте объект класса `Koala`, например:
   ```python
   koala_provider = Koala()
   ```
2. **Подготовка данных**:  Создайте список `messages` с историей сообщений в формате:
   ```python
   messages = [
       {'role': 'user', 'content': 'Привет! Как дела?'}, 
       {'role': 'assistant', 'content': 'Привет! У меня все отлично!'}
   ]
   ```
3. **Запуск генератора**: Используйте метод `create_async_generator` для получения асинхронного генератора. 
   ```python
   async def get_response():
       async for chunk in koala_provider.create_async_generator(model='gpt-4o-mini', messages=messages):
           print(chunk)
   ```
4. **Получение ответов**: Итерируйте по генератору, чтобы получить ответы от модели в виде словарей.
    ```python
    await get_response() 
    ```
5. **Обработка ответов**:  Доступ к информации в словаре:
    ```python
    # ...
    print(chunk['content']) # Вывод текста ответа
    print(chunk['role'])  #  Роль отправителя (assistant, user)
    # ...
    ```

Пример использования
-------------------------
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Koala import Koala

async def main():
    koala_provider = Koala()
    messages = [
        {'role': 'user', 'content': 'Привет! Как дела?'},
        {'role': 'assistant', 'content': 'Привет! У меня все отлично!'}
    ]
    
    async for chunk in koala_provider.create_async_generator(model='gpt-4o-mini', messages=messages):
        print(f"Ответ: {chunk['content']}")
        print(f"Роль: {chunk['role']}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```