# Документация модуля `vision_images.py`

## Обзор

Этот модуль демонстрирует, как использовать модель GPT-4 Vision для обработки изображений, как удаленных (по URL), так и локальных (из файла). Модуль использует библиотеку `g4f` для взаимодействия с API и отправки запросов на анализ изображений.

## Подробней

Модуль содержит примеры кода для отправки запросов к модели GPT-4 Vision с использованием библиотеки `g4f`. Он показывает, как загружать изображения как из удаленных источников (через URL), так и из локальных файлов, и отправлять их в модель для анализа.

## Функции

### Отправка запроса на анализ удаленного изображения

```python
remote_image = requests.get("https://raw.githubusercontent.com/xtekky/gpt4free/refs/heads/main/docs/images/cat.jpeg", stream=True).content
response_remote = client.chat.completions.create(
    model=g4f.models.default_vision,
    messages=[
        {"role": "user", "content": "What are on this image?"}
    ],
    image=remote_image
)
print("Response for remote image:")
print(response_remote.choices[0].message.content)
```

**Назначение**: Отправляет запрос на анализ удаленного изображения, загруженного по URL, к модели GPT-4 Vision и выводит полученный ответ.

**Параметры**:
- `remote_image` (bytes): Содержимое изображения, полученное из URL.
- `response_remote` (g4f.ChatCompletion): Ответ от модели GPT-4 Vision.

**Возвращает**:
- `None`: Функция ничего не возвращает явно, но выводит результат запроса в консоль.

**Вызывает исключения**:
- Возможные исключения, связанные с сетевыми запросами (`requests.get`) и обработкой ответов от API `g4f`.

**Как работает функция**:
1. **Загрузка изображения**: Сначала происходит загрузка изображения из удаленного источника с использованием библиотеки `requests`. Изображение загружается как бинарный поток (`stream=True`) и его содержимое сохраняется в переменной `remote_image`.
2. **Отправка запроса**: Затем создается запрос к модели GPT-4 Vision с использованием метода `client.chat.completions.create()`. В запросе указывается модель (`g4f.models.default_vision`), сообщение с вопросом (`"What are on this image?"`) и само изображение (`image=remote_image`).
3. **Обработка ответа**: После получения ответа от модели, он извлекается из объекта `response_remote` и выводится в консоль.

**ASCII flowchart**:

```
Загрузка изображения из URL
    ↓
Создание запроса к GPT-4 Vision с изображением
    ↓
Получение ответа от GPT-4 Vision
    ↓
Вывод ответа в консоль
```

**Примеры**:

```python
import requests
import g4f

# Пример использования
remote_image_url = "https://raw.githubusercontent.com/xtekky/gpt4free/refs/heads/main/docs/images/cat.jpeg"
remote_image = requests.get(remote_image_url, stream=True).content
if remote_image:
    response_remote = client.chat.completions.create(
        model=g4f.models.default_vision,
        messages=[{"role": "user", "content": "Describe this image."}],
        image=remote_image
    )
    print(f"Remote image description: {response_remote.choices[0].message.content}")
else:
    print("Failed to download remote image.")
```

### Отправка запроса на анализ локального изображения

```python
local_image = open("docs/images/cat.jpeg", "rb")
response_local = client.chat.completions.create(
    model=g4f.models.default_vision,
    messages=[
        {"role": "user", "content": "What are on this image?"}
    ],
    image=local_image
)
print("Response for local image:")
print(response_local.choices[0].message.content)
local_image.close()  # Close file after use
```

**Назначение**: Отправляет запрос на анализ локального изображения, загруженного из файла, к модели GPT-4 Vision и выводит полученный ответ.

**Параметры**:
- `local_image` (file): Файловый объект, представляющий локальное изображение.
- `response_local` (g4f.ChatCompletion): Ответ от модели GPT-4 Vision.

**Возвращает**:
- `None`: Функция ничего не возвращает явно, но выводит результат запроса в консоль.

**Вызывает исключения**:
- Возможные исключения, связанные с открытием и чтением файла, а также обработкой ответов от API `g4f`.

**Как работает функция**:
1. **Открытие изображения**: Сначала открывается локальный файл с изображением в бинарном режиме (`"rb"`) с использованием функции `open()`.
2. **Отправка запроса**: Затем создается запрос к модели GPT-4 Vision с использованием метода `client.chat.completions.create()`. В запросе указывается модель (`g4f.models.default_vision`), сообщение с вопросом (`"What are on this image?"`) и сам файловый объект изображения (`image=local_image`).
3. **Обработка ответа**: После получения ответа от модели, он извлекается из объекта `response_local` и выводится в консоль.
4. **Закрытие файла**: В конце файл с изображением закрывается с использованием метода `local_image.close()`.

**ASCII flowchart**:

```
Открытие локального файла изображения
    ↓
Создание запроса к GPT-4 Vision с изображением
    ↓
Получение ответа от GPT-4 Vision
    ↓
Вывод ответа в консоль
    ↓
Закрытие файла изображения
```

**Примеры**:

```python
import g4f

# Пример использования
local_image_path = "docs/images/cat.jpeg"
try:
    local_image = open(local_image_path, "rb")
    response_local = client.chat.completions.create(
        model=g4f.models.default_vision,
        messages=[{"role": "user", "content": "Describe this image."}],
        image=local_image
    )
    print(f"Local image description: {response_local.choices[0].message.content}")
except FileNotFoundError:
    print(f"File not found: {local_image_path}")
finally:
    if 'local_image' in locals() and hasattr(local_image, 'close'):
        local_image.close()