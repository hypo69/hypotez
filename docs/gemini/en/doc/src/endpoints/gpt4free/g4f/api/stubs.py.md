# Stubs for `gpt4free` API

## Overview

This module provides stubs for the `gpt4free` API, including data models and configuration classes. It defines Pydantic models for various requests and responses, enabling structured data validation and serialization.

## Details

This module serves as a foundational element for interacting with the `gpt4free` API. By defining clear data models, it ensures type safety and enhances code maintainability. It's particularly useful when constructing API requests and processing API responses.

## Classes

### `ChatCompletionsConfig`

**Description**: Represents configuration parameters for chat completions requests, including model selection, message history, and various generation settings.

**Inherits**: `pydantic.BaseModel`

**Attributes**:

- `messages`:  `Messages` - List of chat messages used to provide context for the completion.
- `model`: `str` - The ID of the model to use for completion.
- `provider`: `Optional[str]` - The provider (e.g., OpenAI, Google) to use for the request.
- `stream`: `bool` - Whether to stream the response as it's being generated.
- `image`: `Optional[str]` - URL of the image to be analyzed by the model.
- `image_name`: `Optional[str]` - Name for the image.
- `images`: `Optional[list[tuple[str, str]]]` - List of image URLs and names.
- `media`: `Optional[list[tuple[str, str]]]` - List of media URLs and names.
- `modalities`: `Optional[list[str]]` - List of modalities (e.g., "text", "audio") supported by the model.
- `temperature`: `Optional[float]` - Controls the randomness of the generated response.
- `presence_penalty`: `Optional[float]` - Penalizes the model for repeating previous tokens.
- `frequency_penalty`: `Optional[float]` - Penalizes the model for using the same token too often.
- `top_p`: `Optional[float]` - Controls the diversity of the generated response.
- `max_tokens`: `Optional[int]` - Maximum number of tokens to be generated.
- `stop`: `Union[list[str], str, None]` - Stop sequences to signal the end of generation.
- `api_key`: `Optional[str]` - API key for the provider.
- `api_base`: `str` - Base URL for the API.
- `web_search`: `Optional[bool]` - Whether to enable web search for the request.
- `proxy`: `Optional[str]` - Proxy server to use for the request.
- `conversation_id`: `Optional[str]` - ID of the conversation to continue.
- `conversation`: `Optional[dict]` - Conversation history.
- `return_conversation`: `Optional[bool]` - Whether to return the updated conversation history.
- `history_disabled`: `Optional[bool]` - Whether to disable the use of message history.
- `timeout`: `Optional[int]` - Timeout for the request in seconds.
- `tool_calls`: `list` - List of tool calls for the model to use.
- `tools`: `list` - List of tools that the model can use.
- `parallel_tool_calls`: `bool` - Whether to allow parallel tool calls.
- `tool_choice`: `Optional[str]` - Name of the tool to use.
- `reasoning_effort`: `Optional[str]` - Controls the reasoning effort of the model.
- `logit_bias`: `Optional[dict]` - A dictionary of logit bias values.
- `audio`: `Optional[dict]` - Audio-related parameters.
- `response_format`: `Optional[dict]` - Specifies the format of the response.
- `extra_data`: `Optional[dict]` - Additional data to be passed to the model.

### `ImageGenerationConfig`

**Description**: Configuration for image generation requests, including prompt, model, and generation parameters.

**Inherits**: `pydantic.BaseModel`

**Attributes**:

- `prompt`: `str` - Text description of the desired image.
- `model`: `Optional[str]` - ID of the image generation model.
- `provider`: `Optional[str]` - Provider for image generation.
- `response_format`: `Optional[str]` - Format of the response.
- `api_key`: `Optional[str]` - API key for the provider.
- `proxy`: `Optional[str]` - Proxy server to use.
- `width`: `Optional[int]` - Width of the generated image.
- `height`: `Optional[int]` - Height of the generated image.
- `num_inference_steps`: `Optional[int]` - Number of inference steps for image generation.
- `seed`: `Optional[int]` - Random seed for image generation.
- `guidance_scale`: `Optional[int]` - Guidance scale for image generation.
- `aspect_ratio`: `Optional[str]` - Aspect ratio of the generated image.
- `n`: `Optional[int]` - Number of images to generate.
- `negative_prompt`: `Optional[str]` - Text description of what not to include in the image.
- `resolution`: `Optional[str]` - Resolution of the generated image.

### `ProviderResponseModel`

**Description**: Base model for provider responses.

**Inherits**: `pydantic.BaseModel`

**Attributes**:

- `id`: `str` - Unique identifier for the response.
- `object`: `str` - Type of the response, always "provider".
- `created`: `int` - Timestamp of the response creation.
- `url`: `Optional[str]` - URL associated with the response.
- `label`: `Optional[str]` - Label for the response.

### `ProviderResponseDetailModel`

**Description**: Model for detailed provider responses.

**Inherits**: `ProviderResponseModel`

**Attributes**:

- `models`: `list[str]` - List of available models.
- `image_models`: `list[str]` - List of available image generation models.
- `vision_models`: `list[str]` - List of available vision models.
- `params`: `list[str]` - List of available parameters.

### `ModelResponseModel`

**Description**: Model for model responses.

**Inherits**: `pydantic.BaseModel`

**Attributes**:

- `id`: `str` - Unique identifier for the model.
- `object`: `str` - Type of the response, always "model".
- `created`: `int` - Timestamp of the model creation.
- `owned_by`: `Optional[str]` - Owner of the model.

### `UploadResponseModel`

**Description**: Model for upload responses.

**Inherits**: `pydantic.BaseModel`

**Attributes**:

- `bucket_id`: `str` - ID of the storage bucket.
- `url`: `str` - URL of the uploaded file.

### `ErrorResponseModel`

**Description**: Model for error responses.

**Inherits**: `pydantic.BaseModel`

**Attributes**:

- `error`: `ErrorResponseMessageModel` - Error message details.
- `model`: `Optional[str]` - Model associated with the error.
- `provider`: `Optional[str]` - Provider associated with the error.

### `ErrorResponseMessageModel`

**Description**: Model for error message details.

**Inherits**: `pydantic.BaseModel`

**Attributes**:

- `message`: `str` - Error message.

### `FileResponseModel`

**Description**: Model for file responses.

**Inherits**: `pydantic.BaseModel`

**Attributes**:

- `filename`: `str` - Name of the file.

## Inner Functions

None