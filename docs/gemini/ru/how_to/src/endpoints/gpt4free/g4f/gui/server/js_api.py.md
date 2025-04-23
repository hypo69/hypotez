### **Как использовать блок кода JsApi**
=========================================================================================

Описание
-------------------------
Класс `JsApi` расширяет класс `Api` и предоставляет интерфейс для взаимодействия JavaScript-кода с Python-backend через `webview`. Он включает методы для получения сообщений, выбора изображений, работы с камерой и управления состоянием выбранных элементов в пользовательском интерфейсе.

Шаги выполнения
-------------------------
1. **Инициализация класса `JsApi`**:
   - Создается экземпляр класса `JsApi`. Этот класс использует `webview` для взаимодействия с веб-интерфейсом.

2. **Метод `get_conversation`**:
   - Получает опции разговора, идентификатор сообщения и флаг прокрутки.
   - Если у экземпляра класса есть атрибут `image` (изображение выбрано), оно открывается в бинарном режиме и добавляется в опции.
   - Вызывается `_create_response_stream` для получения потока сообщений.
   - Для каждого сообщения выполняется JavaScript-код, который добавляет сообщение на страницу, используя `add_message_chunk`.
   - Проверяется, не остановлен ли процесс (`is_stopped()`). Если остановлен, цикл прерывается.
   - После завершения процесса атрибут `image` сбрасывается в `None`, и вызывается `set_selected(None)`.

3. **Метод `choose_image`**:
   - Вызывает функцию `user_select_image` для выбора изображения из файловой системы пользователя.
   - При выборе изображения вызывается метод `on_image_selection`.

4. **Метод `take_picture`**:
   - Формирует имя файла для сохранения снимка, используя `uuid4()` для уникальности.
   - Вызывает функцию `camera.take_picture` для создания снимка с камеры.
   - После создания снимка вызывается метод `on_camera`.

5. **Метод `on_image_selection`**:
   - Обрабатывает результат выбора изображения.
   - Если файл выбран и существует, его имя сохраняется в атрибут `self.image`.
   - Если файл не выбран или не существует, атрибут `self.image` устанавливается в `None`.
   - Вызывается метод `set_selected` для обновления состояния выбранного элемента интерфейса.

6. **Метод `on_camera`**:
   - Аналогично `on_image_selection`, обрабатывает результат снимка с камеры.
   - Если снимок сделан и файл существует, его имя сохраняется в атрибут `self.image`.
   - Если снимок не сделан или файл не существует, атрибут `self.image` устанавливается в `None`.
   - Вызывается метод `set_selected` для обновления состояния выбранного элемента интерфейса.

7. **Метод `set_selected`**:
   - Управляет визуальным состоянием выбранных элементов интерфейса.
   - Сначала удаляет класс `selected` у элемента с классом `image-label.selected`.
   - Если `input_id` указан и является `image` или `camera`, добавляет класс `selected` к соответствующему элементу `label`.

8. **Методы `get_version`, `get_models`, `get_providers`, `get_provider_models`**:
   - Вызывают соответствующие методы из родительского класса `Api`.

Пример использования
-------------------------

```python
from __future__ import annotations

import json
import os.path
from typing import Iterator
from uuid import uuid4
from functools import partial
import webview
import platformdirs
from plyer import camera
from plyer import filechooser

app_storage_path = platformdirs.user_pictures_dir
user_select_image = partial(
    filechooser.open_file,
    path=platformdirs.user_pictures_dir(),
    filters=[["Image", "*.jpg", "*.jpeg", "*.png", "*.webp", "*.svg"]],
)

from .api import Api

class JsApi(Api):

    def get_conversation(self, options: dict, message_id: str = None, scroll: bool = None) -> Iterator:
        window = webview.windows[0]
        if hasattr(self, "image") and self.image is not None:
            options["image"] = open(self.image, "rb")
        for message in self._create_response_stream(
            self._prepare_conversation_kwargs(options),
            options.get("conversation_id"),
            options.get('provider')
        ):
            if window.evaluate_js(
                f"""
                    is_stopped() ? true :
                    this.add_message_chunk({{
                        json.dumps(message)
                    }}, {{
                        json.dumps(message_id)
                    }}, {{
                        json.dumps(options.get('provider'))
                    }}, {{
                        'true' if scroll else 'false'
                    }}); is_stopped();
                """):\
                break
        self.image = None
        self.set_selected(None)

    def choose_image(self):
        user_select_image(
            on_selection=self.on_image_selection
        )

    def take_picture(self):
        filename = os.path.join(app_storage_path(), f"chat-{uuid4()}.png")
        camera.take_picture(filename=filename, on_complete=self.on_camera)

    def on_image_selection(self, filename):
        filename = filename[0] if isinstance(filename, list) and filename else filename
        if filename and os.path.exists(filename):
            self.image = filename
        else:
            self.image = None
        self.set_selected(None if self.image is None else "image")

    def on_camera(self, filename):
        if filename and os.path.exists(filename):
            self.image = filename
        else:
            self.image = None
        self.set_selected(None if self.image is None else "camera")

    def set_selected(self, input_id: str = None):
        window = webview.windows[0]
        if window is not None:
            window.evaluate_js(
                f"document.querySelector(`.image-label.selected`)?.classList.remove(`selected`);"
            )
            if input_id is not None and input_id in ("image", "camera"):
                window.evaluate_js(
                    f'document.querySelector(`label[for="{input_id}"]`)?.classList.add(`selected`);'
                )

    def get_version(self):
        return super().get_version()

    def get_models(self):
        return super().get_models()

    def get_providers(self):
        return super().get_providers()

    def get_provider_models(self, provider: str, **kwargs):
        return super().get_provider_models(provider, **kwargs)

# Пример использования класса JsApi
if __name__ == '__main__':
    # Создание экземпляра класса JsApi
    js_api = JsApi()

    # Пример вызова метода choose_image (предполагается, что webview уже инициализирован)
    # js_api.choose_image()

    # Пример вызова метода take_picture (предполагается, что webview уже инициализирован)
    # js_api.take_picture()

    # Пример вызова метода get_conversation (с фиктивными данными)
    options = {"conversation_id": "123", "provider": "ExampleProvider"}
    message_id = "456"
    # for message in js_api.get_conversation(options, message_id, scroll=True):
    #     print(f"Received message: {message}")