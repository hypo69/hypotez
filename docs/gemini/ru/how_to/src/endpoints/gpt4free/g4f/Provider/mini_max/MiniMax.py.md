## Как использовать MiniMax API
=========================================================================================

Описание
-------------------------
Этот блок кода определяет класс `MiniMax`, который представляет собой реализацию `OpenaiTemplate` для взаимодействия с API MiniMax. Класс содержит информацию о параметрах API, таких как URL, аутентификация, доступные модели и т.д.

Шаги выполнения
-------------------------
1. **Определение класса `MiniMax`:** Класс наследуется от `OpenaiTemplate`, что позволяет использовать его в рамках проекта.
2. **Определение атрибутов класса:**
    - `label`: Текстовое описание API ("MiniMax API").
    - `url`: Основной URL для отправки запросов к API ("https://www.hailuo.ai/chat").
    - `login_url`: URL для аутентификации ("https://intl.minimaxi.com/user-center/basic-information/interface-key").
    - `api_base`: Базовый URL для API ("https://api.minimaxi.chat/v1").
    - `working`: Флаг, указывающий на работоспособность API (True).
    - `needs_auth`: Флаг, указывающий на необходимость аутентификации (True).
    - `default_model`: Имя модели по умолчанию ("MiniMax-Text-01").
    - `default_vision_model`: Имя модели по умолчанию для обработки изображений (то же, что и `default_model`).
    - `models`: Список доступных моделей для использования с API ([default_model, "abab6.5s-chat"]).
    - `model_aliases`: Словарь с альтернативными названиями моделей, где "MiniMax"  - это псевдоним для `default_model`.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.mini_max.MiniMax import MiniMax

# Создание объекта MiniMax
mini_max = MiniMax()

# Получение списка доступных моделей
print(mini_max.models)  # Выведет ['MiniMax-Text-01', 'abab6.5s-chat']

# Использование модели по умолчанию
response = mini_max.generate_text("Привет, как дела?")

# Использование другой модели
response = mini_max.generate_text("Привет, как дела?", model="abab6.5s-chat")

```