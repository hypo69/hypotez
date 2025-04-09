# Модуль определения моделей для G4F

## Обзор

Модуль `models.py` содержит определения различных языковых моделей, используемых в проекте `g4f` (или FreeGPT WebUI). Он определяет классы для каждой модели, указывая их имя, базового провайдера и рекомендуемого провайдера. Также предоставляет утилиты для преобразования строковых идентификаторов моделей в соответствующие классы моделей.

## Подробнее

Этот модуль играет ключевую роль в конфигурации и выборе моделей для генерации текста, позволяя легко управлять и расширять список поддерживаемых моделей. Определения моделей включают информацию о том, какой провайдер лучше всего подходит для каждой модели, что может влиять на качество и скорость ответов.

## Классы

### `Model`

Класс `Model` служит контейнером для вложенных классов, каждый из которых представляет конкретную языковую модель.

**Принцип работы:**

Класс `Model` не имеет собственных методов и атрибутов, он служит только для организации других классов, представляющих конкретные модели. Каждый вложенный класс содержит статические атрибуты, описывающие характеристики соответствующей модели.

### `Model.model`

Базовый класс модели, определяющий структуру для всех остальных моделей.

**Атрибуты:**

- `name` (str): Имя модели.
- `base_provider` (str): Базовый провайдер модели.
- `best_provider` (str): Рекомендуемый провайдер модели.

### `Model.gpt_35_turbo`

**Описание**: Класс, представляющий модель `gpt-3.5-turbo`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'gpt-3.5-turbo'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Mishalsgpt`.

### `Model.gpt_35_turbo_0613`

**Описание**: Класс, представляющий модель `gpt-3.5-turbo-0613`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'gpt-3.5-turbo-0613'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Gravityengine`.

### `Model.gpt_35_turbo_16k_0613`

**Описание**: Класс, представляющий модель `gpt-3.5-turbo-16k-0613`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'gpt-3.5-turbo-16k-0613'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Mishalsgpt`.

### `Model.gpt_35_turbo_16k`

**Описание**: Класс, представляющий модель `gpt-3.5-turbo-16k`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'gpt-3.5-turbo-16k'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Gravityengine`.

### `Model.gpt_4_dev`

**Описание**: Класс, представляющий модель `gpt-4-for-dev`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'gpt-4-for-dev'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Phind`.

### `Model.gpt_4`

**Описание**: Класс, представляющий модель `gpt-4`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'gpt-4'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.ChatgptAi`.
- `best_providers` (list): Список провайдеров, по умолчанию `[Provider.Bing, Provider.Lockchat]`.

### `Model.claude_instant_v1_100k`

**Описание**: Класс, представляющий модель `claude-instant-v1-100k`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'claude-instant-v1-100k'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'anthropic'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.claude_instant_v1`

**Описание**: Класс, представляющий модель `claude-instant-v1`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'claude-instant-v1'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'anthropic'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.claude_v1_100k`

**Описание**: Класс, представляющий модель `claude-v1-100k`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'claude-v1-100k'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'anthropic'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.claude_v1`

**Описание**: Класс, представляющий модель `claude-v1`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'claude-v1'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'anthropic'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.alpaca_7b`

**Описание**: Класс, представляющий модель `alpaca-7b`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'alpaca-7b'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'replicate'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.stablelm_tuned_alpha_7b`

**Описание**: Класс, представляющий модель `stablelm-tuned-alpha-7b`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'stablelm-tuned-alpha-7b'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'replicate'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.bloom`

**Описание**: Класс, представляющий модель `bloom`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'bloom'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.bloomz`

**Описание**: Класс, представляющий модель `bloomz`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'bloomz'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.flan_t5_xxl`

**Описание**: Класс, представляющий модель `flan-t5-xxl`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'flan-t5-xxl'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.flan_ul2`

**Описание**: Класс, представляющий модель `flan-ul2`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'flan-ul2'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.gpt_neox_20b`

**Описание**: Класс, представляющий модель `gpt-neox-20b`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'gpt-neox-20b'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.oasst_sft_4_pythia_12b_epoch_35`

**Описание**: Класс, представляющий модель `oasst-sft-4-pythia-12b-epoch-3.5`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'oasst-sft-4-pythia-12b-epoch-3.5'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.santacoder`

**Описание**: Класс, представляющий модель `santacoder`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'santacoder'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.command_medium_nightly`

**Описание**: Класс, представляющий модель `command-medium-nightly`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'command-medium-nightly'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'cohere'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.command_xlarge_nightly`

**Описание**: Класс, представляющий модель `command-xlarge-nightly`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'command-xlarge-nightly'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'cohere'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.code_cushman_001`

**Описание**: Класс, представляющий модель `code-cushman-001`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'code-cushman-001'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.code_davinci_002`

**Описание**: Класс, представляющий модель `code-davinci-002`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'code-davinci-002'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.text_ada_001`

**Описание**: Класс, представляющий модель `text-ada-001`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'text-ada-001'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.text_babbage_001`

**Описание**: Класс, представляющий модель `text-babbage-001`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'text-babbage-001'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.text_curie_001`

**Описание**: Класс, представляющий модель `text-curie-001`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'text-curie-001'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.text_davinci_002`

**Описание**: Класс, представляющий модель `text-davinci-002`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'text-davinci-002'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.text_davinci_003`

**Описание**: Класс, представляющий модель `text-davinci-003`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'text-davinci-003'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Vercel`.

### `Model.palm`

**Описание**: Класс, представляющий модель `palm2`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'palm2'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'google'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.Bard`.

### `Model.falcon_40b`

**Описание**: Класс, представляющий модель `falcon-40b`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'falcon-40b'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.H2o`.

### `Model.falcon_7b`

**Описание**: Класс, представляющий модель `falcon-7b`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'falcon-7b'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.H2o`.

### `Model.llama_13b`

**Описание**: Класс, представляющий модель `llama-13b`.

**Атрибуты**:
- `name` (str): Имя модели, по умолчанию `'llama-13b'`.
- `base_provider` (str): Базовый провайдер модели, по умолчанию `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер для модели, по умолчанию `Provider.H2o`.

### `ModelUtils`

Класс `ModelUtils` предоставляет утилиты для работы с моделями, такие как преобразование строковых идентификаторов моделей в соответствующие классы моделей.

**Принцип работы:**

Класс `ModelUtils` содержит словарь `convert`, который отображает строковые идентификаторы моделей на соответствующие классы моделей. Это позволяет легко получать доступ к информации о конкретной модели по её имени.

**Атрибуты**:

- `convert` (dict): Словарь, сопоставляющий строковые идентификаторы моделей с соответствующими классами моделей.

## Функции

В данном модуле отсутствуют отдельные функции, поскольку основная логика реализована через статические атрибуты классов, представляющих модели, и атрибут `convert` класса `ModelUtils`. `ModelUtils.convert` по сути является справочником, позволяющим получить класс модели по её строковому идентификатору.

**Как работает `ModelUtils.convert`:**

1.  **Получение идентификатора модели:** Функция или метод, использующий `ModelUtils.convert`, получает строковый идентификатор модели (например, `"gpt-3.5-turbo"`).
2.  **Поиск класса модели:** Этот идентификатор используется в качестве ключа для доступа к словарю `ModelUtils.convert`.
3.  **Возврат класса модели:** Если идентификатор найден в словаре, возвращается соответствующий класс модели (например, `Model.gpt_35_turbo`). Если идентификатор не найден, может быть возвращено значение по умолчанию или вызвано исключение.
    A (Получение идентификатора модели)
    ↓
    B (Поиск класса модели в ModelUtils.convert)
    │
    C (Возврат класса модели)
    ↓
    D (Использование класса модели)

**Примеры**:

```python
# Получение класса модели gpt-3.5-turbo
model_class = ModelUtils.convert['gpt-3.5-turbo']
print(model_class.name)  # Вывод: gpt-3.5-turbo

# Получение класса модели palm
model_class = ModelUtils.convert['palm']
print(model_class.base_provider)  # Вывод: google
```