# Anthropic Claude Client

## Overview

This Python module provides a simple interface to interact with the Claude language model from Anthropic. It includes basic functions for text generation, sentiment analysis, and text translation.

## Details

The module leverages the `anthropic` library, which allows developers to utilize Anthropic's Claude language model for various natural language processing tasks. The `ClaudeClient` class acts as the central component, providing methods to perform text generation, sentiment analysis, and text translation.

## Classes

### `ClaudeClient`

**Description**: Класс для взаимодействия с API Anthropic Claude.

**Attributes**:
- `api_key` (str): Ключ API Anthropic для аутентификации.

**Methods**:
- `generate_text(prompt, max_tokens_to_sample=100)`: Генерация текста на основе предоставленной подсказки.
- `analyze_sentiment(text)`: Анализ тональности текста.
- `translate_text(text, source_language, target_language)`: Перевод текста с одного языка на другой.

## Functions

### `generate_text(prompt, max_tokens_to_sample=100)`

**Purpose**: Генерация текста на основе заданной подсказки.

**Parameters**:
- `prompt` (str): Текст подсказки для модели Claude.
- `max_tokens_to_sample` (int, optional): Максимальное количество токенов, которые должны быть сгенерированы. По умолчанию 100.

**Returns**:
- str: Сгенерированный текст.

**Examples**:

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)

prompt = "Write a short story about a robot learning to love."
generated_text = claude_client.generate_text(prompt)
print("Generated Text:", generated_text)
```

### `analyze_sentiment(text)`

**Purpose**: Анализ тональности текста.

**Parameters**:
- `text` (str): Текст, который нужно проанализировать.

**Returns**:
- dict: Словарь с результатами анализа тональности.

**Examples**:

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)

text_to_analyze = "I am very happy today!"
sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
print("Sentiment Analysis:", sentiment_analysis)
```

### `translate_text(text, source_language, target_language)`

**Purpose**: Перевод текста с одного языка на другой.

**Parameters**:
- `text` (str): Текст, который нужно перевести.
- `source_language` (str): Код исходного языка.
- `target_language` (str): Код целевого языка.

**Returns**:
- str: Переведенный текст.

**Examples**:

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)

text_to_translate = "Hello, how are you?"
source_language = "en"
target_language = "es"
translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
print("Translated Text:", translated_text)
```

## Example Code

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)

# Generate text
prompt = "Write a short story about a robot learning to love."
generated_text = claude_client.generate_text(prompt)
print("Generated Text:", generated_text)

# Analyze sentiment
text_to_analyze = "I am very happy today!"
sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
print("Sentiment Analysis:", sentiment_analysis)

# Translate text
text_to_translate = "Hello, how are you?"
source_language = "en"
target_language = "es"
translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
print("Translated Text:", translated_text)
```

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue if you encounter any problems or have suggestions for improvement.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Note:** Replace `"your-api-key"` with your actual Anthropic API key.