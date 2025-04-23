### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код реализует взаимодействие с Microsoft Designer для генерации изображений на основе текстового запроса. Он включает в себя получение токена доступа и user-agent, необходимых для аутентификации, формирование запроса к API Microsoft Designer и обработку ответа для получения URL-адресов сгенерированных изображений.

Шаги выполнения
-------------------------
1. **Получение токена доступа и User-Agent**:
   - Функция `generate` вызывает `readHAR` для извлечения токена доступа и user-agent из HAR-файла (HTTP Archive).
   - Если HAR-файл не содержит необходимых данных или отсутствует, вызывается `get_access_token_and_user_agent` для получения этих данных через автоматизированный браузер.

2. **Формирование запроса к API Microsoft Designer**:
   - Функция `create_images` формирует URL-адрес API и заголовки запроса, включая токен доступа и user-agent.
   - Подготавливает `form_data` с параметрами запроса, такими как текст запроса (`prompt`), размер изображения (`image_size`) и случайное начальное число (`seed`).

3. **Отправка запроса и обработка ответа**:
   - Использует `aiohttp.ClientSession` для отправки POST-запроса к API Microsoft Designer.
   - Проверяет статус ответа с помощью `raise_for_status`.
   - Извлекает данные ответа в формате JSON.

4. **Опрос API для получения изображений**:
   - Организует цикл опроса API, используя URL-адрес и метаданные из предыдущего ответа.
   - Отправляет POST-запросы с интервалом, указанным в `polling_meta_data`.
   - Извлекает URL-адреса изображений из ответа и возвращает их.

5. **Чтение HAR-файлов**:
   - Функция `readHAR` ищет HAR-файлы в указанных директориях.
   - Перебирает записи в HAR-файле в поисках URL-адреса, начинающегося с "https://designerapp.officeapps.live.com".
   - Извлекает токен авторизации и user-agent из заголовков запроса.

6. **Получение токена через автоматизированный браузер**:
   - Функция `get_access_token_and_user_agent` запускает автоматизированный браузер (Playwright).
   - Переходит по указанному URL-адресу и извлекает user-agent.
   - Выполняет JavaScript-код для извлечения токена доступа из `localStorage`.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.needs_auth.MicrosoftDesigner import MicrosoftDesigner
import asyncio

async def main():
    prompt = "A futuristic cityscape at sunset"
    image_size = "1024x1024"
    proxy = None  # Замените на ваш прокси, если необходимо

    try:
        # Генерирует изображения
        image_response = await MicrosoftDesigner.generate(prompt, image_size, proxy)
        
        if image_response and image_response.images:
            print("Images generated successfully:")
            for image_url in image_response.images:
                print(image_url)
        else:
            print("No images were generated.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())