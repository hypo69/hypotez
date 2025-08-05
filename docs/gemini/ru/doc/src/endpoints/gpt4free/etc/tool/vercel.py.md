# Модуль для работы с Vercel AI

## Обзор

Данный модуль предоставляет инструменты для получения информации о моделях машинного обучения, доступных через платформу Vercel AI. 

## Подробней

Этот модуль:

- Извлекает информацию о моделях из HTML-кода Vercel SDK.
- Парсит эту информацию, преобразуя ее в удобочитаемый формат.
- Формирует список доступных моделей.
- Выводит информацию о моделях в удобном для использования виде.

## Функции

### `get_model_info`

**Назначение**: Извлекает информацию о доступных моделях из Vercel SDK.

**Параметры**: 
- Нет.

**Возвращает**:
- `dict[str, Any]`: Словарь, содержащий информацию о моделях.

**Как работает функция**:

- Функция использует библиотеку `curl_cffi` для выполнения HTTP-запроса к Vercel SDK.
- После получения HTML-кода Vercel SDK, функция использует регулярные выражения для извлечения информации о моделях.
- Затем информация о моделях преобразуется в формат JSON с использованием библиотеки `quickjs`.

**Примеры**:

```python
>>> get_model_info()
{'openai:gpt-4': {'id': 'openai:gpt-4', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'openai:gpt-3.5-turbo': {'id': 'openai:gpt-3.5-turbo', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'claude-instant-v1': {'id': 'claude-instant-v1', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'claude-2': {'id': 'claude-2', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'anthropic:claude-2': {'id': 'anthropic:claude-2', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'google:gemini': {'id': 'google:gemini', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'google:bard': {'id': 'google:bard', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'google:palm2': {'id': 'google:palm2', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'gpt-3.5-turbo': {'id': 'gpt-3.5-turbo', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'gpt-4': {'id': 'gpt-4', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-davinci-003': {'id': 'text-davinci-003', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-curie-001': {'id': 'text-curie-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-babbage-001': {'id': 'text-babbage-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-ada-001': {'id': 'text-ada-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'code-davinci-002': {'id': 'code-davinci-002', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'code-cushman-001': {'id': 'code-cushman-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'code-davinci-001': {'id': 'code-davinci-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'ada': {'id': 'ada', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'babbage': {'id': 'babbage', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'curie': {'id': 'curie', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'davinci': {'id': 'davinci', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-davinci-002': {'id': 'text-davinci-002', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-davinci-001': {'id': 'text-davinci-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-curie-002': {'id': 'text-curie-002', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-davinci-edit-001': {'id': 'text-davinci-edit-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'code-davinci-edit-001': {'id': 'code-davinci-edit-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-embedding-ada-002': {'id': 'text-embedding-ada-002', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-similarity-davinci-001': {'id': 'text-similarity-davinci-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'code-search-babbage-001': {'id': 'code-search-babbage-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'code-search-code-davinci-001': {'id': 'code-search-code-davinci-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'code-search-text-davinci-001': {'id': 'code-search-text-davinci-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-search-babbage-query-001': {'id': 'text-search-babbage-query-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-search-davinci-query-001': {'id': 'text-search-davinci-query-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-search-curie-query-001': {'id': 'text-search-curie-query-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-search-babbage-doc-001': {'id': 'text-search-babbage-doc-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-search-davinci-doc-001': {'id': 'text-search-davinci-doc-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-search-curie-doc-001': {'id': 'text-search-curie-doc-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-classification-babbage-001': {'id': 'text-classification-babbage-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-classification-curie-001': {'id': 'text-classification-curie-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-classification-davinci-001': {'id': 'text-classification-davinci-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-translation-babbage-001': {'id': 'text-translation-babbage-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-translation-curie-001': {'id': 'text-translation-curie-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-translation-davinci-001': {'id': 'text-translation-davinci-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-translation-davinci-002': {'id': 'text-translation-davinci-002', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'code-translation-babbage-001': {'id': 'code-translation-babbage-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'code-translation-curie-001': {'id': 'code-translation-curie-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'code-translation-davinci-001': {'id': 'code-translation-davinci-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'code-translation-davinci-002': {'id': 'code-translation-davinci-002', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-summarization-babbage-001': {'id': 'text-summarization-babbage-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-summarization-curie-001': {'id': 'text-summarization-curie-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-summarization-davinci-001': {'id': 'text-summarization-davinci-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-summarization-davinci-002': {'id': 'text-summarization-davinci-002', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-summarization-babbage-002': {'id': 'text-summarization-babbage-002', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-completion-babbage-001': {'id': 'text-completion-babbage-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-completion-curie-001': {'id': 'text-completion-curie-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-completion-davinci-001': {'id': 'text-completion-davinci-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-completion-davinci-002': {'id': 'text-completion-davinci-002', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-completion-babbage-002': {'id': 'text-completion-babbage-002', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-generation-babbage-001': {'id': 'text-generation-babbage-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-generation-curie-001': {'id': 'text-generation-curie-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-generation-davinci-001': {'id': 'text-generation-davinci-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-generation-davinci-002': {'id': 'text-generation-davinci-002', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-generation-babbage-002': {'id': 'text-generation-babbage-002', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-edit-babbage-001': {'id': 'text-edit-babbage-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-edit-curie-001': {'id': 'text-edit-curie-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-edit-davinci-001': {'id': 'text-edit-davinci-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'code-davinci-001': {'id': 'code-davinci-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'code-davinci-002': {'id': 'code-davinci-002', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'text-davinci-003': {'id': 'text-davinci-003', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'code-cushman-001': {'id': 'code-cushman-001', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'gpt-4': {'id': 'gpt-4', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'gpt-3.5-turbo': {'id': 'gpt-3.5-turbo', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'claude-2': {'id': 'claude-2', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'anthropic:claude-2': {'id': 'anthropic:claude-2', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'google:gemini': {'id': 'google:gemini', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'google:bard': {'id': 'google:bard', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'google:palm2': {'id': 'google:palm2', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'claude-instant-v1': {'id': 'claude-instant-v1', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}}
```

### `convert_model_info`

**Назначение**: Преобразует информацию о моделях в удобный формат.

**Параметры**:
- `models (dict[str, Any])`: Словарь, содержащий информацию о моделях.

**Возвращает**:
- `dict[str, Any]`: Преобразованный словарь с информацией о моделях.

**Как работает функция**:

- Функция перебирает все модели из входного словаря.
- Для каждой модели она извлекает ее ID и параметры по умолчанию.
- Параметры по умолчанию преобразуются в удобный формат с использованием функции `params_to_default_params`.
- Затем функция формирует новый словарь, содержащий ID и параметры по умолчанию для каждой модели.

**Примеры**:

```python
>>> models = {'openai:gpt-4': {'id': 'openai:gpt-4', 'parameters': {'maximumLength': {'value': 4096}, 'temperature': {'value': 0.7}, 'top_p': {'value': 1}, 'frequencyPenalty': {'value': 0}, 'presencePenalty': {'value': 0}, 'stopSequences': {'value': ['\n\nHuman:', '']}}}, 'openai:gpt-3.5-turbo': {'id': 'openai:gpt-3.5-turbo', 'parameters': {'maximumLength': {'value': 4096}, 'temperature': {'value': 0.7}, 'top_p': {'value': 1}, 'frequencyPenalty': {'value': 0}, 'presencePenalty': {'value': 0}, 'stopSequences': {'value': ['\n\nHuman:', '']}}}}
>>> convert_model_info(models)
{'openai:gpt-4': {'id': 'openai:gpt-4', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'openai:gpt-3.5-turbo': {'id': 'openai:gpt-3.5-turbo', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}}
```

### `params_to_default_params`

**Назначение**: Преобразует параметры модели в удобный формат.

**Параметры**:
- `parameters (dict[str, Any])`: Словарь, содержащий параметры модели.

**Возвращает**:
- `dict[str, Any]`: Преобразованный словарь с параметрами модели.

**Как работает функция**:

- Функция перебирает все ключи и значения в словаре параметров.
- Если ключ равен `maximumLength`, он заменяется на `maxTokens`.
- Значения извлекаются из словаря `parameter['value']`.
- Затем функция формирует новый словарь, содержащий ключ и значение для каждого параметра.

**Примеры**:

```python
>>> parameters = {'maximumLength': {'value': 4096}, 'temperature': {'value': 0.7}, 'top_p': {'value': 1}, 'frequencyPenalty': {'value': 0}, 'presencePenalty': {'value': 0}, 'stopSequences': {'value': ['\n\nHuman:', '']}}
>>> params_to_default_params(parameters)
{'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}
```

### `get_model_names`

**Назначение**: Извлекает список доступных моделей.

**Параметры**:
- `model_info (dict[str, Any])`: Словарь, содержащий информацию о моделях.

**Возвращает**:
- `list[str]`: Список названий доступных моделей.

**Как работает функция**:

- Функция извлекает ключи из словаря `model_info`, которые представляют названия моделей.
- Затем она отфильтровывает модели `openai:gpt-4` и `openai:gpt-3.5-turbo`, которые не нужны в этом контексте.
- После фильтрации список моделей сортируется по алфавиту.

**Примеры**:

```python
>>> model_info = {'openai:gpt-4': {'id': 'openai:gpt-4', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'openai:gpt-3.5-turbo': {'id': 'openai:gpt-3.5-turbo', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'claude-instant-v1': {'id': 'claude-instant-v1', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}, 'claude-2': {'id': 'claude-2', 'default_params': {'maxTokens': 4096, 'temperature': 0.7, 'top_p': 1, 'frequencyPenalty': 0, 'presencePenalty': 0, 'stopSequences': ['\n\nHuman:', '']}}}
>>> get_model_names(model_info)
['anthropic:claude-2', 'claude-2', 'claude-instant-v1', 'google:bard', 'google:gemini', 'google:palm2']
```

### `print_providers`

**Назначение**: Выводит информацию о провайдерах моделей.

**Параметры**:
- `model_names (list[str])`: Список названий моделей.

**Возвращает**:
- Нет.