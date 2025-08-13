import os
import re
from deep_translator import GoogleTranslator

def translate_text(text, dest_language="en"):
    """
    Translates text to the destination language.
    """
    if not text.strip():
        return ""
    try:
        return GoogleTranslator(source='auto', target=dest_language).translate(text)
    except Exception as e:
        print(f"Error translating text: {e}")
        return text

def translate_file_content(content):
    """
    Translates Russian comments and docstrings in a Python file content to English.
    """
    # Translate multi-line docstrings """..."""
    translated_content = re.sub(r'"""(.*?)"""', 
                                lambda m: f'"""{translate_text(m.group(1))}"""', 
                                content, 
                                flags=re.DOTALL)
    
    # Translate multi-line docstrings '''...'''
    translated_content = re.sub(r"'''(.*?)'''",
                                lambda m: f"'''{translate_text(m.group(1))}'''",
                                translated_content,
                                flags=re.DOTALL)

    # Translate single-line comments
    translated_content = re.sub(r'#\s*(.*)', 
                                lambda m: f'# {translate_text(m.group(1))}', 
                                translated_content)

    return translated_content

def process_files(src_dir, dest_dir):
    """
    Processes all .py files in the source directory, translates them, 
    and saves them to the destination directory.
    """
    existing_translated_files = set()
    for root, _, files in os.walk(dest_dir):
        for file in files:
            if file.endswith(".py"):
                relative_path = os.path.relpath(os.path.join(root, file), dest_dir)
                existing_translated_files.add(relative_path)

    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py"):
                src_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(src_file_path, src_dir)
                
                if relative_path in existing_translated_files:
                    continue

                dest_file_path = os.path.join(dest_dir, relative_path)

                print(f"Translating {src_file_path}...")
                try:
                    with open(src_file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except UnicodeDecodeError:
                    print(f"Could not read file {src_file_path} with utf-8 encoding. Skipping.")
                    continue

                if not re.search(r'[\u0400-\u04FF]', content):
                    print(f"No Russian text found in {src_file_path}. Copying file as is.")
                    translated_content = content
                else:
                    translated_content = translate_file_content(content)

                os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                with open(dest_file_path, "w", encoding="utf-8") as f:
                    f.write(translated_content)
                print(f"Saved translated file to {dest_file_path}")

if __name__ == "__main__":
    src_directory = "src"
    dest_directory = "src_en"
    process_files(src_directory, dest_directory)