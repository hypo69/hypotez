# Модуль для определения моделей G4F

## Обзор

Этот модуль определяет классы моделей, используемых в G4F (Generative Functions for Frontend).
Он содержит классы для каждой модели, определяющие их имя, базового провайдера и лучшего провайдера.
Модуль также содержит класс `ModelUtils`, который предоставляет словарь для преобразования строковых идентификаторов моделей в соответствующие классы моделей.

## Подробнее

Модуль предоставляет удобный способ определения и управления различными моделями, используемыми в G4F.
Каждая модель представлена классом, содержащим информацию о ее имени, базовом провайдере и лучшем провайдере.
Это позволяет легко настраивать и переключаться между различными моделями в приложении.

## Классы

### `Model`

Описание: Класс, содержащий в себе определения для различных моделей.

**Вложенные классы**:
- `model`: Базовый класс для определения атрибутов модели.
- `gpt_35_turbo`: Определяет модель `gpt-3.5-turbo`.
- `gpt_35_turbo_0613`: Определяет модель `gpt-3.5-turbo-0613`.
- `gpt_35_turbo_16k_0613`: Определяет модель `gpt-3.5-turbo-16k-0613`.
- `gpt_35_turbo_16k`: Определяет модель `gpt-3.5-turbo-16k`.
- `gpt_4_dev`: Определяет модель `gpt-4-for-dev`.
- `gpt_4`: Определяет модель `gpt-4`.
- `claude_instant_v1_100k`: Определяет модель `claude-instant-v1-100k`.
- `claude_instant_v1`: Определяет модель `claude-instant-v1`.
- `claude_v1_100k`: Определяет модель `claude-v1-100k`.
- `claude_v1`: Определяет модель `claude-v1`.
- `alpaca_7b`: Определяет модель `alpaca-7b`.
- `stablelm_tuned_alpha_7b`: Определяет модель `stablelm-tuned-alpha-7b`.
- `bloom`: Определяет модель `bloom`.
- `bloomz`: Определяет модель `bloomz`.
- `flan_t5_xxl`: Определяет модель `flan-t5-xxl`.
- `flan_ul2`: Определяет модель `flan-ul2`.
- `gpt_neox_20b`: Определяет модель `gpt-neox-20b`.
- `oasst_sft_4_pythia_12b_epoch_35`: Определяет модель `oasst-sft-4-pythia-12b-epoch-3.5`.
- `santacoder`: Определяет модель `santacoder`.
- `command_medium_nightly`: Определяет модель `command-medium-nightly`.
- `command_xlarge_nightly`: Определяет модель `command-xlarge-nightly`.
- `code_cushman_001`: Определяет модель `code-cushman-001`.
- `code_davinci_002`: Определяет модель `code-davinci-002`.
- `text_ada_001`: Определяет модель `text-ada-001`.
- `text_babbage_001`: Определяет модель `text-babbage-001`.
- `text_curie_001`: Определяет модель `text-curie-001`.
- `text_davinci_002`: Определяет модель `text-davinci-002`.
- `text_davinci_003`: Определяет модель `text-davinci-003`.
- `palm`: Определяет модель `palm2`.
- `falcon_40b`: Определяет модель `falcon-40b`.
- `falcon_7b`: Определяет модель `falcon-7b`.
- `llama_13b`: Определяет модель `llama-13b`.

### `ModelUtils`

**Описание**: Класс, предоставляющий утилиты для работы с моделями.

**Атрибуты**:
- `convert` (dict): Словарь, преобразующий строковые идентификаторы моделей в соответствующие классы моделей.

```python
class ModelUtils:
    convert: dict = {
        'gpt-3.5-turbo': Model.gpt_35_turbo,
        'gpt-3.5-turbo-0613': Model.gpt_35_turbo_0613,
        'gpt-4': Model.gpt_4,
        'gpt-4-for-dev': Model.gpt_4_dev,
        'gpt-3.5-turbo-16k': Model.gpt_35_turbo_16k,
        'gpt-3.5-turbo-16k-0613': Model.gpt_35_turbo_16k_0613,
        
        'claude-instant-v1-100k': Model.claude_instant_v1_100k,
        'claude-v1-100k': Model.claude_v1_100k,
        'claude-instant-v1': Model.claude_instant_v1,
        'claude-v1': Model.claude_v1,
        
        'alpaca-7b': Model.alpaca_7b,
        'stablelm-tuned-alpha-7b': Model.stablelm_tuned_alpha_7b,
        
        'bloom': Model.bloom,
        'bloomz': Model.bloomz,
        
        'flan-t5-xxl': Model.flan_t5_xxl,
        'flan-ul2': Model.flan_ul2,
        
        'gpt-neox-20b': Model.gpt_neox_20b,
        'oasst-sft-4-pythia-12b-epoch-3.5': Model.oasst_sft_4_pythia_12b_epoch_35,
        'santacoder': Model.santacoder,
        
        'command-medium-nightly': Model.command_medium_nightly,
        'command-xlarge-nightly': Model.command_xlarge_nightly,
        
        'code-cushman-001': Model.code_cushman_001,
        'code-davinci-002': Model.code_davinci_002,
        
        'text-ada-001': Model.text_ada_001,
        'text-babbage-001': Model.text_babbage_001,
        'text-curie-001': Model.text_curie_001,
        'text-davinci-002': Model.text_davinci_002,
        'text-davinci-003': Model.text_davinci_003,
        
        'palm2': Model.palm,
        'palm': Model.palm,
        'google': Model.palm,
        'google-bard': Model.palm,
        'google-palm': Model.palm,
        'bard': Model.palm,
        
        'falcon-40b': Model.falcon_40b,
        'falcon-7b': Model.falcon_7b,
        'llama-13b': Model.llama_13b,
    }
```

**Принцип работы**:
   - `ModelUtils.convert` - это словарь, который связывает строковое имя модели с соответствующим классом модели.
     Это позволяет легко получать класс модели по ее имени.

**Примеры**:

```python
model_class = ModelUtils.convert['gpt-3.5-turbo']
print(model_class.name)  # Вывод: gpt-3.5-turbo