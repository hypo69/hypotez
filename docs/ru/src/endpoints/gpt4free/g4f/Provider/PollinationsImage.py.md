# Модуль PollinationsImage

## Обзор

Модуль `PollinationsImage` является частью проекта `hypotez` и предназначен для работы с сервисом Pollinations AI для генерации изображений. Он расширяет возможности класса `PollinationsAI`, добавляя функциональность, специфичную для работы с изображениями, такую как выбор модели для генерации изображений и форматирование запросов.

## Подробней

Модуль предоставляет класс `PollinationsImage`, который наследуется от `PollinationsAI`. Класс `PollinationsImage` позволяет генерировать изображения, используя различные модели, предоставляемые сервисом Pollinations AI. Он также предоставляет методы для управления списком доступных моделей и настройки параметров генерации изображений, таких как соотношение сторон, ширина, высота и другие параметры. Модуль использует асинхронные генераторы для эффективной обработки запросов на генерацию изображений.

## Классы

### `PollinationsImage`

**Описание**: Класс `PollinationsImage` предназначен для работы с сервисом Pollinations AI для генерации изображений. Он наследуется от класса `PollinationsAI` и добавляет специфические методы и атрибуты для работы с изображениями.

**Наследует**:

- `PollinationsAI`: Класс, предоставляющий общую функциональность для взаимодействия с сервисом Pollinations AI.

**Атрибуты**:

- `label` (str): Метка, идентифицирующая провайдера изображений (`"PollinationsImage"`).
- `default_model` (str): Модель, используемая по умолчанию для генерации изображений (`"flux"`).
- `default_vision_model` (None): Модель, используемая по умолчанию для анализа изображений (в данном случае `None`).
- `default_image_model` (str): Модель, используемая по умолчанию для генерации изображений (совпадает с `default_model`).
- `image_models` (list[str]): Список поддерживаемых моделей для генерации изображений (изначально содержит только `default_image_model`).
- `_models_loaded` (bool): Флаг, указывающий, были ли загружены модели (изначально `False`).

**Методы**:

- `get_models(**kwargs)`: Получает список доступных моделей для генерации изображений.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, prompt: str = None, aspect_ratio: str = "1:1", width: int = None, height: int = None, seed: Optional[int] = None, cache: bool = False, nologo: bool = True, private: bool = False, enhance: bool = False, safe: bool = False, n: int = 4, **kwargs) -> AsyncResult`: Создает асинхронный генератор для генерации изображений на основе предоставленных параметров.

## Функции

### `get_models`

```python
    @classmethod
    def get_models(cls, **kwargs):
        """Получает список доступных моделей для генерации изображений.

        Args:
            **kwargs: Дополнительные параметры (не используются).

        Returns:
            list[str]: Список доступных моделей для генерации изображений.
        """
```

**Назначение**: Метод `get_models` предназначен для получения списка доступных моделей для генерации изображений. Он обеспечивает загрузку моделей только один раз, используя флаг `_models_loaded`.

**Параметры**:

- `cls` (class): Ссылка на класс `PollinationsImage`.
- `**kwargs`: Дополнительные параметры (не используются).

**Возвращает**:

- `list[str]`: Список доступных моделей для генерации изображений.

**Как работает функция**:

1.  Проверяет, загружены ли модели, используя флаг `cls._models_loaded`.
2.  Если модели не загружены, вызывает метод `super().get_models()` для загрузки моделей из родительского класса `PollinationsAI`.
3.  Объединяет модели из `cls.image_models`, `PollinationsAI.image_models` и `cls.extra_image_models`, удаляя дубликаты.
4.  Устанавливает флаг `cls._models_loaded` в `True`.
5.  Возвращает список моделей `cls.image_models`.

```
A: Проверка, загружены ли модели (cls._models_loaded)
│
├───> B: Если модели не загружены:
│     │
│     ├───> C: Загрузка моделей из родительского класса (super().get_models())
│     │
│     ├───> D: Объединение моделей из разных источников
│     │
│     └───> E: Установка флага cls._models_loaded в True
│
└───> F: Возврат списка моделей (cls.image_models)
```

**Примеры**:

```python
PollinationsImage.get_models()
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        prompt: str = None,
        aspect_ratio: str = "1:1",
        width: int = None,
        height: int = None,
        seed: Optional[int] = None,
        cache: bool = False,
        nologo: bool = True,
        private: bool = False,
        enhance: bool = False,
        safe: bool = False,
        n: int = 4,
        **kwargs
    ) -> AsyncResult:
        """Создает асинхронный генератор для генерации изображений на основе предоставленных параметров.

        Args:
            model (str): Модель для генерации изображений.
            messages (Messages): Сообщения для генерации изображения.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            prompt (str, optional): Текст запроса для генерации изображения. По умолчанию `None`.
            aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию `"1:1"`.
            width (int, optional): Ширина изображения. По умолчанию `None`.
            height (int, optional): Высота изображения. По умолчанию `None`.
            seed (Optional[int], optional): Зерно для генерации случайных чисел. По умолчанию `None`.
            cache (bool, optional): Использовать кэш. По умолчанию `False`.
            nologo (bool, optional): Удалять логотип. По умолчанию `True`.
            private (bool, optional): Приватный режим. По умолчанию `False`.
            enhance (bool, optional): Улучшать изображение. По умолчанию `False`.
            safe (bool, optional): Безопасный режим. По умолчанию `False`.
            n (int, optional): Количество изображений для генерации. По умолчанию `4`.
            **kwargs: Дополнительные параметры.

        Yields:
            AsyncResult: Часть сгенерированного изображения.
        """
```

**Назначение**: Метод `create_async_generator` создает асинхронный генератор для генерации изображений на основе предоставленных параметров. Он вызывает метод `get_models` для обновления списка моделей перед созданием генератора.

**Параметры**:

- `cls` (class): Ссылка на класс `PollinationsImage`.
- `model` (str): Модель для генерации изображений.
- `messages` (Messages): Сообщения для генерации изображения.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `prompt` (str, optional): Текст запроса для генерации изображения. По умолчанию `None`.
- `aspect_ratio` (str, optional): Соотношение сторон изображения. По умолчанию `"1:1"`.
- `width` (int, optional): Ширина изображения. По умолчанию `None`.
- `height` (int, optional): Высота изображения. По умолчанию `None`.
- `seed` (Optional[int], optional): Зерно для генерации случайных чисел. По умолчанию `None`.
- `cache` (bool, optional): Использовать кэш. По умолчанию `False`.
- `nologo` (bool, optional): Удалять логотип. По умолчанию `True`.
- `private` (bool, optional): Приватный режим. По умолчанию `False`.
- `enhance` (bool, optional): Улучшать изображение. По умолчанию `False`.
- `safe` (bool, optional): Безопасный режим. По умолчанию `False`.
- `n` (int, optional): Количество изображений для генерации. По умолчанию `4`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:

- `AsyncResult`: Асинхронный генератор, возвращающий части сгенерированного изображения.

**Как работает функция**:

1.  Вызывает метод `cls.get_models()` для обновления списка моделей.
2.  Создает асинхронный генератор, который вызывает метод `cls._generate_image` с предоставленными параметрами.
3.  Форматирует запрос `prompt` с использованием функции `format_image_prompt`.
4.  Передает параметры в метод `cls._generate_image` для генерации изображения.
5.  Генератор возвращает части сгенерированного изображения.

```
A: Вызов метода cls.get_models() для обновления списка моделей
│
├───> B: Создание асинхронного генератора
│     │
│     ├───> C: Форматирование запроса prompt с использованием функции format_image_prompt
│     │
│     └───> D: Вызов метода cls._generate_image с предоставленными параметрами
│
└───> E: Генератор возвращает части сгенерированного изображения
```

**Примеры**:

```python
async for chunk in PollinationsImage.create_async_generator(model="flux", messages=["Example message"], prompt="Example prompt"):
    print(chunk)