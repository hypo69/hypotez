**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
========================================================================================

Description
-------------------------
This code block provides functionality to download and store images locally with Unicode-safe filenames, returning a list of relative image URLs. It handles various image types, including data URIs, and ensures the correct format for downloaded images.

Execution Steps
-------------------------
1. **Initial Setup:** 
    - Defines a directory for storing generated images (`images_dir`).
    - Defines functions to extract media file extensions, create the images directory if it doesn't exist, and extract original URLs from image parameters.
2. **Media Type Validation:** 
    - Defines a function to check if a given content type is valid for media (image, audio, or video).
3. **Saving Media from Response:**
    - The `save_response_media` function processes a media response, extracts the content type, generates a filename, and saves the media to the `images_dir`.
    - It returns an iterator yielding the appropriate media response object (ImageResponse, AudioResponse, or VideoResponse) based on the content type.
4. **Filename Generation:**
    - The `get_filename` function generates a unique and safe filename based on timestamps, tags, alternative text, and a hash of the image.
5. **Media Copying:** 
    - The `copy_media` function is the main entry point for the image copying process.
    - It takes a list of image URLs, optional parameters (cookies, headers, proxy, alt text, tags, target directory, SSL), and performs the following actions:
        - **Check if the image is already local:** If the URL starts with `/`, it assumes the image is local and returns the URL.
        - **Process individual images:** Calls the `copy_image` function for each image.
        - **Build safe filenames:** Uses the `get_filename` function to create safe filenames.
        - **Handle data URIs:** Extracts data from the data URI and saves it as a file.
        - **Download images:** Downloads images from the provided URLs using an `aiohttp` session, verifying the content type and saving the files to the `images_dir`.
        - **Format verification:** Checks the file format of downloaded images and renames them if needed.
        - **Return relative image URLs:** Returns a list of relative image URLs for the downloaded images.
    - The `copy_image` function handles individual image processing, including downloading, saving, and generating the relative URL.

Usage Example
-------------------------

```python
    from hypotez.src.endpoints.gpt4free.g4f.image.copy_images import copy_media

    async def download_images():
        images = [
            "https://example.com/image1.jpg",
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=",
            "/media/image2.png"
        ]
        result = await copy_media(images, alt="My image", tags=["art", "painting"])
        print(result)  # Output: ["/media/image1.jpg", "/media/image2.png", "/media/image3.png"]

    asyncio.run(download_images())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".