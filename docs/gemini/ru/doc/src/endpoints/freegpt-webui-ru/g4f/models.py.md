# Модуль для определения моделей G4F

## Обзор

Модуль `models.py` содержит определения различных языковых моделей, используемых в проекте `hypotez` через библиотеку `g4f`. Он определяет класс `Model`, который содержит вложенные классы, представляющие конкретные модели. Каждый вложенный класс определяет атрибуты модели, такие как имя, базовый провайдер и лучший провайдер. Также в модуле присутствует класс `ModelUtils` с методом `convert`, который представляет собой словарь для преобразования строковых идентификаторов моделей в соответствующие классы моделей.

## Подробней

Этот модуль предоставляет централизованное место для определения и управления различными языковыми моделями, используемыми в проекте. Это позволяет легко добавлять новые модели, изменять их параметры и выбирать лучших провайдеров для каждой модели. Класс `ModelUtils` используется для преобразования строковых идентификаторов моделей, полученных извне, в соответствующие классы моделей, что упрощает использование моделей в других частях проекта.

## Классы

### `Model`

**Описание**: Класс `Model` служит контейнером для вложенных классов, каждый из которых представляет конкретную языковую модель.

**Принцип работы**: Класс `Model` не имеет методов, его основная цель - организация вложенных классов моделей.

### `Model.model`

**Описание**: Базовый класс для определения атрибутов моделей.

**Аттрибуты**:
- `name` (str): Имя модели.
- `base_provider` (str): Базовый провайдер модели.
- `best_provider` (str): Лучший провайдер модели.

### `Model.gpt_35_turbo`

**Описание**: Класс, представляющий модель GPT-3.5 Turbo.

**Аттрибуты**:
- `name` (str): Имя модели - `'gpt-3.5-turbo'`.
- `base_provider` (str): Базовый провайдер - `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Mishalsgpt`.

### `Model.gpt_35_turbo_0613`

**Описание**: Класс, представляющий модель GPT-3.5 Turbo 0613.

**Аттрибуты**:
- `name` (str): Имя модели - `'gpt-3.5-turbo-0613'`.
- `base_provider` (str): Базовый провайдер - `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Gravityengine`.

### `Model.gpt_35_turbo_16k_0613`

**Описание**: Класс, представляющий модель GPT-3.5 Turbo 16k 0613.

**Аттрибуты**:
- `name` (str): Имя модели - `'gpt-3.5-turbo-16k-0613'`.
- `base_provider` (str): Базовый провайдер - `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Mishalsgpt`.

### `Model.gpt_35_turbo_16k`

**Описание**: Класс, представляющий модель GPT-3.5 Turbo 16k.

**Аттрибуты**:
- `name` (str): Имя модели - `'gpt-3.5-turbo-16k'`.
- `base_provider` (str): Базовый провайдер - `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Gravityengine`.

### `Model.gpt_4_dev`

**Описание**: Класс, представляющий модель GPT-4 для разработчиков.

**Аттрибуты**:
- `name` (str): Имя модели - `'gpt-4-for-dev'`.
- `base_provider` (str): Базовый провайдер - `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Phind`.

### `Model.gpt_4`

**Описание**: Класс, представляющий модель GPT-4.

**Аттрибуты**:
- `name` (str): Имя модели - `'gpt-4'`.
- `base_provider` (str): Базовый провайдер - `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.ChatgptAi`.
- `best_providers` (list): Список лучших провайдеров - `[Provider.Bing, Provider.Lockchat]`.

### `Model.claude_instant_v1_100k`

**Описание**: Класс, представляющий модель Claude Instant v1 100k.

**Аттрибуты**:
- `name` (str): Имя модели - `'claude-instant-v1-100k'`.
- `base_provider` (str): Базовый провайдер - `'anthropic'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.claude_instant_v1`

**Описание**: Класс, представляющий модель Claude Instant v1.

**Аттрибуты**:
- `name` (str): Имя модели - `'claude-instant-v1'`.
- `base_provider` (str): Базовый провайдер - `'anthropic'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.claude_v1_100k`

**Описание**: Класс, представляющий модель Claude v1 100k.

**Аттрибуты**:
- `name` (str): Имя модели - `'claude-v1-100k'`.
- `base_provider` (str): Базовый провайдер - `'anthropic'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.claude_v1`

**Описание**: Класс, представляющий модель Claude v1.

**Аттрибуты**:
- `name` (str): Имя модели - `'claude-v1'`.
- `base_provider` (str): Базовый провайдер - `'anthropic'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.alpaca_7b`

**Описание**: Класс, представляющий модель Alpaca 7b.

**Аттрибуты**:
- `name` (str): Имя модели - `'alpaca-7b'`.
- `base_provider` (str): Базовый провайдер - `'replicate'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.stablelm_tuned_alpha_7b`

**Описание**: Класс, представляющий модель StableLM Tuned Alpha 7b.

**Аттрибуты**:
- `name` (str): Имя модели - `'stablelm-tuned-alpha-7b'`.
- `base_provider` (str): Базовый провайдер - `'replicate'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.bloom`

**Описание**: Класс, представляющий модель Bloom.

**Аттрибуты**:
- `name` (str): Имя модели - `'bloom'`.
- `base_provider` (str): Базовый провайдер - `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.bloomz`

**Описание**: Класс, представляющий модель Bloomz.

**Аттрибуты**:
- `name` (str): Имя модели - `'bloomz'`.
- `base_provider` (str): Базовый провайдер - `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.flan_t5_xxl`

**Описание**: Класс, представляющий модель FLAN-T5 XXL.

**Аттрибуты**:
- `name` (str): Имя модели - `'flan-t5-xxl'`.
- `base_provider` (str): Базовый провайдер - `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.flan_ul2`

**Описание**: Класс, представляющий модель FLAN-UL2.

**Аттрибуты**:
- `name` (str): Имя модели - `'flan-ul2'`.
- `base_provider` (str): Базовый провайдер - `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.gpt_neox_20b`

**Описание**: Класс, представляющий модель GPT-NeoX 20B.

**Аттрибуты**:
- `name` (str): Имя модели - `'gpt-neox-20b'`.
- `base_provider` (str): Базовый провайдер - `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.oasst_sft_4_pythia_12b_epoch_35`

**Описание**: Класс, представляющий модель oasst-sft-4-pythia-12b-epoch-3.5.

**Аттрибуты**:
- `name` (str): Имя модели - `'oasst-sft-4-pythia-12b-epoch-3.5'`.
- `base_provider` (str): Базовый провайдер - `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.santacoder`

**Описание**: Класс, представляющий модель Santacoder.

**Аттрибуты**:
- `name` (str): Имя модели - `'santacoder'`.
- `base_provider` (str): Базовый провайдер - `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.command_medium_nightly`

**Описание**: Класс, представляющий модель Command Medium Nightly.

**Аттрибуты**:
- `name` (str): Имя модели - `'command-medium-nightly'`.
- `base_provider` (str): Базовый провайдер - `'cohere'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.command_xlarge_nightly`

**Описание**: Класс, представляющий модель Command XLarge Nightly.

**Аттрибуты**:
- `name` (str): Имя модели - `'command-xlarge-nightly'`.
- `base_provider` (str): Базовый провайдер - `'cohere'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.code_cushman_001`

**Описание**: Класс, представляющий модель Code-Cushman-001.

**Аттрибуты**:
- `name` (str): Имя модели - `'code-cushman-001'`.
- `base_provider` (str): Базовый провайдер - `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.code_davinci_002`

**Описание**: Класс, представляющий модель Code-Davinci-002.

**Аттрибуты**:
- `name` (str): Имя модели - `'code-davinci-002'`.
- `base_provider` (str): Базовый провайдер - `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.text_ada_001`

**Описание**: Класс, представляющий модель Text-Ada-001.

**Аттрибуты**:
- `name` (str): Имя модели - `'text-ada-001'`.
- `base_provider` (str): Базовый провайдер - `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.text_babbage_001`

**Описание**: Класс, представляющий модель Text-Babbage-001.

**Аттрибуты**:
- `name` (str): Имя модели - `'text-babbage-001'`.
- `base_provider` (str): Базовый провайдер - `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.text_curie_001`

**Описание**: Класс, представляющий модель Text-Curie-001.

**Аттрибуты**:
- `name` (str): Имя модели - `'text-curie-001'`.
- `base_provider` (str): Базовый провайдер - `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.text_davinci_002`

**Описание**: Класс, представляющий модель Text-Davinci-002.

**Аттрибуты**:
- `name` (str): Имя модели - `'text-davinci-002'`.
- `base_provider` (str): Базовый провайдер - `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.text_davinci_003`

**Описание**: Класс, представляющий модель Text-Davinci-003.

**Аттрибуты**:
- `name` (str): Имя модели - `'text-davinci-003'`.
- `base_provider` (str): Базовый провайдер - `'openai'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Vercel`.

### `Model.palm`

**Описание**: Класс, представляющий модель PaLM.

**Аттрибуты**:
- `name` (str): Имя модели - `'palm2'`.
- `base_provider` (str): Базовый провайдер - `'google'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.Bard`.

### `Model.falcon_40b`

**Описание**: Класс, представляющий модель Falcon-40b.

**Аттрибуты**:
- `name` (str): Имя модели - `'falcon-40b'`.
- `base_provider` (str): Базовый провайдер - `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.H2o`.

### `Model.falcon_7b`

**Описание**: Класс, представляющий модель Falcon-7b.

**Аттрибуты**:
- `name` (str): Имя модели - `'falcon-7b'`.
- `base_provider` (str): Базовый провайдер - `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.H2o`.

### `Model.llama_13b`

**Описание**: Класс, представляющий модель Llama-13b.

**Аттрибуты**:
- `name` (str): Имя модели - `'llama-13b'`.
- `base_provider` (str): Базовый провайдер - `'huggingface'`.
- `best_provider` (Provider.Provider): Лучший провайдер - `Provider.H2o`.

### `ModelUtils`

**Описание**: Класс `ModelUtils` предоставляет утилиты для работы с моделями.

**Методы**:

### `ModelUtils.convert`

**Описание**: `convert` - это словарь, который сопоставляет строковые идентификаторы моделей с соответствующими классами моделей.

**Как работает функция**:

1.  Функция принимает строковый идентификатор модели в качестве ключа.
2.  Она возвращает соответствующий класс модели из словаря `convert`.

**Примеры**:

```python
model_class = ModelUtils.convert['gpt-3.5-turbo'] #  функция возвращает класс Model.gpt_35_turbo
model_class = ModelUtils.convert['llama-13b']    #  функция возвращает класс Model.llama_13b
```
```