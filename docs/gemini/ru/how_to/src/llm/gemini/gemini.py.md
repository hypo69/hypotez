### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет класс `GoogleGenerativeAi` для взаимодействия с моделями Google Gemini. Он включает в себя функциональность для инициализации модели, ведения чата, загрузки файлов и описания изображений.

Шаги выполнения
-------------------------
1.  **Инициализация модели**: Класс `GoogleGenerativeAi` инициализируется с использованием API-ключа, имени модели и конфигурации генерации.
2.  **Запуск сеанса чата**: Функция `_start_chat` запускает новый сеанс чата с моделью, учитывая наличие системной инструкции.
3.  **Сохранение истории чата**: Функция `_save_chat_history` асинхронно сохраняет историю чата в JSON-файл.
4.  **Загрузка истории чата**: Функция `_load_chat_history` асинхронно загружает историю чата из JSON-файла.
5.  **Очистка истории чата**: Функция `clear_history` очищает историю чата как в памяти, так и удаляет соответствующий JSON-файл.
6.  **Обработка чат-запросов**: Функция `chat` обрабатывает запросы пользователя, управляет историей и возвращает ответ модели.
7.  **Отправка текстовых запросов**: Функция `ask` синхронно отправляет текстовый запрос модели и возвращает ответ.
8.  **Асинхронная отправка текстовых запросов**: Функция `ask_async` асинхронно отправляет текстовый запрос модели и возвращает ответ.
9.  **Описание изображений**: Функция `describe_image` отправляет изображение в модель Gemini Pro Vision и возвращает текстовое описание.
10. **Загрузка файлов**: Функция `upload_file` асинхронно загружает файл в Google AI File API.

Пример использования
-------------------------

```python
    import asyncio
    from pathlib import Path
    from src import gs
    from src.llm.gemini.gemini import GoogleGenerativeAi
    from src.logger import logger

    async def main():
        # Проверка наличия ключа API
        if not gs.credentials.gemini.api_key:
            logger.error("Ключ API Gemini не найден в gs.credentials.gemini.api_key.")
            return

        # Инициализация LLM
        system_instruction = 'Ты - полезный ассистент. Отвечай на все вопросы кратко'
        model_name = 'gemini-pro'  # Пример имени модели, замените при необходимости
        try:
            llm = GoogleGenerativeAi(
                api_key=gs.credentials.gemini.api_key,
                model_name=model_name,  # Передаем имя модели
                system_instruction=system_instruction
            )
        except Exception as init_ex:
            logger.error(f"Не удалось инициализировать GoogleGenerativeAi: {init_ex}")
            return

        # Пример описания изображения
        image_path = Path('test.jpg')  # Замените на путь к вашему изображению

        if not image_path.is_file():
            logger.info(
                f"Файл изображения {image_path} не существует. Поместите файл с таким именем в корневую папку."
            )
        else:
            # Пример 1: Запрос описания в JSON
            prompt_json = """Проанализируй это изображение. Выдай ответ в формате JSON,
            где ключом будет имя объекта, а значением его описание.
             Если есть люди, опиши их действия."""

            description_json = llm.describe_image(image_path, prompt=prompt_json)  # describe_image синхронный
            if description_json:
                logger.info("Описание изображения (запрос JSON):")
                logger.info(description_json)
            else:
                logger.info("Не удалось получить описание изображения (запрос JSON).")

        # Пример загрузки файла
        file_path_txt = Path('test.txt')
        try:
            with open(file_path_txt, 'w', encoding='utf-8') as f:
                f.write("Hello, Gemini File API!")
            logger.info(f"Тестовый файл {file_path_txt} создан.")

            # Асинхронная загрузка файла
            file_upload_response = await llm.upload_file(file_path_txt, 'test_file_from_sdk.txt')
            if file_upload_response:
                logger.info("Ответ API на загрузку файла:")
                logger.info(file_upload_response)  # Логгируем ответ API
            else:
                logger.error("Не удалось загрузить файл.")

        except IOError as e:
            logger.error(f"Ошибка при создании тестового файла {file_path_txt}: {e}")
        except Exception as e:
            logger.error(f"Ошибка при загрузке файла: {e}")
        finally:
            # Опционально: удаление тестового файла
            if file_path_txt.exists():
                try:
                    file_path_txt.unlink()
                    logger.info(f"Тестовый файл {file_path_txt} удален.")
                except OSError as e:
                    logger.error(f"Не удалось удалить тестовый файл {file_path_txt}: {e}")

        # Пример чата
        logger.info("\nНачало сеанса чата. Введите 'exit' для выхода.")
        chat_session_name = f'chat_session_{gs.now}'  # Уникальное имя для сессии чата

        while True:
            try:
                user_message = input("You: ")
            except EOFError:  # Обработка Ctrl+D/EOF
                logger.info("\nЗавершение чата по EOF.")
                break
            if user_message.lower() == 'exit':
                logger.info("Завершение чата по команде пользователя.")
                break

            # Асинхронный вызов чата
            llm_message = await llm.chat(user_message, chat_name=chat_session_name)
            if llm_message:
                # Используем logger для вывода ответа Gemini
                logger.info(f"Gemini: {llm_message}")
            else:
                # Сообщение об ошибке уже должно быть в логах из метода chat
                logger.warning("Gemini: Не удалось получить ответ.")

    if __name__ == "__main__":
        asyncio.run(main())