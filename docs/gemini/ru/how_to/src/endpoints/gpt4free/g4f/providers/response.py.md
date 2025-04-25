## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода предоставляет набор функций для форматирования текста и URL-адресов в виде Markdown, а также несколько классов для представления различных типов ответов от API. 

Шаги выполнения
-------------------------
1. **`quote_url(url: str)`**: Функция принимает URL-адрес в качестве аргумента и возвращает его, закодированный для безопасного использования в Markdown. 
    - Она разделят URL-адрес на протокол, домен и путь.
    - Если URL-адрес является относительным, она кодирует весь URL-адрес.
    - Если URL-адрес является абсолютным, она кодирует только путь.
2. **`quote_title(title: str)`**: Функция принимает заголовок в качестве аргумента и возвращает его с нормализованными пробелами. 
    - Она заменяет несколько пробелов одним.
3. **`format_link(url: str, title: Optional[str] = None)`**:  Функция принимает URL-адрес и необязательный заголовок в качестве аргументов и возвращает их отформатированными как Markdown-ссылка. 
    - Она использует `quote_url` и `quote_title` для кодирования URL-адреса и заголовка.
4. **`format_image(image: str, alt: str, preview: Optional[str] = None)`**: Функция форматирует изображение как Markdown-код.
    - Она принимает URL изображения, альтернативный текст (alt) и необязательный URL для предварительного просмотра.
    - Она использует `quote_url` для кодирования URL-адресов.
5. **`format_images_markdown(images: Union[str, List[str]], alt: str, preview: Union[str, List[str]] = None)`**: Функция форматирует изображение или список изображений как Markdown-код.
    - Она принимает URL изображения или список URL-адресов, альтернативный текст (alt) и необязательный URL для предварительного просмотра или список URL-адресов для предварительного просмотра.
    - Она использует `format_image` для форматирования каждого изображения.
6. **Классы `ResponseType`, `JsonMixin`, `RawResponse`**:  Эти классы используются для представления различных типов ответов от API.
    - `ResponseType` - базовый класс для всех типов ответов.
    - `JsonMixin` - класс для сериализации объектов в JSON.
    - `RawResponse` - класс для представления необработанных ответов.
7. **`FinishReason`, `ToolCalls`, `Usage`, `AuthResult`, `TitleGeneration`, `DebugResponse`, `Reasoning`, `Sources`, `YouTube`, `AudioResponse`, `BaseConversation`, `JsonConversation`, `SynthesizeData`, `SuggestedFollowups`, `RequestLogin`, `MediaResponse`, `ImageResponse`, `VideoResponse`, `ImagePreview`, `PreviewResponse`, `Parameters`, `ProviderInfo`**:  Эти классы реализуют конкретные типы ответов.

Пример использования
-------------------------
```python
from hypotez.src.endpoints.gpt4free.g4f.providers.response import format_link, format_image, format_images_markdown

# Форматирование ссылки
url = "https://example.com/article"
title = "Пример статьи"
link = format_link(url, title)
print(link)  # Вывод: [Пример статьи](https://example.com/article)

# Форматирование изображения
image_url = "https://example.com/image.jpg"
alt_text = "Пример изображения"
image_markdown = format_image(image_url, alt_text)
print(image_markdown)  # Вывод: [![Пример изображения](https://example.com/image.jpg)](https://example.com/image.jpg)

# Форматирование списка изображений
images = ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
alt_text = "Изображение"
images_markdown = format_images_markdown(images, alt_text)
print(images_markdown)  # Вывод: 
# <!-- generated images start -->
# [![#1 Изображение](https://example.com/image1.jpg)](https://example.com/image1.jpg)
# [![#2 Изображение](https://example.com/image2.jpg)](https://example.com/image2.jpg)
# <!-- generated images end -->

```