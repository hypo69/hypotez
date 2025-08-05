# Vision Images Example

## Overview

This file demonstrates how to process images using GPT-4 Free, a powerful open-source implementation of GPT-4. This example showcases the usage of GPT-4 Free for image recognition tasks.

## Details

This script utilizes GPT-4 Free's image processing capabilities to analyze both remote and local images.  It utilizes the `g4f` library to interact with the GPT-4 Free API and perform image-based text generation.

## Classes

This example doesn't involve defining any custom classes. It relies on existing classes from the `g4f` library.

## Functions

This example does not define any functions.

## Code Breakdown

### Example with Remote Image

```python
# Processing remote image
remote_image = requests.get("https://raw.githubusercontent.com/xtekky/gpt4free/refs/heads/main/docs/images/cat.jpeg", stream=True).content
response_remote = client.chat.completions.create(
    model=g4f.models.default_vision,
    messages=[
        {"role": "user", "content": "What are on this image?"}
    ],
    image=remote_image
)
print("Response for remote image:")
print(response_remote.choices[0].message.content)
```
1. **Fetching a remote image**: The code retrieves a remote image by making an HTTP request to a GitHub repository using the `requests` library. The `stream=True` parameter helps handle large images efficiently.
2. **Sending the image to GPT-4 Free**: The retrieved image is sent to the GPT-4 Free API using the `client.chat.completions.create` method. The `model` argument is set to `g4f.models.default_vision`, which specifies the vision-capable model for image analysis. The prompt "What are on this image?" is included in the `messages` list, instructing the model to describe the image content.
3. **Receiving and printing the response**: GPT-4 Free returns a text description based on the image. The `response_remote.choices[0].message.content` attribute extracts the generated text, which is then printed to the console.

### Example with Local Image

```python
# Processing local image
local_image = open("docs/images/cat.jpeg", "rb")
response_local = client.chat.completions.create(
    model=g4f.models.default_vision,
    messages=[
        {"role": "user", "content": "What are on this image?"}
    ],
    image=local_image
)
print("Response for local image:")
print(response_local.choices[0].message.content)
local_image.close()  # Close file after use
```
1. **Opening the local image**: The code opens a local image file (`"docs/images/cat.jpeg"`) in binary read mode (`"rb"`).
2. **Sending the image to GPT-4 Free**: The opened image file is passed to the `client.chat.completions.create` method, following the same procedure as with the remote image.
3. **Receiving and printing the response**:  GPT-4 Free generates a text description for the local image. The description is printed to the console, and the image file is closed to prevent resource leaks.

## Example Usage

This example demonstrates how to use GPT-4 Free to analyze both remote and local images:
1. **Remote image**: 
  - Download an image from the internet or use an image that is publicly available on the internet.
  - Replace `"https://raw.githubusercontent.com/xtekky/gpt4free/refs/heads/main/docs/images/cat.jpeg"` with the URL of your image.
2. **Local image**: 
  - Place an image in the `docs/images` directory.
  - Modify `"docs/images/cat.jpeg"` to reflect the path of your image file.

## Conclusion

This script provides a comprehensive guide to using GPT-4 Free for image processing. It demonstrates how to analyze both remote and local images and receive descriptive responses. The script showcases the versatility of GPT-4 Free and how it can be integrated into various applications involving image analysis.