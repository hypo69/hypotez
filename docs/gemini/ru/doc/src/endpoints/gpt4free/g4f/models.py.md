# Модуль для представления и управления моделями машинного обучения

## Обзор

Модуль `models.py` содержит классы и структуры данных для представления и управления моделями машинного обучения, используемыми в проекте `hypotez`. Он включает в себя классы для моделей различных типов (текстовые, аудио, визуальные) и утилиты для сопоставления строковых идентификаторов с экземплярами моделей.

## Подробнее

Этот модуль предоставляет основу для работы с различными моделями машинного обучения, используемыми в проекте `hypotez`. Он определяет структуру данных для представления моделей, включая их имена, базовых провайдеров и предпочтительных провайдеров. Модуль также предоставляет утилиты для сопоставления строковых идентификаторов с экземплярами моделей, что упрощает выбор и использование конкретных моделей в проекте.

## Классы

### `Model`

**Описание**:
Представляет конфигурацию модели машинного обучения.

**Атрибуты**:
- `name` (str): Название модели.
- `base_provider` (str): Провайдер по умолчанию для модели.
- `best_provider` (ProviderType): Предпочтительный провайдер для модели, обычно с логикой повторных попыток.

**Методы**:
- `__all__() -> list[str]`: Возвращает список всех названий моделей.

#### `__all__`

```python
    @staticmethod
    def __all__() -> list[str]:
        """Returns a list of all model names."""
        return _all_models
```

**Назначение**:
Возвращает список всех названий моделей, зарегистрированных в модуле.

**Возвращает**:
- `list[str]`: Список строк, представляющих названия всех доступных моделей.

**Как работает функция**:
Статический метод `__all__` возвращает список `_all_models`, который содержит названия всех определенных в модуле моделей. Этот метод позволяет получить полный перечень доступных моделей для использования в других частях программы.

**Примеры**:
```python
>>> Model.__all__()
['gpt-3.5-turbo', 'gpt-4', 'gpt-4o', ...]
```

### `ImageModel`

**Описание**:
Представляет модель машинного обучения для работы с изображениями.
**Наследует**:
Наследует класс `Model`.

### `AudioModel`

**Описание**:
Представляет модель машинного обучения для работы со звуком.
**Наследует**:
Наследует класс `Model`.

### `VisionModel`

**Описание**:
Представляет модель машинного обучения для работы с видео.
**Наследует**:
Наследует класс `Model`.

### `ModelUtils`

**Описание**:
Утилитный класс для сопоставления строковых идентификаторов с экземплярами `Model`.

**Атрибуты**:
- `convert` (dict[str, Model]): Словарь, сопоставляющий строковые идентификаторы моделей с экземплярами `Model`.

## Методы класса

### `Model.__init__`

```python
def __init__(name: str, base_provider: str, best_provider: ProviderType = None)
    """
    Args:
        name (str): Название модели.
        base_provider (str): Провайдер по умолчанию для модели.
        best_provider (ProviderType): Предпочтительный провайдер для модели, обычно с логикой повторных попыток. По умолчанию `None`.
    """
    ...
```

**Назначение**:
Конструктор класса `Model`, инициализирует экземпляр модели с заданными параметрами.

**Параметры**:
- `name` (str): Название модели.
- `base_provider` (str): Провайдер по умолчанию для модели.
- `best_provider` (ProviderType, optional): Предпочтительный провайдер для модели. По умолчанию `None`.

**Примеры**:

```python
model = Model(name='gpt-3.5-turbo', base_provider='OpenAI')
```

### `ModelUtils.__init__`

```python
def __init__(convert: dict[str, Model])
    """
    Args:
        convert (dict[str, Model]): Словарь, сопоставляющий строковые идентификаторы моделей с экземплярами `Model`.
    """
    ...
```

**Назначение**:
Конструктор класса `ModelUtils`, инициализирует словарь `convert`, который сопоставляет строковые идентификаторы моделей с соответствующими экземплярами `Model`.

**Параметры**:
- `convert` (dict[str, Model]): Словарь, сопоставляющий строковые идентификаторы моделей с экземплярами `Model`.

**Примеры**:

```python
model_utils = ModelUtils(convert={'gpt-3.5-turbo': gpt_3_5_turbo})
```

## Переменные

### `default`

```python
default = Model(
    name = "",
    base_provider = "",
    best_provider = IterListProvider([\
        DDG,\
        Blackbox,\
        Copilot,\
        DeepInfraChat,\
        AllenAI,\
        PollinationsAI,\
        TypeGPT,\
        OIVSCode,\
        ChatGptEs,\
        Free2GPT,\
        FreeGpt,\
        Glider,\
        Dynaspark,\
        OpenaiChat,\
        Jmuz,\
        Cloudflare,\
    ])
)
```

**Назначение**:
Определяет модель по умолчанию, которая используется, когда не указана конкретная модель.

**Описание**:
- `name` (str): Пустая строка, указывающая на отсутствие конкретного имени модели.
- `base_provider` (str): Пустая строка, указывающая на отсутствие конкретного базового провайдера.
- `best_provider` (IterListProvider): Список провайдеров, которые будут использоваться для обработки запроса.

### `default_vision`

```python
default_vision = Model(
    name = "",
    base_provider = "",
    best_provider = IterListProvider([\
        Blackbox,\
        OIVSCode,\
        TypeGPT,\
        DeepInfraChat,\
        PollinationsAI,\
        Dynaspark,\
        HuggingSpace,\
        GeminiPro,\
        HuggingFaceAPI,\
        CopilotAccount,\
        OpenaiAccount,\
        Gemini,\
    ], shuffle=False)
)
```

**Назначение**:
Определяет модель по умолчанию для задач, связанных с обработкой изображений.

**Описание**:
- `name` (str): Пустая строка, указывающая на отсутствие конкретного имени модели.
- `base_provider` (str): Пустая строка, указывающая на отсутствие конкретного базового провайдера.
- `best_provider` (IterListProvider): Список провайдеров, которые будут использоваться для обработки запроса.

### `demo_models`

```python
demo_models = {\
    llama_3_2_11b.name: [llama_3_2_11b, [HuggingChat]],\
    qwen_2_vl_7b.name: [qwen_2_vl_7b, [HuggingFaceAPI]],\
    deepseek_r1.name: [deepseek_r1, [HuggingFace, PollinationsAI]],\
    janus_pro_7b.name: [janus_pro_7b, [HuggingSpace, G4F]],\
    command_r.name: [command_r, [HuggingSpace]],\
    command_r_plus.name: [command_r_plus, [HuggingSpace]],\
    command_r7b.name: [command_r7b, [HuggingSpace]],\
    qwen_2_5_coder_32b.name: [qwen_2_5_coder_32b, [HuggingFace]],\
    qwq_32b.name: [qwq_32b, [HuggingFace]],\
    llama_3_3_70b.name: [llama_3_3_70b, [HuggingFace]],\
    sd_3_5.name: [sd_3_5, [HuggingSpace, HuggingFace]],\
    flux_dev.name: [flux_dev, [PollinationsImage, HuggingFace, HuggingSpace]],\
    flux_schnell.name: [flux_schnell, [PollinationsImage, HuggingFace, HuggingSpace]],\
}
```

**Назначение**:
Определяет словарь, содержащий демонстрационные модели и их провайдеров.

**Описание**:
Словарь `demo_models` сопоставляет имена моделей со списком, содержащим экземпляр модели и список провайдеров для этой модели.

### `__models__`

```python
__models__  = {\
    model.name: (model, providers)\
        for model, providers in [\
            (model, [provider for provider in model.best_provider.providers if provider.working]\
                if isinstance(model.best_provider, IterListProvider)\
                else [model.best_provider]\
                if model.best_provider is not None and model.best_provider.working\
                else [])\
        for model in ModelUtils.convert.values()]\
        if providers\
    }
```

**Назначение**:
Создает словарь, содержащий все модели и их провайдеров.

**Описание**:
Словарь `__models__` сопоставляет имена моделей с кортежем, содержащим экземпляр модели и список провайдеров для этой модели.

### `_all_models`

```python
_all_models = list(__models__.keys())
```

**Назначение**:
Создает список всех доступных моделей.

**Описание**:
Список `_all_models` содержит имена всех моделей, определенных в словаре `__models__`.