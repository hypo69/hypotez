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
This code block defines a function `convert_images` that converts WebP images to PNG format. It iterates through all WebP files in a specified directory, converts each file to PNG, and saves the output to another directory. The conversion process relies on the `webp2png` function from the `src.utils.convertors.webp2png` module. 

Execution Steps
-------------------------
1. **Get WebP File List**: The code first retrieves a list of WebP file names from the specified source directory using the `get_filenames` function.
2. **Iterate Through Files**: It then iterates through each WebP file in the list.
3. **Generate PNG File Path**: For each WebP file, it constructs the corresponding PNG file path by using the `stem` attribute (the file name without the extension) and appending `.png`.
4. **Perform WebP to PNG Conversion**: The code calls the `webp2png` function, passing the WebP file path and the generated PNG file path as arguments. The `webp2png` function performs the actual conversion.
5. **Print Conversion Result**: The result of the `webp2png` function is printed to the console.

Usage Example
-------------------------

```python
    # Define the directories for WebP and PNG images
    webp_dir = gs.path.google_drive / 'kazarinov' / 'raw_images_from_openai'
    png_dir = gs.path.google_drive / 'kazarinov' / 'converted_images'
    print(f"from: {webp_dir=}\\nto:{png_dir=}")
    # Run the conversion
    convert_images(webp_dir, png_dir)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".