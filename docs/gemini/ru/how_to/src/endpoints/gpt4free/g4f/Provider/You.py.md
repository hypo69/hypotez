### Как использовать блок кода You.py
=========================================================================================

Описание
-------------------------
Этот код определяет класс `You`, который предоставляет интерфейс для взаимодействия с сервисом You.com для генерации текста и изображений. Он поддерживает различные модели, включая `gpt-4o-mini`, `dall-e` и другие, а также позволяет загружать изображения для использования в запросах. Класс использует асинхронные запросы для взаимодействия с API You.com и предоставляет методы для создания асинхронного генератора ответов и загрузки файлов.

Шаги выполнения
-------------------------
1. **Инициализация класса `You`**:
   - Определяются основные атрибуты класса, такие как `label`, `url`, `working`, `default_model`, `image_models` и `models`.
   - Устанавливаются значения по умолчанию для модели и модели для генерации изображений.
   - Инициализируются атрибуты для хранения cookies и telemetry IDs.

2. **Создание асинхронного генератора `create_async_generator`**:
   - Функция принимает параметры, такие как `model` (модель для использования), `messages` (сообщения для отправки), `stream` (флаг потоковой передачи), `image` (изображение для загрузки), `image_name` (имя изображения), `proxy` (прокси-сервер), `timeout` (время ожидания), `chat_mode` (режим чата) и `cookies` (cookies для аутентификации).
   - Определяется режим чата в зависимости от наличия изображения или выбранной модели.
   - Если cookies не предоставлены и режим чата не `default`, пытается получить cookies из домена `.you.com`.
   - Если cookies отсутствуют, запускается браузер для получения cookies с сайта You.com.
   - Создается асинхронная сессия с использованием `StreamSession` для выполнения запросов.
   - Если предоставлено изображение, оно загружается с использованием метода `upload_file`.
   - Формируются заголовки и данные для запроса к API `streamingSearch`.
   - Выполняется GET-запрос к API `streamingSearch` с использованием асинхронной сессии.
   - Полученные данные обрабатываются построчно, и генерируются результаты в зависимости от типа события (`youChatUpdate`, `youChatToken`).
   - Для режима `create` (генерация изображений) извлекаются ссылки на изображения из ответов.

3. **Загрузка файла `upload_file`**:
   - Функция принимает клиента `StreamSession`, cookies, файл в виде байтов и имя файла.
   - Получает одноразовый nonce для загрузки файла с использованием GET-запроса к API `get_nonce`.
   - Формирует данные формы с использованием `FormData`, добавляя файл с указанием типа содержимого и имени файла.
   - Выполняет POST-запрос к API `upload` с данными формы и заголовком `X-Upload-Nonce`.
   - Обрабатывает ответ, извлекая результат в формате JSON и добавляя информацию о имени файла и размере.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.You import You
from src.endpoints.gpt4free.g4f.typing import Messages, ImageType
import asyncio

async def main():
    # Пример использования create_async_generator для текстового запроса
    messages: Messages = [{"role": "user", "content": "Напиши короткий стих о весне."}]
    async for response in You.create_async_generator(model="gpt-4o-mini", messages=messages):
        print(response)

    # Пример использования create_async_generator для запроса с изображением
    # image: ImageType = open("image.jpg", "rb").read()
    # messages: Messages = [{"role": "user", "content": "Опиши, что изображено на картинке."}]
    # async for response in You.create_async_generator(model=You.default_vision_model, messages=messages, image=image, image_name="image.jpg"):
    #     print(response)

    # Пример использования upload_file
    # async with StreamSession() as client:
    #     file = open("image.jpg", "rb").read()
    #     cookies = {}  # Замените на ваши cookies
    #     result = await You.upload_file(client, cookies, file, "image.jpg")
    #     print(result)

if __name__ == "__main__":
    asyncio.run(main())