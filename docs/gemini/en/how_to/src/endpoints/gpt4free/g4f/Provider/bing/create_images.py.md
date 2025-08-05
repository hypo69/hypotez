**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
The provided code implements a function for creating images using Bing's image generation service. It utilizes an `aiohttp` client session to send requests to Bing's API and processes the response to retrieve the generated images.

Execution Steps
-------------------------
1. **Create a Client Session:** The `create_session` function creates a new `aiohttp` client session with the specified cookies and headers.
2. **Send Request:** The `create_images` function sends a POST request to Bing's image creation endpoint with the given prompt.
3. **Handle Rate Limits and Errors:** The code checks for rate limit errors ("0 coins available") and other errors related to prompt blocking or service availability.
4. **Poll for Results:** It polls the status of the image generation process through a specified URL until the generation is complete.
5. **Extract Image URLs:** The `read_images` function extracts the image URLs from the HTML content received in the response.
6. **Return Image URLs:** The function returns a list of URLs to the generated images.

Usage Example
-------------------------

```python
    # Example usage

    from src.endpoints.gpt4free.g4f.Provider.bing.create_images import create_images, create_session
    from src.endpoints.gpt4free.g4f.Provider.bing.login import login

    async def generate_images(prompt: str, cookies: dict, proxy: str = None) -> list[str]:
        """Generates images using Bing's image creation service."""
        async with create_session(cookies, proxy=proxy) as session:
            try:
                images = await create_images(session, prompt)
                return images
            except Exception as e:
                print(f"Error generating images: {e}")

    async def main():
        # Replace with your own login credentials
        credentials = {"username": "your_username", "password": "your_password"}
        cookies = await login(credentials)
        prompt = "A cat wearing a hat"
        images = await generate_images(prompt, cookies)
        print(f"Generated images: {images}")

    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".