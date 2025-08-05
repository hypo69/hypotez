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
The code block defines a function `extract_conversations_from_html` that reads a `.html` file and extracts all `<div class="conversation">` elements from it. It then returns each conversation as a `BeautifulSoup` object.

Execution Steps
-------------------------
1. The function takes a file path (`file_path`) as input.
2. It opens the file with `file_path.open('r', encoding='utf-8')`.
3. It parses the HTML content using `BeautifulSoup(file, 'html.parser')`.
4. The code searches for all `<div>` elements with the class "conversation" using `soup.find_all('div', class_='conversation')`.
5. The function iterates over each found conversation and yields it using `yield conversation`.

Usage Example
-------------------------

```python
    # Example usage
    from pathlib import Path
    from src import gs
    from src.suppliers.chat_gpt.converstions_parser import extract_conversations_from_html

    file_path = Path(gs.path.data / 'chat_gpt' / 'chat.html')
    for conversation in extract_conversations_from_html(file_path):
        print(conversation.prettify())  # Print the content of each found conversation
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".