# Инструкция по установке Gemini Client

## Структура директорий

Создайте следующую структуру в вашем проекте:

```
src/
├── endpoints/
│   └── aistros/
│       ├── aistros.json        ← Файл конфигурации
│       ├── gemini_client.py    ← Клиент Gemini
│       └── header.py           ← Определение __root__
└── llm/
    └── gemini/
        └── gemini.py           ← Должен уже существовать
```

## Шаги установки

### 1. Создайте директорию aistros

```bash
mkdir -p src/endpoints/aistros
```

### 2. Скопируйте файлы

Скопируйте следующие файлы в `src/endpoints/aistros/`:

- `gemini_client.py` - основной клиент
- `aistros.json` - конфигурация
- `header.py` - определение корневой директории

```bash
cp gemini_client.py src/endpoints/aistros/
cp aistros.json src/endpoints/aistros/
cp header.py src/endpoints/aistros/
```

### 3. Настройте aistros.json

Откройте `src/endpoints/aistros/aistros.json` и настройте параметры:

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
  "system_instruction": "Ты — полезный ассистент..."
}
```

**Важно:** `key_name` должен соответствовать ключу в `gs.credentials.gemini.<key_name>.api_key`

### 4. Проверьте credentials

Убедитесь, что API ключ настроен в credentials:

```python
# Структура credentials
gs.credentials.gemini.<key_name>.api_key

# Например:
gs.credentials.gemini.kazarinov.api_key = "ваш-api-ключ"
```

### 5. Проверьте установку

```python
from src.endpoints.aistros.gemini_client import GeminiClient

# Тест
client = GeminiClient()
response = client.ask('Привет!')
print(response)
```

## Использование

### Базовый пример

```python
from src.endpoints.aistros.gemini_client import GeminiClient

# Инициализация (настройки из aistros.json)
client = GeminiClient()

# Простой запрос
response = client.ask('Что такое Python?')
print(response)
```

### С контекстом (RAG)

```python
context = [
    'Компания основана в 2020 году',
    'Основной продукт - AI Assistant'
]

response = client.ask_with_context(
    question='Когда основана компания?',
    context=context
)
print(response)
```

### С переопределением параметров

```python
# Переопределяем модель
client = GeminiClient(model_name='gemini-1.5-flash')

# Переопределяем API ключ
client = GeminiClient(api_key='your-custom-key')
```

## Troubleshooting

### Ошибка: "API ключ не найден"

**Причина:** Не настроен `key_name` в `aistros.json` или отсутствует ключ в credentials.

**Решение:**
1. Проверьте `aistros.json` - должен быть параметр `key_name`
2. Убедитесь, что `gs.credentials.gemini.<key_name>.api_key` существует

### Ошибка: "Файл конфигурации не найден"

**Причина:** Файл `aistros.json` находится не в той директории.

**Решение:**
1. Убедитесь, что `aistros.json` находится в `src/endpoints/aistros/`
2. Проверьте структуру директорий

### Ошибка импорта

**Причина:** Неправильный путь импорта.

**Решение:**
Используйте правильный импорт:
```python
from src.endpoints.aistros.gemini_client import GeminiClient
```

А не:
```python
from src.llm.gemini.gemini_client import GeminiClient  # ❌ Неправильно
```

## Дополнительная информация

Полная документация: `README_gemini_client.md`
