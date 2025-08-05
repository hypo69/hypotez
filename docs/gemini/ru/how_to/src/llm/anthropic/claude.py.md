## Как использовать клиент Claude
=========================================================================================

Описание
-------------------------
Клиент Claude предоставляет доступ к функциям Claude AI, позволяя генерировать текст, анализировать тональность и переводить текст.

Шаги выполнения
-------------------------
1. **Инициализация клиента:**  Создайте экземпляр класса `ClaudeClient` с предоставленным API-ключом. API-ключ можно получить на [сайте Anthropic](https://www.anthropic.com/).
2. **Использование методов:**  Клиент предоставляет следующие методы для работы с Claude AI:
    - `generate_text(prompt: str, max_tokens_to_sample: int = 100) -> str`: Генерирует текст на основе предоставленного запроса.
    - `analyze_sentiment(text: str) -> str`: Анализирует тональность текста.
    - `translate_text(text: str, source_language: str, target_language: str) -> str`: Переводит текст с исходного языка на целевой.

Пример использования
-------------------------

```python
    api_key = 'your-api-key'
    claude_client = ClaudeClient(api_key)

    # Пример генерации текста
    prompt = 'Write a short story about a robot learning to love.'
    generated_text = claude_client.generate_text(prompt)
    print('Generated Text:', generated_text)

    # Пример анализа тональности
    text_to_analyze = 'I am very happy today!'
    sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
    print('Sentiment Analysis:', sentiment_analysis)

    # Пример перевода текста
    text_to_translate = 'Hello, how are you?'
    source_language = 'en'
    target_language = 'es'
    translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
    print('Translated Text:', translated_text)
```