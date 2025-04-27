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
This code snippet implements a function `promote_post` that manages the promotion of a Facebook post with a title, description, and media files. It utilizes a Driver instance to interact with the webpage and performs the following actions:

- Sends the title and description to the post message box using the `post_title` function.
- Uploads media files to the images section and updates captions asynchronously using the `upload_media` function.
- Completes editing and publishes the post.

Execution Steps
-------------------------
1. Calls `post_title` function to send the title and description to the post message box.
2. Calls `upload_media` function to upload media files and update captions asynchronously.
3. Executes the "finish editing" button locator.
4. Executes the "publish" button locator to publish the post.

Usage Example
-------------------------

```python
    from src.endpoints.advertisement.facebook.scenarios.post_message_async import promote_post
    from src.webdriver.driver import Driver
    from types import SimpleNamespace

    driver = Driver(...) # Initialize Driver instance
    category = SimpleNamespace(title="Campaign Title", description="Campaign Description") # Define campaign details
    products = [SimpleNamespace(local_image_path='path/to/image.jpg', ...)] # Define product details with media paths

    await promote_post(driver, category, products) # Promote the post
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".