## Клиент для модели Claude от Anthropic

```rst
.. module:: src.ai.anthropic
```

[English](https://github.com/hypo69/hypotez/blob/master/src/ai/anthropic/README.MD)

### Описание

Этот Python-модуль предоставляет простой интерфейс для взаимодействия с языковой моделью Claude от Anthropic. Он включает базовые функции для генерации текста, анализа тональности и перевода текста.

#### Основные функции:

1.  **Инициализация клиента Claude:**
    *   Для работы с API Claude необходим API-ключ. Этот модуль предоставляет класс для удобной инициализации с API-ключом.

2.  **Разнообразные операции с текстом:**

    *   `Генерация текста`: Позволяет создавать новый контент на основе заданных промптов.
    *   `Анализ тональности`: Определяет эмоциональную окраску текста (положительная, отрицательная, нейтральная).
    *   `Перевод`: Предоставляет возможность переводить текст с одного языка на другой.

### Пример использования

Ниже приведен пример использования класса `ClaudeClient`:

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)

# Пример генерации текста
prompt = 'Напишите короткую историю о роботе, который учится любить.'
generated_text = claude_client.generate_text(prompt)
print('Сгенерированный текст:', generated_text)

# Пример анализа тональности
text_to_analyze = "Сегодня я очень счастлив!"
sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
print('Анализ тональности:', sentiment_analysis)

# Пример перевода текста
text_to_translate = "Привет, как дела?"
source_language = "ru"
target_language = "en"
translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
print('Переведенный текст:', translated_text)
```

#### Для работы с Claude API необходимо

1.  Установить библиотеку Anthropic:

```bash
pip install anthropic
```

2.  Получить Api Key от Anthropic.

### Доступные методы

*   **`generate_text(prompt, max_tokens_to_sample=100)`**: Генерирует текст на основе заданного промпта.

    *   **Параметры:**
        *   `prompt`: Текст запроса для генерации.
        *   `max_tokens_to_sample`: (необязательный) Максимальное количество токенов для генерации (по умолчанию: 100).
    *   **Возвращает:** Сгенерированный текст.

*   **`analyze_sentiment(text)`**: Анализирует тональность заданного текста.

    *   **Параметры:**
        *   `text`: Текст для анализа.
    *   **Возвращает:** Результат анализа тональности.

*   **`translate_text(text, source_language, target_language)`**: Переводит заданный текст с одного языка на другой.

    *   **Параметры:**
        *   `text`: Текст для перевода.
        *   `source_language`: Код исходного языка.
        *   `target_language`: Код целевого языка.
    *   **Возвращает:** Переведенный текст.

### Вклад

Вклад приветствуется! Не стесняйтесь отправлять pull request или открывать issue, если вы столкнулись с какими-либо проблемами или имеете предложения по улучшению.

### Лицензия

Этот проект лицензирован под MIT License. Подробности смотрите в файле [LICENSE](LICENSE).

---

**Примечание:** Замените `"your-api-key"` на ваш реальный API-ключ от Anthropic.