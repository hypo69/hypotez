### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода определяет различные классы и функции, предназначенные для обработки и форматирования ответов от различных сервисов, особенно в контексте работы с медиа-контентом, URL-адресами и текстом. Он включает в себя функции для квотирования URL-адресов и заголовков, форматирования ссылок и изображений в Markdown, а также классы для представления различных типов ответов, таких как JSON, скрытые ответы, сообщения о завершении, вызовы инструментов, использование, результаты аутентификации, заголовки, отладочные сообщения, рассуждения, источники, YouTube-видео, аудио, базовые и JSON-беседы, синтезированные данные, предлагаемые последующие действия, запросы на вход, медиа-ответы, ответы изображений, видео-ответы, превью изображений, ответы превью, параметры и информацию о провайдере.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются различные модули, такие как `re`, `base64`, `typing`, `abc`, и `urllib.parse`.

2. **Определение функций для обработки URL и текста**:
   - `quote_url(url: str) -> str`: Экранирует части URL, сохраняя структуру домена. Функция проверяет, есть ли символы `%` в URL, и если есть, то сначала убирает экранирование, чтобы избежать двойного экранирования. Затем разделяет URL на части (протокол и остальная часть), экранирует только путь, сохраняя протокол и домен.
   - `quote_title(title: str) -> str`: Нормализует пробелы в заголовке, заменяя множественные пробелы на одинарные.
   - `format_link(url: str, title: Optional[str] = None) -> str`: Форматирует URL и заголовок как ссылку в Markdown. Если заголовок не указан, пытается извлечь его из URL.
   - `format_image(image: str, alt: str, preview: Optional[str] = None) -> str`: Форматирует изображение как строку в Markdown, используя URL изображения, альтернативный текст и URL превью (если указан).
   - `format_images_markdown(images: Union[str, List[str]], alt: str, preview: Union[str, List[str]] = None) -> str`: Форматирует одно или несколько изображений как строку в Markdown.

3. **Определение базовых классов для представления ответов**:
   - `ResponseType`: Абстрактный базовый класс для всех типов ответов. Определяет абстрактный метод `__str__`, который должен возвращать строковое представление ответа.
   - `JsonMixin`: Класс, предоставляющий функциональность для работы с JSON. Позволяет инициализировать объект с помощью именованных аргументов и преобразовывать объект в словарь.
   - `RawResponse(ResponseType, JsonMixin)`: Пустой класс для представления необработанных ответов.
   - `HiddenResponse(ResponseType)`: Базовый класс для скрытых ответов, возвращает пустую строку при преобразовании в строку.
   - `FinishReason(JsonMixin, HiddenResponse)`: Класс для представления причины завершения запроса.
   - `ToolCalls(HiddenResponse)`: Класс для представления вызовов инструментов.
   - `Usage(JsonMixin, HiddenResponse)`: Класс для представления информации об использовании ресурсов.
   - `AuthResult(JsonMixin, HiddenResponse)`: Класс для представления результатов аутентификации.
   - `TitleGeneration(HiddenResponse)`: Класс для представления сгенерированного заголовка.
   - `DebugResponse(HiddenResponse)`: Класс для представления отладочных сообщений.
   - `Reasoning(ResponseType)`: Класс для представления рассуждений, включает токен, статус и состояние "размышления".
   - `Sources(ResponseType)`: Класс для представления источников, включает список URL-адресов и заголовков.
   - `YouTube(HiddenResponse)`: Класс для представления YouTube-видео, включает список идентификаторов видео.
   - `AudioResponse(ResponseType)`: Класс для представления аудиоданных, позволяет преобразовать данные в URI.
   - `BaseConversation(ResponseType)`: Базовый класс для представлений бесед.
   - `JsonConversation(BaseConversation, JsonMixin)`: Класс для представления бесед в формате JSON.
   - `SynthesizeData(HiddenResponse, JsonMixin)`: Класс для представления синтезированных данных.
   - `SuggestedFollowups(HiddenResponse)`: Класс для представления предложенных последующих действий.
   - `RequestLogin(HiddenResponse)`: Класс для представления запроса на вход в систему.
   - `MediaResponse(ResponseType)`: Базовый класс для медиа-ответов, включает URL-адреса и альтернативный текст.
   - `ImageResponse(MediaResponse)`: Класс для представления ответов изображений.
   - `VideoResponse(MediaResponse)`: Класс для представления ответов видео.
   - `ImagePreview(ImageResponse)`: Класс для предварительного просмотра изображений.
   - `PreviewResponse(HiddenResponse)`: Класс для представления ответов предварительного просмотра.
   - `Parameters(ResponseType, JsonMixin)`: Класс для представления параметров.
   - `ProviderInfo(JsonMixin, HiddenResponse)`: Класс для представления информации о провайдере.

Пример использования
-------------------------

```python
from typing import List, Dict, Optional

# Пример использования функций форматирования URL и текста
url = "https://www.example.com/path?param1=value1&param2=value2"
title = "Example Title with  multiple   spaces"
formatted_link = format_link(url, title)
print(f"Formatted link: {formatted_link}")

image_url = "https://www.example.com/image.jpg"
alt_text = "Example Image"
formatted_image = format_image(image_url, alt_text)
print(f"Formatted image: {formatted_image}")

images = ["https://www.example.com/image1.jpg", "https://www.example.com/image2.jpg"]
alt_text = "Example Images"
formatted_images = format_images_markdown(images, alt_text)
print(f"Formatted images: {formatted_images}")

# Пример использования классов для представления ответов
from typing import List

sources: List[Dict[str, str]] = [{"url": "https://www.example.com/source1", "title": "Source 1"}, {"url": "https://www.example.com/source2", "title": "Source 2"}]
sources_response = Sources(sources)
print(f"Sources response: {sources_response}")

youtube_ids: List[str] = ["video_id_1", "video_id_2"]
youtube_response = YouTube(youtube_ids)
print(f"YouTube response: {youtube_response.to_string()}")

audio_data = b"audio data bytes"
audio_response = AudioResponse(audio_data)
print(f"Audio response: {audio_response}")

image_response = ImageResponse(urls=["https://example.com/image1.jpg", "https://example.com/image2.jpg"], alt="Example Images", options={"preview": "https://example.com/preview/{image}"})
print(f"Image response: {image_response}")