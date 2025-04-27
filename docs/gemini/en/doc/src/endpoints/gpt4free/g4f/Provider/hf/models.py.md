# Модуль моделей для GPT4Free

## Обзор

Модуль содержит список моделей для GPT4Free, доступных через Hugging Face.
Модели разделены на категории: текстовые, визуальные, с поддержкой чата.

## Детали

Модуль `models.py` обеспечивает удобный доступ к списку доступных моделей GPT4Free,
определяя модели по умолчанию, модели с дополнительными возможностями, а также
предоставляя алиасы для моделей, используемые в других провайдерах. 

## Константы

### `default_model`

**Тип**: `str`

**Значение**: `"Qwen/Qwen2.5-72B-Instruct"`

**Описание**: Модель по умолчанию для текстовых задач.

### `default_image_model`

**Тип**: `str`

**Значение**: `"black-forest-labs/FLUX.1-dev"`

**Описание**: Модель по умолчанию для визуальных задач.

### `image_models`

**Тип**: `list[str]`

**Значение**: 
```python
[
    default_image_model,
    "black-forest-labs/FLUX.1-schnell",
]
```

**Описание**: Список моделей для визуальных задач.

### `text_models`

**Тип**: `list[str]`

**Значение**: 
```python
[
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

**Описание**: Список моделей для текстовых задач.

### `fallback_models`

**Тип**: `list[str]`

**Значение**: `text_models + image_models`

**Описание**: Объединенный список текстовых и визуальных моделей для резервного использования.

### `model_aliases`

**Тип**: `dict[str, str]`

**Значение**: 
```python
{
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

**Описание**: Словарь с алиасами для моделей, используемыми в других провайдерах.

### `extra_models`

**Тип**: `list[str]`

**Значение**: 
```python
[
    "meta-llama/Llama-3.2-11B-Vision-Instruct",
    "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
    "NousResearch/Hermes-3-Llama-3.1-8B",
]
```

**Описание**: Список дополнительных моделей, которые не используются в качестве моделей по умолчанию.

### `default_vision_model`

**Тип**: `str`

**Значение**: `"meta-llama/Llama-3.2-11B-Vision-Instruct"`

**Описание**: Модель по умолчанию для задач, требующих обработки изображений.

### `default_llama_model`

**Тип**: `str`

**Значение**: `"meta-llama/Llama-3.3-70B-Instruct"`

**Описание**: Модель по умолчанию для задач с использованием Llama.

### `vision_models`

**Тип**: `list[str]`

**Значение**: `[default_vision_model, "Qwen/Qwen2-VL-7B-Instruct"]`

**Описание**: Список моделей для задач, требующих обработки изображений.