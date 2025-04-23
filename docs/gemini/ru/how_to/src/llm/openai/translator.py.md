### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода содержит функцию `translate`, которая использует OpenAI API для перевода текста с одного языка на другой. Он формирует запрос к OpenAI с исходным текстом и информацией о языках, а затем возвращает переведенный текст.

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек**:
   - Импортируется библиотека `openai` для взаимодействия с OpenAI API.
   - Импортируется модуль `gs` для получения учетных данных.
   - Импортируется модуль `logger` из `src.logger.logger` для логирования ошибок.

2. **Настройка OpenAI API**:
   - Устанавливается ключ API для OpenAI из учетных данных, хранящихся в `gs.credentials.openai`.

3. **Определение функции `translate(text, source_language, target_language)`**:
   - Функция принимает три аргумента:
     - `text` (str): Текст, который необходимо перевести.
     - `source_language` (str): Язык исходного текста.
     - `target_language` (str): Язык, на который требуется перевести текст.

4. **Формирование запроса к OpenAI API**:
   - Создается строка `prompt`, содержащая инструкцию для перевода текста из исходного языка в целевой. Текст для перевода включается в `prompt`.

5. **Отправка запроса к OpenAI API и обработка ответа**:
   - В блоке `try` происходит следующее:
     - Отправляется запрос к OpenAI API с использованием метода `openai.Completion.create`.
     - Указываются параметры запроса:
       - `engine`: Используемая модель OpenAI (в данном случае "text-davinci-003").
       - `prompt`: Сформированный запрос на перевод.
       - `max_tokens`: Максимальное количество токенов в ответе.
       - `n`: Количество возвращаемых вариантов перевода.
       - `stop`: Условие остановки генерации.
       - `temperature`: Параметр, определяющий случайность выбора токенов.
     - Функция `openai.Completion.create` возвращает объект `response`, содержащий результат запроса.
     - Извлекается переведенный текст из ответа API: `translation = response.choices[0].text.strip()`.
     - Функция возвращает переведенный текст.

6. **Обработка ошибок**:
   - Если в процессе выполнения запроса или обработки ответа возникает исключение, оно перехватывается в блоке `except`.
   - В случае ошибки:
     - Функция логирует сообщение об ошибке с использованием `logger.error("Error during translation", ex)`.
     - Функция возвращает `None`.

Пример использования
-------------------------

```python
import openai
from src import gs
from src.logger.logger import logger

openai.api_key = gs.credentials.openai

def translate(text: str, source_language: str, target_language: str) -> str | None:
    """
    Функция выполняет перевод текста с использованием OpenAI API.

    Args:
        text (str): Текст для перевода.
        source_language (str): Язык исходного текста.
        target_language (str): Язык для перевода.

    Returns:
        str | None: Переведённый текст, или None в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при выполнении запроса к OpenAI API.

    Example:
        >>> source_text = "Привет, как дела?"
        >>> source_language = "Russian"
        >>> target_language = "English"
        >>> translation = translate(source_text, source_language, target_language)
        >>> if translation:
        ...     print(f"Переведенный текст: {translation}")
        ... else:
        ...     print("Не удалось выполнить перевод.")
    """
    # Формирование запроса к OpenAI API
    prompt = (
        f"Translate the following text from {source_language} to {target_language}:\\n\\n"
        f"{text}\\n\\n"
        f"Translation:"
    )

    try:
        # Отправка запроса к OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",  # Укажите нужную модель
            prompt=prompt,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.3,
        )

        # Функция извлекает перевод из ответа API
        translation = response.choices[0].text.strip()
        return translation
    except Exception as ex:
        # Логирование ошибки
        logger.error("Ошибка во время перевода", ex, exc_info=True)
        return None

# Пример использования:
if __name__ == "__main__":
    source_text = "Привет, как дела?"
    source_language = "Russian"
    target_language = "English"
    translation = translate(source_text, source_language, target_language)
    if translation:
        print(f"Переведенный текст: {translation}")
    else:
        print("Не удалось выполнить перевод.")