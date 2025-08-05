## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода представляет класс `StabilityAI_SD35Large`, который реализует асинхронный генератор изображений, основанный на модели StabilityAI SD-3.5-Large, размещенной на платформе Hugging Face Spaces. 

Шаги выполнения
-------------------------
1. **Инициализация класса**: Создается экземпляр класса `StabilityAI_SD35Large`.
2. **Создание асинхронного генератора**: Вызывается метод `create_async_generator` класса, который возвращает асинхронный генератор (`AsyncResult`).
3. **Передача параметров**: В метод `create_async_generator` передаются параметры, такие как:
    - `model`: имя модели (например, `'stabilityai-stable-diffusion-3.5-large'`).
    - `messages`: список сообщений, которые будут использоваться для генерации изображения.
    - `prompt`: текст запроса к модели.
    - `negative_prompt`: текст, описывающий, что не должно быть на изображении.
    - `api_key`: ключ API для доступа к сервису StabilityAI.
    - `proxy`: прокси-сервер (опционально).
    - `aspect_ratio`: соотношение сторон изображения (например, `'1:1'`).
    - `width`, `height`: ширина и высота изображения (в пикселях).
    - `guidance_scale`: параметр, управляющий силой подсказок.
    - `num_inference_steps`: количество шагов генерации.
    - `seed`: начальное значение для генератора случайных чисел.
    - `randomize_seed`: флаг, определяющий, нужно ли случайным образом генерировать начальное значение для генератора случайных чисел.
4. **Отправка запроса**: Класс отправляет запрос к API StabilityAI с заданными параметрами.
5. **Обработка ответа**: Класс обрабатывает ответ от API, генерируя асинхронный генератор, который последовательно выдает `ImagePreview` (предварительный просмотр) или `ImageResponse` (полное изображение).

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.StabilityAI_SD35Large import StabilityAI_SD35Large

async def generate_image(prompt: str, api_key: str, **kwargs):
    provider = StabilityAI_SD35Large()
    async_generator = await provider.create_async_generator(
        model='stabilityai-stable-diffusion-3.5-large',
        messages=[{'role': 'user', 'content': prompt}],
        api_key=api_key,
        **kwargs
    )
    async for image in async_generator:
        if isinstance(image, ImagePreview):
            print(f"Предварительный просмотр: {image.url}")
        else:
            print(f"Полное изображение: {image.url}")

# Пример вызова функции
await generate_image(prompt='Кошка, сидящая на облаке', api_key='your_api_key')
```