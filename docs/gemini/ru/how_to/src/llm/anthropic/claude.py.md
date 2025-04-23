### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет класс `ClaudeClient`, который позволяет взаимодействовать с API Claude для выполнения таких задач, как генерация текста, анализ тональности и перевод текста. Класс инициализируется с использованием API-ключа и предоставляет методы для выполнения различных операций с использованием API Claude.

Шаги выполнения
-------------------------
1. **Инициализация клиента Claude**:
   - Создайте экземпляр класса `ClaudeClient`, передав свой API-ключ в качестве аргумента.
   - `self.client = anthropic.Client(api_key)`: Инициализируется клиент Claude с предоставленным API-ключом.

2. **Генерация текста**:
   - Вызовите метод `generate_text`, передав запрос (`prompt`) и максимальное количество токенов для генерации (`max_tokens_to_sample`).
   - `response = self.client.completion(...)`: Отправляет запрос в API Claude и получает ответ.
   - `return response['completion']`: Извлекает сгенерированный текст из ответа.

3. **Анализ тональности**:
   - Вызовите метод `analyze_sentiment`, передав текст для анализа.
   - `response = self.client.completion(...)`: Отправляет запрос в API Claude для анализа тональности и получает ответ.
   - `return response['completion']`: Извлекает результат анализа тональности из ответа.

4. **Перевод текста**:
   - Вызовите метод `translate_text`, передав текст для перевода, код исходного языка и код целевого языка.
   - `response = self.client.completion(...)`: Отправляет запрос в API Claude для перевода текста и получает ответ.
   - `return response['completion']`: Извлекает переведенный текст из ответа.

Пример использования
-------------------------

```python
    import anthropic
    from typing import Optional


    class ClaudeClient:
        def __init__(self, api_key: str) -> None:
            """
            Инициализирует клиент Claude с предоставленным API-ключом.

            Args:
                api_key (str): API-ключ для доступа к сервисам Claude.

            Example:
                >>> claude_client = ClaudeClient(\'your_api_key\')
            """
            self.client = anthropic.Client(api_key)

        def generate_text(self, prompt: str, max_tokens_to_sample: int = 100) -> str:
            """
            Генерирует текст на основе предоставленного запроса.

            Args:
                prompt (str): Запрос для генерации текста.
                max_tokens_to_sample (int, optional): Максимальное количество токенов для генерации. По умолчанию 100.

            Returns:
                str: Сгенерированный текст.

            Example:
                >>> claude_client.generate_text(\'Write a short story.\')
                \'A short story about...\'
            """
            response = self.client.completion(
                prompt=prompt,
                model='claude-v1',
                max_tokens_to_sample=max_tokens_to_sample,
                stop_sequences=['\\n\\nHuman:']
            )
            return response['completion']

        def analyze_sentiment(self, text: str) -> str:
            """
            Анализирует тональность предоставленного текста.

            Args:
                text (str): Текст для анализа.

            Returns:
                str: Результат анализа тональности.

            Example:
                >>> claude_client.analyze_sentiment(\'I am very happy!\')
                \'Positive\'
            """
            response = self.client.completion(
                prompt=f'Analyze the sentiment of the following text: {text}',
                model='claude-v1',
                max_tokens_to_sample=50,
                stop_sequences=['\\n\\nHuman:']
            )
            return response['completion']

        def translate_text(self, text: str, source_language: str, target_language: str) -> str:
            """
            Переводит предоставленный текст с исходного языка на целевой язык.

            Args:
                text (str): Текст для перевода.
                source_language (str): Код исходного языка.
                target_language (str): Код целевого языка.

            Returns:
                str: Переведенный текст.

            Example:
                >>> claude_client.translate_text(\'Hello\', \'en\', \'es\')
                \'Hola\'
            """
            response = self.client.completion(
                prompt=f'Translate the following text from {source_language} to {target_language}: {text}',
                model='claude-v1',
                max_tokens_to_sample=100,
                stop_sequences=['\\n\\nHuman:']
            )
            return response['completion']


    # Пример использования класса
    if __name__ == '__main__':
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