# Документация для модуля `MiniMax`

## Обзор

Модуль `MiniMax` предоставляет класс для работы с API MiniMax. Он наследуется от `OpenaiTemplate` и содержит информацию о URL, необходимости аутентификации, базовом URL API и поддерживаемых моделях.

## Подробнее

Модуль предназначен для упрощения взаимодействия с MiniMax API, предоставляя стандартный интерфейс через класс `MiniMax`. Он определяет параметры подключения и модели, используемые для запросов к API. Расположение файла в проекте `hypotez` указывает на его роль как одного из провайдеров API.

## Классы

### `MiniMax`

**Описание**: Класс для взаимодействия с API MiniMax.

**Наследует**:
- `OpenaiTemplate`: Предоставляет базовый функционал для работы с OpenAI-подобными API.

**Атрибуты**:
- `label` (str): Метка для API ("MiniMax API").
- `url` (str): URL главной страницы MiniMax ("https://www.hailuo.ai/chat").
- `login_url` (str): URL страницы для получения ключа API ("https://intl.minimaxi.com/user-center/basic-information/interface-key").
- `api_base` (str): Базовый URL API ("https://api.minimaxi.chat/v1").
- `working` (bool): Флаг, указывающий на работоспособность API (True).
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации (True).
- `default_model` (str): Модель, используемая по умолчанию ("MiniMax-Text-01").
- `default_vision_model` (str): Модель для работы с изображениями по умолчанию (совпадает с `default_model`).
- `models` (list[str]): Список поддерживаемых моделей ([`default_model`, "abab6.5s-chat"]).
- `model_aliases` (dict[str, str]): Псевдонимы моделей ({`"MiniMax"`: `default_model`}).

**Принцип работы**:
Класс `MiniMax` определяет все необходимые атрибуты для подключения и работы с API MiniMax. Он наследует от `OpenaiTemplate`, что позволяет использовать общую логику для работы с API, такими как отправка запросов и обработка ответов. Атрибуты класса содержат информацию о URL, необходимости аутентификации и поддерживаемых моделях.

## Методы класса

В данном классе отсутствуют явно определенные методы, поскольку он наследует методы от класса `OpenaiTemplate`. Однако, можно предположить, что методы из `OpenaiTemplate` будут использоваться для взаимодействия с API MiniMax.

## Примеры

Пример использования класса `MiniMax`:

```python
from src.endpoints.gpt4free.g4f.Provider.mini_max.MiniMax import MiniMax

minimax = MiniMax()
print(minimax.label)
print(minimax.api_base)