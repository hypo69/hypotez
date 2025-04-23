# Модуль `models.py`

## Обзор

Модуль `models.py` содержит определения классов, представляющих различные модели обработки естественного языка (NLP) и инструменты для работы с этими моделями. Он включает классы для каждой модели, определяющие их имена, базовых провайдеров и лучших провайдеров. Также модуль содержит класс `ModelUtils` для конвертации строковых идентификаторов моделей в соответствующие классы моделей.

## Подробней

Этот модуль предоставляет структуру для определения и управления различными моделями, используемыми в приложении. Каждая модель представлена классом внутри класса `Model`, что позволяет удобно группировать и идентифицировать модели. `ModelUtils` предоставляет механизм для динамического выбора класса модели на основе строкового идентификатора. Это позволяет упростить конфигурацию и выбор моделей во время выполнения.

## Классы

### `Model`

Класс `Model` служит контейнером для вложенных классов, каждый из которых представляет конкретную модель.

### `Model.model`

**Описание**: Базовый класс для определения атрибутов модели.

**Атрибуты**:
- `name` (str): Имя модели.
- `base_provider` (str): Базовый провайдер модели.
- `best_provider` (str): Лучший провайдер модели.

### `Model.gpt_35_turbo`

**Описание**: Представляет модель `gpt-3.5-turbo`.

**Атрибуты**:
- `name` (str): Имя модели (`gpt-3.5-turbo`).
- `base_provider` (str): Базовый провайдер (`openai`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Mishalsgpt).

### `Model.gpt_35_turbo_0613`

**Описание**: Представляет модель `gpt-3.5-turbo-0613`.

**Атрибуты**:
- `name` (str): Имя модели (`gpt-3.5-turbo-0613`).
- `base_provider` (str): Базовый провайдер (`openai`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Gravityengine).

### `Model.gpt_35_turbo_16k_0613`

**Описание**: Представляет модель `gpt-3.5-turbo-16k-0613`.

**Атрибуты**:
- `name` (str): Имя модели (`gpt-3.5-turbo-16k-0613`).
- `base_provider` (str): Базовый провайдер (`openai`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Mishalsgpt).

### `Model.gpt_35_turbo_16k`

**Описание**: Представляет модель `gpt-3.5-turbo-16k`.

**Атрибуты**:
- `name` (str): Имя модели (`gpt-3.5-turbo-16k`).
- `base_provider` (str): Базовый провайдер (`openai`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Gravityengine).

### `Model.gpt_4_dev`

**Описание**: Представляет модель `gpt-4-for-dev`.

**Атрибуты**:
- `name` (str): Имя модели (`gpt-4-for-dev`).
- `base_provider` (str): Базовый провайдер (`openai`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Phind).

### `Model.gpt_4`

**Описание**: Представляет модель `gpt-4`.

**Атрибуты**:
- `name` (str): Имя модели (`gpt-4`).
- `base_provider` (str): Базовый провайдер (`openai`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.ChatgptAi).
- `best_providers` (list): Список лучших провайдеров ([Provider.Bing, Provider.Lockchat]).

### `Model.claude_instant_v1_100k`

**Описание**: Представляет модель `claude-instant-v1-100k`.

**Атрибуты**:
- `name` (str): Имя модели (`claude-instant-v1-100k`).
- `base_provider` (str): Базовый провайдер (`anthropic`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.claude_instant_v1`

**Описание**: Представляет модель `claude-instant-v1`.

**Атрибуты**:
- `name` (str): Имя модели (`claude-instant-v1`).
- `base_provider` (str): Базовый провайдер (`anthropic`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.claude_v1_100k`

**Описание**: Представляет модель `claude-v1-100k`.

**Атрибуты**:
- `name` (str): Имя модели (`claude-v1-100k`).
- `base_provider` (str): Базовый провайдер (`anthropic`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.claude_v1`

**Описание**: Представляет модель `claude-v1`.

**Атрибуты**:
- `name` (str): Имя модели (`claude-v1`).
- `base_provider` (str): Базовый провайдер (`anthropic`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.alpaca_7b`

**Описание**: Представляет модель `alpaca-7b`.

**Атрибуты**:
- `name` (str): Имя модели (`alpaca-7b`).
- `base_provider` (str): Базовый провайдер (`replicate`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.stablelm_tuned_alpha_7b`

**Описание**: Представляет модель `stablelm-tuned-alpha-7b`.

**Атрибуты**:
- `name` (str): Имя модели (`stablelm-tuned-alpha-7b`).
- `base_provider` (str): Базовый провайдер (`replicate`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.bloom`

**Описание**: Представляет модель `bloom`.

**Атрибуты**:
- `name` (str): Имя модели (`bloom`).
- `base_provider` (str): Базовый провайдер (`huggingface`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.bloomz`

**Описание**: Представляет модель `bloomz`.

**Атрибуты**:
- `name` (str): Имя модели (`bloomz`).
- `base_provider` (str): Базовый провайдер (`huggingface`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.flan_t5_xxl`

**Описание**: Представляет модель `flan-t5-xxl`.

**Атрибуты**:
- `name` (str): Имя модели (`flan-t5-xxl`).
- `base_provider` (str): Базовый провайдер (`huggingface`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.flan_ul2`

**Описание**: Представляет модель `flan-ul2`.

**Атрибуты**:
- `name` (str): Имя модели (`flan-ul2`).
- `base_provider` (str): Базовый провайдер (`huggingface`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.gpt_neox_20b`

**Описание**: Представляет модель `gpt-neox-20b`.

**Атрибуты**:
- `name` (str): Имя модели (`gpt-neox-20b`).
- `base_provider` (str): Базовый провайдер (`huggingface`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.oasst_sft_4_pythia_12b_epoch_35`

**Описание**: Представляет модель `oasst-sft-4-pythia-12b-epoch-3.5`.

**Атрибуты**:
- `name` (str): Имя модели (`oasst-sft-4-pythia-12b-epoch-3.5`).
- `base_provider` (str): Базовый провайдер (`huggingface`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.santacoder`

**Описание**: Представляет модель `santacoder`.

**Атрибуты**:
- `name` (str): Имя модели (`santacoder`).
- `base_provider` (str): Базовый провайдер (`huggingface`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.command_medium_nightly`

**Описание**: Представляет модель `command-medium-nightly`.

**Атрибуты**:
- `name` (str): Имя модели (`command-medium-nightly`).
- `base_provider` (str): Базовый провайдер (`cohere`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.command_xlarge_nightly`

**Описание**: Представляет модель `command-xlarge-nightly`.

**Атрибуты**:
- `name` (str): Имя модели (`command-xlarge-nightly`).
- `base_provider` (str): Базовый провайдер (`cohere`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.code_cushman_001`

**Описание**: Представляет модель `code-cushman-001`.

**Атрибуты**:
- `name` (str): Имя модели (`code-cushman-001`).
- `base_provider` (str): Базовый провайдер (`openai`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.code_davinci_002`

**Описание**: Представляет модель `code-davinci-002`.

**Атрибуты**:
- `name` (str): Имя модели (`code-davinci-002`).
- `base_provider` (str): Базовый провайдер (`openai`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.text_ada_001`

**Описание**: Представляет модель `text-ada-001`.

**Атрибуты**:
- `name` (str): Имя модели (`text-ada-001`).
- `base_provider` (str): Базовый провайдер (`openai`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.text_babbage_001`

**Описание**: Представляет модель `text-babbage-001`.

**Атрибуты**:
- `name` (str): Имя модели (`text-babbage-001`).
- `base_provider` (str): Базовый провайдер (`openai`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.text_curie_001`

**Описание**: Представляет модель `text-curie-001`.

**Атрибуты**:
- `name` (str): Имя модели (`text-curie-001`).
- `base_provider` (str): Базовый провайдер (`openai`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.text_davinci_002`

**Описание**: Представляет модель `text-davinci-002`.

**Атрибуты**:
- `name` (str): Имя модели (`text-davinci-002`).
- `base_provider` (str): Базовый провайдер (`openai`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.text_davinci_003`

**Описание**: Представляет модель `text-davinci-003`.

**Атрибуты**:
- `name` (str): Имя модели (`text-davinci-003`).
- `base_provider` (str): Базовый провайдер (`openai`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Vercel).

### `Model.palm`

**Описание**: Представляет модель `palm2`.

**Атрибуты**:
- `name` (str): Имя модели (`palm2`).
- `base_provider` (str): Базовый провайдер (`google`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.Bard).

### `Model.falcon_40b`

**Описание**: Представляет модель `falcon-40b`.

**Атрибуты**:
- `name` (str): Имя модели (`falcon-40b`).
- `base_provider` (str): Базовый провайдер (`huggingface`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.H2o).

### `Model.falcon_7b`

**Описание**: Представляет модель `falcon-7b`.

**Атрибуты**:
- `name` (str): Имя модели (`falcon-7b`).
- `base_provider` (str): Базовый провайдер (`huggingface`).
- `best_provider` (Provider.Provider): Лучший провайдер (Provider.H2o).

### `Model.llama_13b`

**Description**: Represents the `llama-13b` model.

**Attributes**:
- `name` (str): The name of the model (`llama-13b`).
- `base_provider` (str): The base provider (`huggingface`).
- `best_provider` (Provider.Provider): The best provider (Provider.H2o).

### `ModelUtils`

Класс `ModelUtils` содержит утилиты для работы с моделями, включая преобразование строковых идентификаторов моделей в соответствующие классы моделей.

**Атрибуты**:
- `convert` (dict): Словарь, сопоставляющий строковые идентификаторы моделей с их соответствующими классами.

## Параметры класса `ModelUtils`

- `convert` (dict): Словарь, который содержит соответствия между строковыми именами моделей и классами этих моделей. Используется для удобного доступа к классам моделей по их строковым идентификаторам.
### `ModelUtils.convert`

**Описание**: Словарь, преобразующий строковые идентификаторы моделей в соответствующие классы моделей.

**Примеры**:
- `\'gpt-3.5-turbo\': Model.gpt_35_turbo`
- `\'gpt-4\': Model.gpt_4`
- `\'claude-instant-v1\': Model.claude_instant_v1`