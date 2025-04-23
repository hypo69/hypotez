# Модуль `models.py`

## Обзор

Модуль `models.py` предназначен для определения классов, представляющих различные языковые модели, и утилит для работы с ними. Он содержит определения классов для каждой модели, указывая их имя, базового провайдера и лучшего провайдера. Также включает утилитарный класс `ModelUtils` для конвертации строковых идентификаторов моделей в соответствующие классы моделей.

## Детали

Этот модуль предоставляет централизованный способ определения и управления различными языковыми моделями, используемыми в проекте. Он облегчает доступ к информации о моделях, такой как их провайдеры, и упрощает процесс выбора модели для использования.

## Классы

### `Model`

Класс `Model` служит контейнером для вложенных классов, каждый из которых представляет конкретную языковую модель.

#### Вложенные классы:

- `model`:
  - **Описание**: Базовый класс для определения атрибутов модели.
  - **Атрибуты**:
    - `name` (str): Имя модели.
    - `base_provider` (str): Базовый провайдер модели.
    - `best_provider` (str): Лучший провайдер модели.

- `gpt_35_turbo`:
  - **Описание**: Представляет модель GPT-3.5 Turbo.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`gpt-3.5-turbo`).
    - `base_provider` (str): Базовый провайдер (`openai`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Mishalsgpt).

- `gpt_35_turbo_0613`:
  - **Описание**: Представляет модель GPT-3.5 Turbo 0613.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`gpt-3.5-turbo-0613`).
    - `base_provider` (str): Базовый провайдер (`openai`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Gravityengine).

- `gpt_35_turbo_16k_0613`:
  - **Описание**: Представляет модель GPT-3.5 Turbo 16k 0613.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`gpt-3.5-turbo-16k-0613`).
    - `base_provider` (str): Базовый провайдер (`openai`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Mishalsgpt).

- `gpt_35_turbo_16k`:
  - **Описание**: Представляет модель GPT-3.5 Turbo 16k.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`gpt-3.5-turbo-16k`).
    - `base_provider` (str): Базовый провайдер (`openai`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Gravityengine).

- `gpt_4_dev`:
  - **Описание**: Представляет модель GPT-4 для разработчиков.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`gpt-4-for-dev`).
    - `base_provider` (str): Базовый провайдер (`openai`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Phind).

- `gpt_4`:
  - **Описание**: Представляет модель GPT-4.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`gpt-4`).
    - `base_provider` (str): Базовый провайдер (`openai`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.ChatgptAi).
    - `best_providers` (list): Список лучших провайдеров (Provider.Bing, Provider.Lockchat).

- `claude_instant_v1_100k`:
  - **Описание**: Представляет модель Claude Instant v1 100k.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`claude-instant-v1-100k`).
    - `base_provider` (str): Базовый провайдер (`anthropic`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `claude_instant_v1`:
  - **Описание**: Представляет модель Claude Instant v1.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`claude-instant-v1`).
    - `base_provider` (str): Базовый провайдер (`anthropic`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `claude_v1_100k`:
  - **Описание**: Представляет модель Claude v1 100k.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`claude-v1-100k`).
    - `base_provider` (str): Базовый провайдер (`anthropic`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `claude_v1`:
  - **Описание**: Представляет модель Claude v1.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`claude-v1`).
    - `base_provider` (str): Базовый провайдер (`anthropic`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `alpaca_7b`:
  - **Описание**: Представляет модель Alpaca 7b.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`alpaca-7b`).
    - `base_provider` (str): Базовый провайдер (`replicate`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `stablelm_tuned_alpha_7b`:
  - **Описание**: Представляет модель StableLM Tuned Alpha 7b.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`stablelm-tuned-alpha-7b`).
    - `base_provider` (str): Базовый провайдер (`replicate`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `bloom`:
  - **Описание**: Представляет модель Bloom.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`bloom`).
    - `base_provider` (str): Базовый провайдер (`huggingface`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `bloomz`:
  - **Описание**: Представляет модель Bloomz.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`bloomz`).
    - `base_provider` (str): Базовый провайдер (`huggingface`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `flan_t5_xxl`:
  - **Описание**: Представляет модель FLAN-T5 XXL.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`flan-t5-xxl`).
    - `base_provider` (str): Базовый провайдер (`huggingface`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `flan_ul2`:
  - **Описание**: Представляет модель FLAN-UL2.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`flan-ul2`).
    - `base_provider` (str): Базовый провайдер (`huggingface`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `gpt_neox_20b`:
  - **Описание**: Представляет модель GPT-NeoX 20B.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`gpt-neox-20b`).
    - `base_provider` (str): Базовый провайдер (`huggingface`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `oasst_sft_4_pythia_12b_epoch_35`:
  - **Описание**: Представляет модель oasst-sft-4-pythia-12b-epoch-3.5.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`oasst-sft-4-pythia-12b-epoch-3.5`).
    - `base_provider` (str): Базовый провайдер (`huggingface`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `santacoder`:
  - **Описание**: Представляет модель SantaCoder.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`santacoder`).
    - `base_provider` (str): Базовый провайдер (`huggingface`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `command_medium_nightly`:
  - **Описание**: Представляет модель Command Medium Nightly.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`command-medium-nightly`).
    - `base_provider` (str): Базовый провайдер (`cohere`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `command_xlarge_nightly`:
  - **Описание**: Представляет модель Command XLarge Nightly.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`command-xlarge-nightly`).
    - `base_provider` (str): Базовый провайдер (`cohere`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `code_cushman_001`:
  - **Описание**: Представляет модель Code-Cushman-001.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`code-cushman-001`).
    - `base_provider` (str): Базовый провайдер (`openai`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `code_davinci_002`:
  - **Описание**: Представляет модель Code-Davinci-002.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`code-davinci-002`).
    - `base_provider` (str): Базовый провайдер (`openai`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `text_ada_001`:
  - **Описание**: Представляет модель Text-Ada-001.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`text-ada-001`).
    - `base_provider` (str): Базовый провайдер (`openai`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `text_babbage_001`:
  - **Описание**: Представляет модель Text-Babbage-001.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`text-babbage-001`).
    - `base_provider` (str): Базовый провайдер (`openai`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `text_curie_001`:
  - **Описание**: Представляет модель Text-Curie-001.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`text-curie-001`).
    - `base_provider` (str): Базовый провайдер (`openai`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `text_davinci_002`:
  - **Описание**: Представляет модель Text-Davinci-002.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`text-davinci-002`).
    - `base_provider` (str): Базовый провайдер (`openai`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `text_davinci_003`:
  - **Описание**: Представляет модель Text-Davinci-003.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`text-davinci-003`).
    - `base_provider` (str): Базовый провайдер (`openai`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

- `palm`:
  - **Описание**: Представляет модель PaLM 2.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`palm2`).
    - `base_provider` (str): Базовый провайдер (`google`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.Bard).

- `falcon_40b`:
  - **Описание**: Представляет модель Falcon-40b.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`falcon-40b`).
    - `base_provider` (str): Базовый провайдер (`huggingface`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.H2o).

- `falcon_7b`:
  - **Описание**: Представляет модель Falcon-7b.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`falcon-7b`).
    - `base_provider` (str): Базовый провайдер (`huggingface`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.H2o).

- `llama_13b`:
  - **Описание**: Представляет модель Llama-13b.
  - **Наследует**: Нет
  - **Атрибуты**:
    - `name` (str): Имя модели (`llama-13b`).
    - `base_provider` (str): Базовый провайдер (`huggingface`).
    - `best_provider` (Provider.Provider): Лучший провайдер (Provider.H2o).

### `ModelUtils`

Класс `ModelUtils` предоставляет утилиты для работы с моделями.

- **Атрибуты**:
  - `convert` (dict): Словарь, сопоставляющий строковые идентификаторы моделей с соответствующими классами моделей.

  **Принцип работы**:
  - Класс `ModelUtils` содержит словарь `convert`, который позволяет преобразовывать строковые идентификаторы моделей (например, `'gpt-3.5-turbo'`) в соответствующие классы моделей (например, `Model.gpt_35_turbo`). Это упрощает выбор и использование моделей на основе их строковых идентификаторов.

## Примеры

Пример использования класса `ModelUtils` для получения класса модели по её имени:

```python
model_class = ModelUtils.convert['gpt-3.5-turbo']
print(model_class.name) # Вывод: gpt-3.5-turbo
```