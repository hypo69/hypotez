# Модуль для работы с моделями g4f
=====================================

Модуль содержит классы для представления и управления различными моделями машинного обучения, включая текстовые, аудио и визуальные модели. Он также предоставляет утилиты для сопоставления строковых идентификаторов с экземплярами моделей и управления списком доступных моделей и их провайдеров.

## Обзор

Модуль `models.py` содержит определения классов для представления различных моделей машинного обучения, включая текстовые, аудио и визуальные модели. Он также предоставляет утилиты для сопоставления строковых идентификаторов с экземплярами моделей и управления списком доступных моделей и их провайдеров.

## Подробнее

Этот модуль предназначен для централизованного управления информацией о доступных моделях машинного обучения и их провайдерах в проекте `hypotez`. Он предоставляет удобный способ доступа к моделям по их именам и позволяет легко расширять список поддерживаемых моделей.

## Классы

### `Model`

**Описание**: Представляет конфигурацию модели машинного обучения.

   **Атрибуты**:
   - `name` (str): Имя модели.
   - `base_provider` (str): Провайдер по умолчанию для модели.
   - `best_provider` (ProviderType): Предпочтительный провайдер для модели, обычно с логикой повторных попыток.

   **Методы**:
   - `__all__()`: Возвращает список всех имен моделей.

### `ImageModel`
**Описание**: Представляет модель для работы с изображениями, наследуется от класса `Model`.
    **Наследует**
    - `Model`: Базовый класс для моделей машинного обучения.

### `AudioModel`
**Описание**: Представляет модель для работы со звуком, наследуется от класса `Model`.
    **Наследует**
    - `Model`: Базовый класс для моделей машинного обучения.

### `VisionModel`
**Описание**: Представляет модель для работы с видео, наследуется от класса `Model`.
    **Наследует**
    - `Model`: Базовый класс для моделей машинного обучения.

### `ModelUtils`

**Описание**: Утилитный класс для сопоставления строковых идентификаторов с экземплярами `Model`.

   **Атрибуты**:
   - `convert` (dict[str, Model]): Словарь, сопоставляющий строковые идентификаторы моделей с экземплярами `Model`.

## Функции

### `__all__`

```python
@staticmethod
def __all__() -> list[str]:
    """Возвращает список всех имен моделей."""
```

**Назначение**: Возвращает список всех имен моделей, доступных в модуле.

**Параметры**:
- Нет

**Возвращает**:
- `list[str]`: Список строк, представляющих имена всех моделей.

**Как работает функция**:

1.  Функция возвращает список `_all_models`, который содержит имена всех моделей, определенных в модуле.

**Примеры**:

```python
>>> Model.__all__()
['gpt-3.5-turbo', 'gpt-4', 'gpt-4o', 'gpt-4o-mini', ...]
```

### `default`

```python
default = Model(
    name = "",
    base_provider = "",
    best_provider = IterListProvider([
        DDG,
        Blackbox,
        Copilot,
        DeepInfraChat,
        AllenAI,
        PollinationsAI,
        TypeGPT,
        OIVSCode,
        ChatGptEs,
        Free2GPT,
        FreeGpt,
        Glider,
        Dynaspark,
        OpenaiChat,
        Jmuz,
        Cloudflare,
    ])
)
```

**Назначение**: Определяет модель по умолчанию без конкретного имени и базового провайдера, но с указанием списка лучших провайдеров.

**Параметры**:
- `name` (str): Имя модели (в данном случае пустая строка).
- `base_provider` (str): Базовый провайдер (в данном случае пустая строка).
- `best_provider` (ProviderType): Список предпочтительных провайдеров, использующих `IterListProvider`.

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем и базовым провайдером, установленными в пустые строки.
2. В качестве лучшего провайдера используется `IterListProvider`, который содержит список предпочтительных провайдеров, таких как `DDG`, `Blackbox`, `Copilot` и другие.

**Примеры**:

```python
>>> default.name
''
>>> default.base_provider
''
>>> default.best_provider
<g4f.Provider.IterListProvider object at 0x...>
```

### `default_vision`

```python
default_vision = Model(
    name = "",
    base_provider = "",
    best_provider = IterListProvider([
        Blackbox,
        OIVSCode,
        TypeGPT,
        DeepInfraChat,
        PollinationsAI,
        Dynaspark,
        HuggingSpace,
        GeminiPro,
        HuggingFaceAPI,
        CopilotAccount,
        OpenaiAccount,
        Gemini,
    ], shuffle=False)
)
```

**Назначение**: Определяет модель для работы с визуальными данными по умолчанию, без конкретного имени и базового провайдера, но с указанием списка лучших провайдеров.

**Параметры**:
- `name` (str): Имя модели (в данном случае пустая строка).
- `base_provider` (str): Базовый провайдер (в данном случае пустая строка).
- `best_provider` (ProviderType): Список предпочтительных провайдеров, использующих `IterListProvider` с отключенным перемешиванием.

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем и базовым провайдером, установленными в пустые строки.
2. В качестве лучшего провайдера используется `IterListProvider`, который содержит список предпочтительных провайдеров для визуальных данных, таких как `Blackbox`, `OIVSCode`, `TypeGPT` и другие.
3. Параметр `shuffle` установлен в `False`, что означает, что провайдеры будут использоваться в указанном порядке.

**Примеры**:

```python
>>> default_vision.name
''
>>> default_vision.base_provider
''
>>> default_vision.best_provider
<g4f.Provider.IterListProvider object at 0x...>
```

### `gpt_3_5_turbo`

```python
gpt_3_5_turbo = Model(
    name          = \'gpt-3.5-turbo\',
    base_provider = \'OpenAI\'
)
```

**Назначение**: Определяет модель `gpt-3.5-turbo` с указанием базового провайдера `OpenAI`.

**Параметры**:
- `name` (str): Имя модели (`gpt-3.5-turbo`).
- `base_provider` (str): Базовый провайдер (`OpenAI`).

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем `gpt-3.5-turbo` и базовым провайдером `OpenAI`.

**Примеры**:

```python
>>> gpt_3_5_turbo.name
'gpt-3.5-turbo'
>>> gpt_3_5_turbo.base_provider
'OpenAI'
```

### `gpt_4`

```python
gpt_4 = Model(
    name          = \'gpt-4\',\n
    base_provider = \'OpenAI\',\n
    best_provider = IterListProvider([DDG, Jmuz, ChatGptEs, PollinationsAI, Yqcloud, Goabror, Copilot, OpenaiChat, Liaobots])\n
)
```

**Назначение**: Определяет модель `gpt-4` с указанием базового провайдера `OpenAI` и списка лучших провайдеров.

**Параметры**:
- `name` (str): Имя модели (`gpt-4`).
- `base_provider` (str): Базовый провайдер (`OpenAI`).
- `best_provider` (ProviderType): Список предпочтительных провайдеров, использующих `IterListProvider`.

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем `gpt-4`, базовым провайдером `OpenAI` и списком лучших провайдеров, таких как `DDG`, `Jmuz` и другие.

**Примеры**:

```python
>>> gpt_4.name
'gpt-4'
>>> gpt_4.base_provider
'OpenAI'
>>> gpt_4.best_provider
<g4f.Provider.IterListProvider object at 0x...>
```

### `gpt_4o`

```python
gpt_4o = VisionModel(
    name          = \'gpt-4o\',\n
    base_provider = \'OpenAI\',\n
    best_provider = IterListProvider([Blackbox, Jmuz, ChatGptEs, PollinationsAI, Liaobots, OpenaiChat])\n
)
```

**Назначение**: Определяет визуальную модель `gpt-4o` с указанием базового провайдера `OpenAI` и списка лучших провайдеров.

**Параметры**:
- `name` (str): Имя модели (`gpt-4o`).
- `base_provider` (str): Базовый провайдер (`OpenAI`).
- `best_provider` (ProviderType): Список предпочтительных провайдеров, использующих `IterListProvider`.

**Возвращает**:
- `VisionModel`: Экземпляр класса `VisionModel` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `VisionModel` с именем `gpt-4o`, базовым провайдером `OpenAI` и списком лучших провайдеров, таких как `Blackbox`, `Jmuz` и другие.

**Примеры**:

```python
>>> gpt_4o.name
'gpt-4o'
>>> gpt_4o.base_provider
'OpenAI'
>>> gpt_4o.best_provider
<g4f.Provider.IterListProvider object at 0x...>
```

### `gpt_4o_mini`

```python
gpt_4o_mini = Model(
    name          = \'gpt-4o-mini\',\n
    base_provider = \'OpenAI\',\n
    best_provider = IterListProvider([DDG, Blackbox, ChatGptEs, TypeGPT, PollinationsAI, OIVSCode, Liaobots, Jmuz, OpenaiChat])\n
)
```

**Назначение**: Определяет модель `gpt-4o-mini` с указанием базового провайдера `OpenAI` и списка лучших провайдеров.

**Параметры**:
- `name` (str): Имя модели (`gpt-4o-mini`).
- `base_provider` (str): Базовый провайдер (`OpenAI`).
- `best_provider` (ProviderType): Список предпочтительных провайдеров, использующих `IterListProvider`.

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем `gpt-4o-mini`, базовым провайдером `OpenAI` и списком лучших провайдеров, таких как `DDG`, `Blackbox` и другие.

**Примеры**:

```python
>>> gpt_4o_mini.name
'gpt-4o-mini'
>>> gpt_4o_mini.base_provider
'OpenAI'
>>> gpt_4o_mini.best_provider
<g4f.Provider.IterListProvider object at 0x...>
```

### `gpt_4o_audio`

```python
gpt_4o_audio = AudioModel(
    name          = \'gpt-4o-audio\',\n
    base_provider = \'OpenAI\',\n
    best_provider = PollinationsAI\n
)
```

**Назначение**: Определяет аудиомодель `gpt-4o-audio` с указанием базового провайдера `OpenAI` и лучшего провайдера `PollinationsAI`.

**Параметры**:
- `name` (str): Имя модели (`gpt-4o-audio`).
- `base_provider` (str): Базовый провайдер (`OpenAI`).
- `best_provider` (ProviderType): Лучший провайдер (`PollinationsAI`).

**Возвращает**:
- `AudioModel`: Экземпляр класса `AudioModel` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `AudioModel` с именем `gpt-4o-audio`, базовым провайдером `OpenAI` и лучшим провайдером `PollinationsAI`.

**Примеры**:

```python
>>> gpt_4o_audio.name
'gpt-4o-audio'
>>> gpt_4o_audio.base_provider
'OpenAI'
>>> gpt_4o_audio.best_provider
<g4f.Provider.PollinationsAI object at 0x...>
```

### `o1`

```python
o1 = Model(
    name          = \'o1\',\n
    base_provider = \'OpenAI\',\n
    best_provider = IterListProvider([Blackbox, Copilot, OpenaiAccount])\n
)
```

**Назначение**: Определяет модель `o1` с указанием базового провайдера `OpenAI` и списка лучших провайдеров.

**Параметры**:
- `name` (str): Имя модели (`o1`).
- `base_provider` (str): Базовый провайдер (`OpenAI`).
- `best_provider` (ProviderType): Список предпочтительных провайдеров, использующих `IterListProvider`.

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем `o1`, базовым провайдером `OpenAI` и списком лучших провайдеров, таких как `Blackbox`, `Copilot` и `OpenaiAccount`.

**Примеры**:

```python
>>> o1.name
'o1'
>>> o1.base_provider
'OpenAI'
>>> o1.best_provider
<g4f.Provider.IterListProvider object at 0x...>
```

### `o1_mini`

```python
o1_mini = Model(
    name          = \'o1-mini\',\n
    base_provider = \'OpenAI\',\n
    best_provider = OpenaiAccount\n
)
```

**Назначение**: Определяет модель `o1-mini` с указанием базового провайдера `OpenAI` и лучшего провайдера `OpenaiAccount`.

**Параметры**:
- `name` (str): Имя модели (`o1-mini`).
- `base_provider` (str): Базовый провайдер (`OpenAI`).
- `best_provider` (ProviderType): Лучший провайдер (`OpenaiAccount`).

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем `o1-mini`, базовым провайдером `OpenAI` и лучшим провайдером `OpenaiAccount`.

**Примеры**:

```python
>>> o1_mini.name
'o1-mini'
>>> o1_mini.base_provider
'OpenAI'
>>> o1_mini.best_provider
<g4f.Provider.OpenaiAccount object at 0x...>
```

### `o3_mini`

```python
o3_mini = Model(
    name          = \'o3-mini\',\n
    base_provider = \'OpenAI\',\n
    best_provider = IterListProvider([DDG, Blackbox, PollinationsAI, Liaobots])\n
)
```

**Назначение**: Определяет модель `o3-mini` с указанием базового провайдера `OpenAI` и списка лучших провайдеров.

**Параметры**:
- `name` (str): Имя модели (`o3-mini`).
- `base_provider` (str): Базовый провайдер (`OpenAI`).
- `best_provider` (ProviderType): Список предпочтительных провайдеров, использующих `IterListProvider`.

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем `o3-mini`, базовым провайдером `OpenAI` и списком лучших провайдеров, таких как `DDG`, `Blackbox`, `PollinationsAI` и `Liaobots`.

**Примеры**:

```python
>>> o3_mini.name
'o3-mini'
>>> o3_mini.base_provider
'OpenAI'
>>> o3_mini.best_provider
<g4f.Provider.IterListProvider object at 0x...>
```

### `gigachat`

```python
gigachat = Model(
    name          = \'GigaChat:latest\',\n
    base_provider = \'gigachat\',\n
    best_provider = GigaChat\n
)
```

**Назначение**: Определяет модель `GigaChat:latest` с указанием базового провайдера `gigachat` и лучшего провайдера `GigaChat`.

**Параметры**:
- `name` (str): Имя модели (`GigaChat:latest`).
- `base_provider` (str): Базовый провайдер (`gigachat`).
- `best_provider` (ProviderType): Лучший провайдер (`GigaChat`).

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем `GigaChat:latest`, базовым провайдером `gigachat` и лучшим провайдером `GigaChat`.

**Примеры**:

```python
>>> gigachat.name
'GigaChat:latest'
>>> gigachat.base_provider
'gigachat'
>>> gigachat.best_provider
<g4f.Provider.GigaChat object at 0x...>
```

### `meta`

```python
meta = Model(
    name          = "meta-ai",
    base_provider = "Meta",
    best_provider = MetaAI
)
```

**Назначение**: Определяет модель `meta-ai` с указанием базового провайдера `Meta` и лучшего провайдера `MetaAI`.

**Параметры**:
- `name` (str): Имя модели (`meta-ai`).
- `base_provider` (str): Базовый провайдер (`Meta`).
- `best_provider` (ProviderType): Лучший провайдер (`MetaAI`).

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем `meta-ai`, базовым провайдером `Meta` и лучшим провайдером `MetaAI`.

**Примеры**:

```python
>>> meta.name
'meta-ai'
>>> meta.base_provider
'Meta'
>>> meta.best_provider
<g4f.Provider.MetaAI object at 0x...>
```

### `llama_2_7b`

```python
llama_2_7b = Model(
    name          = "llama-2-7b",
    base_provider = "Meta Llama",
    best_provider = Cloudflare
)
```

**Назначение**: Определяет модель `llama-2-7b` с указанием базового провайдера `Meta Llama` и лучшего провайдера `Cloudflare`.

**Параметры**:
- `name` (str): Имя модели (`llama-2-7b`).
- `base_provider` (str): Базовый провайдер (`Meta Llama`).
- `best_provider` (ProviderType): Лучший провайдер (`Cloudflare`).

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем `llama-2-7b`, базовым провайдером `Meta Llama` и лучшим провайдером `Cloudflare`.

**Примеры**:

```python
>>> llama_2_7b.name
'llama-2-7b'
>>> llama_2_7b.base_provider
'Meta Llama'
>>> llama_2_7b.best_provider
<g4f.Provider.Cloudflare object at 0x...>
```

### `llama_3_8b`

```python
llama_3_8b = Model(
    name          = "llama-3-8b",
    base_provider = "Meta Llama",
    best_provider = IterListProvider([Jmuz, Cloudflare])
)
```

**Назначение**: Определяет модель `llama-3-8b` с указанием базового провайдера `Meta Llama` и списка лучших провайдеров.

**Параметры**:
- `name` (str): Имя модели (`llama-3-8b`).
- `base_provider` (str): Базовый провайдер (`Meta Llama`).
- `best_provider` (ProviderType): Список предпочтительных провайдеров, использующих `IterListProvider`.

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем `llama-3-8b`, базовым провайдером `Meta Llama` и списком лучших провайдеров, таких как `Jmuz` и `Cloudflare`.

**Примеры**:

```python
>>> llama_3_8b.name
'llama-3-8b'
>>> llama_3_8b.base_provider
'Meta Llama'
>>> llama_3_8b.best_provider
<g4f.Provider.IterListProvider object at 0x...>
```

### `llama_3_70b`

```python
llama_3_70b = Model(
    name          = "llama-3-70b",
    base_provider = "Meta Llama",
    best_provider = Jmuz
)
```

**Назначение**: Определяет модель `llama-3-70b` с указанием базового провайдера `Meta Llama` и лучшего провайдера `Jmuz`.

**Параметры**:
- `name` (str): Имя модели (`llama-3-70b`).
- `base_provider` (str): Базовый провайдер (`Meta Llama`).
- `best_provider` (ProviderType): Лучший провайдер (`Jmuz`).

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем `llama-3-70b`, базовым провайдером `Meta Llama` и лучшим провайдером `Jmuz`.

**Примеры**:

```python
>>> llama_3_70b.name
'llama-3-70b'
>>> llama_3_70b.base_provider
'Meta Llama'
>>> llama_3_70b.best_provider
<g4f.Provider.Jmuz object at 0x...>
```

### `llama_3_1_8b`

```python
llama_3_1_8b = Model(
    name          = "llama-3.1-8b",
    base_provider = "Meta Llama",
    best_provider = IterListProvider([DeepInfraChat, Glider, PollinationsAI, AllenAI, Jmuz, Cloudflare])
)
```

**Назначение**: Определяет модель `llama-3.1-8b` с указанием базового провайдера `Meta Llama` и списка лучших провайдеров.

**Параметры**:
- `name` (str): Имя модели (`llama-3.1-8b`).
- `base_provider` (str): Базовый провайдер (`Meta Llama`).
- `best_provider` (ProviderType): Список предпочтительных провайдеров, использующих `IterListProvider`.

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем `llama-3.1-8b`, базовым провайдером `Meta Llama` и списком лучших провайдеров, таких как `DeepInfraChat`, `Glider` и другие.

**Примеры**:

```python
>>> llama_3_1_8b.name
'llama-3.1-8b'
>>> llama_3_1_8b.base_provider
'Meta Llama'
>>> llama_3_1_8b.best_provider
<g4f.Provider.IterListProvider object at 0x...>
```

### `llama_3_1_70b`

```python
llama_3_1_70b = Model(
    name          = "llama-3.1-70b",
    base_provider = "Meta Llama",
    best_provider = IterListProvider([Glider, AllenAI, Jmuz])
)
```

**Назначение**: Определяет модель `llama-3.1-70b` с указанием базового провайдера `Meta Llama` и списка лучших провайдеров.

**Параметры**:
- `name` (str): Имя модели (`llama-3.1-70b`).
- `base_provider` (str): Базовый провайдер (`Meta Llama`).
- `best_provider` (ProviderType): Список предпочтительных провайдеров, использующих `IterListProvider`.

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем `llama-3.1-70b`, базовым провайдером `Meta Llama` и списком лучших провайдеров, таких как `Glider`, `AllenAI` и `Jmuz`.

**Примеры**:

```python
>>> llama_3_1_70b.name
'llama-3.1-70b'
>>> llama_3_1_70b.base_provider
'Meta Llama'
>>> llama_3_1_70b.best_provider
<g4f.Provider.IterListProvider object at 0x...>
```

### `llama_3_1_405b`

```python
llama_3_1_405b = Model(
    name          = "llama-3.1-405b",
    base_provider = "Meta Llama",
    best_provider = IterListProvider([AllenAI, Jmuz])
)
```

**Назначение**: Определяет модель `llama-3.1-405b` с указанием базового провайдера `Meta Llama` и списка лучших провайдеров.

**Параметры**:
- `name` (str): Имя модели (`llama-3.1-405b`).
- `base_provider` (str): Базовый провайдер (`Meta Llama`).
- `best_provider` (ProviderType): Список предпочтительных провайдеров, использующих `IterListProvider`.

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем `llama-3.1-405b`, базовым провайдером `Meta Llama` и списком лучших провайдеров, таких как `AllenAI` и `Jmuz`.

**Примеры**:

```python
>>> llama_3_1_405b.name
'llama-3.1-405b'
>>> llama_3_1_405b.base_provider
'Meta Llama'
>>> llama_3_1_405b.best_provider
<g4f.Provider.IterListProvider object at 0x...>
```

### `llama_3_2_1b`

```python
llama_3_2_1b = Model(
    name          = "llama-3.2-1b",
    base_provider = "Meta Llama",
    best_provider = Cloudflare
)
```

**Назначение**: Определяет модель `llama-3.2-1b` с указанием базового провайдера `Meta Llama` и лучшего провайдера `Cloudflare`.

**Параметры**:
- `name` (str): Имя модели (`llama-3.2-1b`).
- `base_provider` (str): Базовый провайдер (`Meta Llama`).
- `best_provider` (ProviderType): Лучший провайдер (`Cloudflare`).

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем `llama-3.2-1b`, базовым провайдером `Meta Llama` и лучшим провайдером `Cloudflare`.

**Примеры**:

```python
>>> llama_3_2_1b.name
'llama-3.2-1b'
>>> llama_3_2_1b.base_provider
'Meta Llama'
>>> llama_3_2_1b.best_provider
<g4f.Provider.Cloudflare object at 0x...>
```

### `llama_3_2_3b`

```python
llama_3_2_3b = Model(
    name          = "llama-3.2-3b",
    base_provider = "Meta Llama",
    best_provider = Glider
)
```

**Назначение**: Определяет модель `llama-3.2-3b` с указанием базового провайдера `Meta Llama` и лучшего провайдера `Glider`.

**Параметры**:
- `name` (str): Имя модели (`llama-3.2-3b`).
- `base_provider` (str): Базовый провайдер (`Meta Llama`).
- `best_provider` (ProviderType): Лучший провайдер (`Glider`).

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем `llama-3.2-3b`, базовым провайдером `Meta Llama` и лучшим провайдером `Glider`.

**Примеры**:

```python
>>> llama_3_2_3b.name
'llama-3.2-3b'
>>> llama_3_2_3b.base_provider
'Meta Llama'
>>> llama_3_2_3b.best_provider
<g4f.Provider.Glider object at 0x...>
```

### `llama_3_2_11b`

```python
llama_3_2_11b = VisionModel(
    name          = "llama-3.2-11b",
    base_provider = "Meta Llama",
    best_provider = IterListProvider([Jmuz, HuggingChat, HuggingFace])
)
```

**Назначение**: Определяет визуальную модель `llama-3.2-11b` с указанием базового провайдера `Meta Llama` и списка лучших провайдеров.

**Параметры**:
- `name` (str): Имя модели (`llama-3.2-11b`).
- `base_provider` (str): Базовый провайдер (`Meta Llama`).
- `best_provider` (ProviderType): Список предпочтительных провайдеров, использующих `IterListProvider`.

**Возвращает**:
- `VisionModel`: Экземпляр класса `VisionModel` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `VisionModel` с именем `llama-3.2-11b`, базовым провайдером `Meta Llama` и списком лучших провайдеров, таких как `Jmuz`, `HuggingChat` и `HuggingFace`.

**Примеры**:

```python
>>> llama_3_2_11b.name
'llama-3.2-11b'
>>> llama_3_2_11b.base_provider
'Meta Llama'
>>> llama_3_2_11b.best_provider
<g4f.Provider.IterListProvider object at 0x...>
```

### `llama_3_2_90b`

```python
llama_3_2_90b = Model(
    name          = "llama-3.2-90b",
    base_provider = "Meta Llama",
    best_provider = IterListProvider([DeepInfraChat, Jmuz])
)
```

**Назначение**: Определяет модель `llama-3.2-90b` с указанием базового провайдера `Meta Llama` и списка лучших провайдеров.

**Параметры**:
- `name` (str): Имя модели (`llama-3.2-90b`).
- `base_provider` (str): Базовый провайдер (`Meta Llama`).
- `best_provider` (ProviderType): Список предпочтительных провайдеров, использующих `IterListProvider`.

**Возвращает**:
- `Model`: Экземпляр класса `Model` с указанными параметрами.

**Как работает функция**:

1. Создается экземпляр класса `Model` с именем `llama-3.2-90b`, базовым провайдером `Meta Llama` и списком лучших провайдеров, таких как `DeepInfraChat` и `Jmuz`.

**Примеры**: