# Gemini Client - Документация

## Описание

Клиент для работы с Google Gemini API через метод `ask()`. Поддерживает конфигурацию через файл `aistros.json`.

## Структура проекта

```
src/
├── endpoints/
│   └── aistros/
│       ├── aistros.json        ← Файл конфигурации
│       ├── gemini_client.py    ← Клиент Gemini (этот файл)
│       └── header.py           ← Определение __root__
└── llm/
    └── gemini/
        └── gemini.py           ← Базовый класс GoogleGenerativeAi
```

## Файл конфигурации `aistros.json`

### Структура файла

```json
{
  "key_name": "kazarinov",
  "model_name": "gemini-2.0-flash-lite",
  "generation_config": {
    "response_mime_type": "text/plain",
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40
  },
  "system_instruction": "Ты — полезный ассистент, который отвечает точно и по существу."
}
```

### Параметры

| Параметр | Тип | Описание | Обязательный |
|----------|-----|----------|--------------|
| `key_name` | string | Имя ключа из `gs.credentials.gemini.<key_name>.api_key` | Да |
| `model_name` | string | Название модели Gemini | Нет (по умолчанию: `gemini-2.0-flash-lite`) |
| `generation_config` | object | Конфигурация генерации ответов | Нет |
| `system_instruction` | string | Системная инструкция для модели | Нет |

### Расположение файла

Файл должен находиться по пути: `src/endpoints/aistros/aistros.json`

## Использование

### 1. Базовая инициализация (с использованием aistros.json)

```python
from src.endpoints.aistros.gemini_client import GeminiClient

# Все настройки берутся из aistros.json
client = GeminiClient()

# Простой запрос
response = client.ask('Что такое машинное обучение?')
print(response)
```

### 2. Инициализация с переопределением параметров

```python
# Переопределяем модель, остальное из aistros.json
client = GeminiClient(model_name='gemini-1.5-flash')

# Переопределяем API ключ
client = GeminiClient(api_key='your-custom-api-key')

# Переопределяем все параметры
client = GeminiClient(
    api_key='your-key',
    model_name='gemini-2.0-flash-lite',
    system_instruction='Отвечай как пират'
)
```

### 3. Запросы с контекстом (RAG)

```python
# Подготовка контекста
context = [
    'Компания "TechCorp" основана в 2020 году.',
    'Основной продукт - платформа DataViz Pro.',
    'Главный офис в Москве.'
]

# Запрос с контекстом
response = client.ask_with_context(
    question='Расскажи о компании TechCorp',
    context=context
)
print(response)
```

### 4. Управление повторными попытками

```python
# Увеличиваем количество попыток при ошибках
response = client.ask(
    question='Сложный вопрос',
    attempts=20  # По умолчанию 15
)
```

## Настройка credentials

API ключ должен быть настроен в `gs.credentials`:

```python
# Структура credentials
gs.credentials.gemini.<key_name>.api_key

# Примеры:
# gs.credentials.gemini.kazarinov.api_key
# gs.credentials.gemini.onela.api_key
# gs.credentials.gemini.production.api_key
```

### Пример настройки key_name

В `aistros.json`:
```json
{
  "key_name": "kazarinov"
}
```

Клиент будет искать ключ по пути: `gs.credentials.gemini.kazarinov.api_key`

## Приоритет настроек

При инициализации клиента параметры применяются в следующем порядке:

1. **Явно переданные параметры** (в конструкторе)
2. **Значения из aistros.json**
3. **Значения по умолчанию**

Пример:
```python
# В aistros.json: model_name = "gemini-2.0-flash-lite"
client = GeminiClient(model_name='gemini-1.5-flash')
# Будет использована модель 'gemini-1.5-flash' (явный параметр приоритетнее)
```

## Доступные модели

Из `gemini.json`:
- `gemini-1.5-flash-001-tuning`
- `gemini-1.5-flash-8b-exp-0924`
- `gemini-1.5-flash`
- `gemini-1.5-flash-8b`
- `gemini-1.5-turbo`
- `gemini-2.0-flash-exp`
- `gemini-2.0-flash-lite` (по умолчанию)
- `gemini-2-13b`
- `gemini-2.5-flash-preview-04-17`
- `gemini-2.5-flash-lite-preview-06-17`
- `gemini-3-20b`

## Примеры использования

### Пример 1: Техническая консультация

```python
client = GeminiClient()

question = 'Объясни разницу между list и tuple в Python'
answer = client.ask(question)
print(answer)
```

### Пример 2: RAG для корпоративных данных

```python
# Загрузка данных из базы знаний
knowledge_base = [
    'Политика отпусков: 28 дней в году',
    'Рабочий день: 9:00 - 18:00',
    'Удалённая работа: до 3 дней в неделю'
]

# Запрос с контекстом
question = 'Сколько дней отпуска положено?'
answer = client.ask_with_context(question, knowledge_base)
print(answer)
```

### Пример 3: Пакетная обработка вопросов

```python
client = GeminiClient()

questions = [
    'Что такое Python?',
    'Что такое машинное обучение?',
    'Что такое нейронные сети?'
]

for q in questions:
    answer = client.ask(q, attempts=10)
    if answer:
        print(f'Q: {q}\nA: {answer}\n')
```

## Обработка ошибок

Клиент автоматически обрабатывает ошибки и логирует их:

```python
response = client.ask('Вопрос')

if response is None:
    print('Не удалось получить ответ (проверьте логи)')
else:
    print(response)
```

## Логирование

Все операции логируются через `src.logger`:

- **INFO**: Успешные операции
- **WARNING**: Предупреждения (пустой ответ, отсутствие конфигурации)
- **ERROR**: Ошибки (проблемы с API, отсутствие ключа)
- **DEBUG**: Отладочная информация

## Troubleshooting

### Проблема: "API ключ не найден"

**Решение:**
1. Проверьте наличие `aistros.json` в `src/endpoints/aistros/`
2. Убедитесь, что `key_name` в `aistros.json` указан правильно
3. Проверьте, что ключ существует в `gs.credentials.gemini.<key_name>.api_key`

### Проблема: "Файл конфигурации не найден"

**Решение:**
1. Создайте файл `aistros.json` в `src/endpoints/aistros/`
2. Или передайте все параметры явно в конструктор

### Проблема: "Модель вернула пустой ответ"

**Решение:**
1. Увеличьте количество попыток: `client.ask(q, attempts=20)`
2. Проверьте логи на наличие ошибок квоты
3. Убедитесь, что вопрос не пустой

## Тестирование

Запуск demo:
```bash
python gemini_client.py
```

Вывод покажет примеры работы с различными типами запросов.
