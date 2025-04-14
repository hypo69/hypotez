# Модуль определения моделей Hugging Face

## Обзор

Модуль `models.py` содержит определения моделей, используемых в провайдере `hf` (Hugging Face) проекта `hypotez`. Он определяет модели для обработки текста и изображений, а также предоставляет псевдонимы для упрощения их использования.
Модуль содержит список стандартных языковых и графических моделей, а также содержит алиасы для более удобного использования.

## Подробнее

Этот модуль предназначен для централизованного управления списком поддерживаемых моделей Hugging Face. Это позволяет легко добавлять, удалять или изменять модели, используемые в различных частях проекта. Модуль также предоставляет псевдонимы для моделей, что упрощает их использование и позволяет избежать жесткой привязки к конкретным именам моделей.

## Переменные

### `default_model`

```python
default_model = "Qwen/Qwen2.5-72B-Instruct"
```

**Описание**: Определяет модель, используемую по умолчанию для задач обработки текста. В данном случае это `"Qwen/Qwen2.5-72B-Instruct"`.

### `default_image_model`

```python
default_image_model = "black-forest-labs/FLUX.1-dev"
```

**Описание**: Определяет модель, используемую по умолчанию для задач обработки изображений. В данном случае это `"black-forest-labs/FLUX.1-dev"`.

### `image_models`

```python
image_models = [
    default_image_model,
    "black-forest-labs/FLUX.1-schnell",
]
```

**Описание**: Список моделей, поддерживаемых для обработки изображений. Включает модель по умолчанию (`default_image_model`) и `"black-forest-labs/FLUX.1-schnell"`.

### `text_models`

```python
text_models = [
    default_model,
    'meta-llama/Llama-3.3-70B-Instruct',
    'CohereForAI/c4ai-command-r-plus-08-2024',
    'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B',
    'Qwen/QwQ-32B',
    'nvidia/Llama-3.1-Nemotron-70B-Instruct-HF',
    'Qwen/Qwen2.5-Coder-32B-Instruct',
    'meta-llama/Llama-3.2-11B-Vision-Instruct',
    'mistralai/Mistral-Nemo-Instruct-2407',
    'microsoft/Phi-3.5-mini-instruct',
]
```

**Описание**: Список моделей, поддерживаемых для обработки текста. Включает модель по умолчанию (`default_model`) и другие модели, такие как `'meta-llama/Llama-3.3-70B-Instruct'` и т.д.

### `fallback_models`

```python
fallback_models = text_models + image_models
```

**Описание**: Список моделей, используемых в качестве запасных вариантов. Объединяет модели для обработки текста и изображений.

### `model_aliases`

```python
model_aliases = {
    ### Chat ###
    "qwen-2.5-72b": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "llama-3": "meta-llama/Llama-3.3-70B-Instruct",
    "llama-3.3-70b": "meta-llama/Llama-3.3-70B-Instruct",
    "command-r-plus": "CohereForAI/c4ai-command-r-plus-08-2024",
    "deepseek-r1": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    "qwq-32b": "Qwen/QwQ-32B",
    "nemotron-70b": "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
    "qwen-2.5-coder-32b": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "llama-3.2-11b": "meta-llama/Llama-3.2-11B-Vision-Instruct",
    "mistral-nemo": "mistralai/Mistral-Nemo-Instruct-2407",
    "phi-3.5-mini": "microsoft/Phi-3.5-mini-instruct",
    ### Image ###
    "flux": "black-forest-labs/FLUX.1-dev",
    "flux-dev": "black-forest-labs/FLUX.1-dev",
    "flux-schnell": "black-forest-labs/FLUX.1-schnell",
    ### Used in other providers ###
    "qwen-2-vl-7b": "Qwen/Qwen2-VL-7B-Instruct",
    "gemma-2-27b": "google/gemma-2-27b-it",
    "qwen-2-72b": "Qwen/Qwen2-72B-Instruct",
    "qvq-72b": "Qwen/QVQ-72B-Preview",
    "sd-3.5": "stabilityai/stable-diffusion-3.5-large",
}
```

**Описание**: Словарь, содержащий псевдонимы для моделей. Позволяет использовать короткие и понятные имена для обращения к моделям. Например, `"qwen-2.5-72b"` является псевдонимом для `"Qwen/Qwen2.5-Coder-32B-Instruct"`.

### `extra_models`

```python
extra_models = [
    "meta-llama/Llama-3.2-11B-Vision-Instruct",
    "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
    "NousResearch/Hermes-3-Llama-3.1-8B",
]
```

**Описание**: Список дополнительных моделей, которые могут использоваться в проекте.

### `default_vision_model`

```python
default_vision_model = "meta-llama/Llama-3.2-11B-Vision-Instruct"
```

**Описание**: Определяет модель, используемую по умолчанию для задач, связанных с обработкой изображений и зрения. В данном случае это `"meta-llama/Llama-3.2-11B-Vision-Instruct"`.

### `default_llama_model`

```python
default_llama_model = "meta-llama/Llama-3.3-70B-Instruct"
```

**Описание**: Определяет модель Llama, используемую по умолчанию для задач обработки текста. В данном случае это `"meta-llama/Llama-3.3-70B-Instruct"`.

### `vision_models`

```python
vision_models = [default_vision_model, "Qwen/Qwen2-VL-7B-Instruct"]
```

**Описание**: Список моделей, используемых для задач, связанных с компьютерным зрением. Включает модель по умолчанию (`default_vision_model`) и `"Qwen/Qwen2-VL-7B-Instruct"`.