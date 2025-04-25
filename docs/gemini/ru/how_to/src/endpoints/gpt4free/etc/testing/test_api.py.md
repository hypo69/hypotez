## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода реализует взаимодействие с API OpenAI для генерации текста с использованием модели gpt-3.5-turbo. 

Шаги выполнения
-------------------------
1. **Инициализация API ключа**:
    -  В начале кода устанавливается ключ API OpenAI. 
    - Если вы используете встраивание текста, установите  токен Hugging Face в качестве API-ключа.  
    - Если не используете встраивание, оставьте ключ пустым.
    - Можно также указать базовый URL API, например, для локальной среды разработки.
2. **Определение функции `main`**:
    - Функция  `main`  содержит код для взаимодействия с API OpenAI.
3. **Вызов API OpenAI**:
    - Используется функция  `openai.ChatCompletion.create`  для отправки запроса к модели gpt-3.5-turbo.
    - В качестве входных данных передается список сообщений с ролью "user" и текстом запроса "write a poem about a tree".
    - Параметр `stream=True` позволяет получать ответ частями (потоком).
4. **Обработка ответа**:
    - Проверяется тип ответа. 
    - Если ответ является словарем (`dict`), то ответ не передается потоком. В этом случае  выводится текст из поля `content` первого ответа (`response.choices[0].message.content`). 
    - Если ответ является объектом потока, то в цикле обрабатываются порции ответа (`for token in response`). 
    -  Для каждой порции ответа выводится текст из поля `content` (`token["choices"][0]["delta"].get("content")`).
5. **Запуск функции `main`**:
    - Функция  `main`  вызывается, если код выполняется в качестве основного скрипта (`if __name__ == "__main__":`).

Пример использования
-------------------------

```python
import openai

# Set your Hugging Face token as the API key if you use embeddings
# If you don't use embeddings, leave it empty
openai.api_key = "YOUR_HUGGING_FACE_TOKEN"  # Replace with your actual token

# Set the API base URL if needed, e.g., for a local development environment
openai.api_base = "http://localhost:1337/v1"

def main():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "write a poem about a tree"}],
        stream=True,
    )
    if isinstance(response, dict):
        # Not streaming
        print(response.choices[0].message.content)
    else:
        # Streaming
        for token in response:
            content = token["choices"][0]["delta"].get("content")
            if content is not None:
                print(content, end="", flush=True)

if __name__ == "__main__":
    main()
```