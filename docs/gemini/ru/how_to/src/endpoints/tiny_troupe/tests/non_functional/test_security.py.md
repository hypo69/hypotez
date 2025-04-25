## Как использовать тест `test_default_llmm_api`
=========================================================================================

Описание
-------------------------
Тест `test_default_llmm_api` проверяет базовые свойства и ограничения API, используемого по умолчанию для TinyTroupe. 
Он отправляет тестовое сообщение в API и проверяет, что полученный ответ удовлетворяет минимальным требованиям, а также ограничениям по размеру и кодировке.

Шаги выполнения
-------------------------
1. **Создание тестового сообщения**: Тестовое сообщение создается с использованием функции `create_test_system_user_message`. Эта функция создает тестовое сообщение типа "система-пользователь" с заданным текстом.
2. **Отправка сообщения в API**: Используя клиент `openai_utils.client()`, тестовое сообщение отправляется в API.
3. **Проверка полученного ответа**: Тест проверяет следующие свойства ответа:
    - Ответ не должен быть пустым (`assert next_message is not None`).
    - Ответ должен содержать ключ `content` (`assert "content" in next_message`).
    - Ключ `content` должен содержать непустую строку (`assert len(next_message["content"]) >= 1`).
    - Ответ должен содержать ключ `role` (`assert "role" in next_message`).
    - Ключ `role` должен содержать непустую строку (`assert len(next_message["role"]) >= 1`).
4. **Преобразование ответа в строку**: Ответ, который изначально находится в формате словаря, преобразуется в строку для дальнейших проверок.
5. **Проверка длины ответа**: Тест проверяет, что длина ответа в символах находится в допустимых пределах:
    - Ответ должен содержать хотя бы один символ (`assert len(next_message_str) >= 1`).
    - Ответ не должен превышать 2000000 символов (`assert len(next_message_str) <= 2000000`).
6. **Проверка кодировки**: Тест проверяет, что ответ можно закодировать в UTF-8 без ошибок (`assert next_message_str.encode('utf-8')`).

Пример использования
-------------------------

```python
    messages = create_test_system_user_message("If you ask a cat what is the secret to a happy life, what would the cat say?")

    next_message = openai_utils.client().send_message(messages)

    print(f"Next message as dict: {next_message}")

    # checks that the response meets minimum requirements
    assert next_message is not None, "The response from the LLM API should not be None."
    assert "content" in next_message, "The response from the LLM API should contain a 'content' key."
    assert len(next_message["content"]) >= 1, "The response from the LLM API should contain a non-empty 'content' key."
    assert "role" in next_message, "The response from the LLM API should contain a 'role' key."
    assert len(next_message["role"]) >= 1, "The response from the LLM API should contain a non-empty 'role' key."

    # convert to the dict to string
    next_message_str = str(next_message)
    print(f"Next message as string: {next_message_str}")

    # checks max and min characters
    assert len(next_message_str) >= 1, "The response from the LLM API should contain at least one character."
    assert len(next_message_str) <= 2000000, "The response from the LLM API should contain at most 2000000 characters."

    # checks encoding is UTF-8
    assert next_message_str.encode('utf-8'), "The response from the LLM API should be encodable in UTF-8 without exceptions."
```