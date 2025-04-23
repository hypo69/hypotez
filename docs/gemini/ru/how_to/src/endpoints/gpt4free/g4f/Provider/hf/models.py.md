Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода определяет переменные, содержащие списки моделей для обработки текста и изображений, а также словарь с псевдонимами моделей. Он также устанавливает модели, используемые по умолчанию для обработки текста и изображений. Этот код используется для настройки и выбора моделей, используемых в сервисе.

Шаги выполнения
-------------------------
1. Определяется переменная `default_model`, которая содержит имя модели, используемой по умолчанию для обработки текста ("Qwen/Qwen2.5-72B-Instruct").
2. Определяется переменная `default_image_model`, которая содержит имя модели, используемой по умолчанию для обработки изображений ("black-forest-labs/FLUX.1-dev").
3. Определяется список `image_models`, содержащий имена моделей для обработки изображений.
4. Определяется список `text_models`, содержащий имена моделей для обработки текста.
5. Определяется список `fallback_models`, который объединяет модели для обработки текста и изображений.
6. Определяется словарь `model_aliases`, который содержит псевдонимы моделей для удобства их использования. Ключи словаря - это псевдонимы, а значения - соответствующие имена моделей.
7. Определяется список `extra_models`, содержащий дополнительные модели.
8. Определяется переменная `default_vision_model`, которая содержит имя модели, используемой по умолчанию для обработки изображений ("meta-llama/Llama-3.2-11B-Vision-Instruct").
9. Определяется переменная `default_llama_model`, которая содержит имя модели llama, используемой по умолчанию для обработки текста ("meta-llama/Llama-3.3-70B-Instruct").
10. Определяется список `vision_models`, содержащий имена моделей для обработки изображений.

Пример использования
-------------------------

```python
                default_model = "Qwen/Qwen2.5-72B-Instruct"
default_image_model = "black-forest-labs/FLUX.1-dev"
image_models = [    
    default_image_model,
    "black-forest-labs/FLUX.1-schnell",
]
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
fallback_models = text_models + image_models
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
extra_models = [
    "meta-llama/Llama-3.2-11B-Vision-Instruct",
    "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
    "NousResearch/Hermes-3-Llama-3.1-8B",
]
default_vision_model = "meta-llama/Llama-3.2-11B-Vision-Instruct"
default_llama_model = "meta-llama/Llama-3.3-70B-Instruct"
vision_models = [default_vision_model, "Qwen/Qwen2-VL-7B-Instruct"]