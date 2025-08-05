## Как использовать класс Jmuz
=========================================================================================

Описание
-------------------------
Класс `Jmuz` - это провайдер для взаимодействия с API Jmuz.me, предоставляющим доступ к различным моделям GPT, таким как `gpt-4o`, `qwq-32b`, `gemini-1.5-flash` и т.д. 

Он наследует класс `OpenaiTemplate` и предоставляет ряд методов для работы с API, в том числе:
- `get_models()`: Возвращает список доступных моделей.
- `create_async_generator()`: Создает асинхронный генератор для получения ответов от модели.

Шаги выполнения
-------------------------
1. **Импорт класса**: Импортируй класс `Jmuz` из соответствующего модуля:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Jmuz import Jmuz
```

2. **Создание объекта**: Создай экземпляр класса `Jmuz`:
```python
provider = Jmuz()
```

3. **Получение списка доступных моделей**: Используй метод `get_models()` для получения доступных моделей:
```python
models = provider.get_models()
print(models)
```

4. **Создание асинхронного генератора**: Используй метод `create_async_generator()` для создания асинхронного генератора для получения ответов от модели.
```python
messages = [
    {"role": "user", "content": "Привет!"},
]

async_generator = provider.create_async_generator(
    model="gpt-4o",
    messages=messages,
)

async for chunk in async_generator:
    print(chunk)
```

5. **Обработка ответа**: Получай ответы от модели с помощью цикла `async for` и обрабатывай их как нужно.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Jmuz import Jmuz

provider = Jmuz()

# Получение списка доступных моделей
models = provider.get_models()
print("Доступные модели:", models)

# Создание асинхронного генератора для модели "gpt-4o"
messages = [
    {"role": "user", "content": "Как дела?"},
]
async_generator = provider.create_async_generator(
    model="gpt-4o",
    messages=messages,
)

# Получение ответов от модели
async for chunk in async_generator:
    print(chunk)
```

**Дополнительные сведения**:

- Метод `create_async_generator()` принимает следующие аргументы:
    - `model`: Название модели.
    - `messages`: Список сообщений для отправки в модель.
    - `stream`: Флаг, указывающий, нужно ли получать ответ потоком (True) или в виде единой строки (False).
- Класс `Jmuz` поддерживает обработку ошибок, связанных с использованием API Jmuz.me.
- Обрати внимание, что класс `Jmuz` может быть изменен в будущем, поэтому проверь документацию перед использованием.