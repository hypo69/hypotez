**Instructions for Generating Code Documentation**

How to Use the TextToImageGenerator Class
========================================================================================

Description
-------------------------
The `TextToImageGenerator` class provides functionality to convert text lines into individual PNG images. It allows customization of image appearance, including canvas size, padding, font, background color, and text color. The class utilizes the `Pillow` library for image manipulation.

Execution Steps
-------------------------
1. **Initialization**: Create an instance of the `TextToImageGenerator` class.
2. **Configuration**: Define desired settings such as output directory, canvas size, font, padding, background color, text color, logging level, and clobber option.
3. **Image Generation**: Call the `generate_images()` method with a list of text lines and the configured settings.
4. **Image Saving**: The `generate_images()` method creates PNG images for each line, saving them to the specified output directory.

Usage Example
-------------------------

```python
from src.utils.convertors.png import TextToImageGenerator

# Initialize the generator with custom settings
generator = TextToImageGenerator()
generator.default_output_dir = "./my_images"  # Customize output directory
generator.default_canvas_size = (1280, 720)  # Adjust canvas size
generator.default_font = "arial.ttf"  # Use a custom font

# Define text lines for image generation
lines = ["This is line 1", "This is line 2", "This is line 3"]

# Generate PNG images from the text lines
images = generator.generate_images(lines, output_dir=generator.default_output_dir, font=generator.default_font)

# Print the paths of generated images
print(images)
```

**Additional Notes**

- The `generate_images()` method returns a list of `Path` objects, representing the paths to the generated PNG images.
- The class also includes functions for overlaying images, converting WEBP images to PNG, and setting up logging.
- For more detailed information about the class and its functions, refer to the docstrings within the code.