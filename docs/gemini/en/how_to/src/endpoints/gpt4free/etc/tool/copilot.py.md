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
This Python code snippet defines a series of functions used to interact with GitHub and GPT-4Free API for automated pull request review. The code retrieves pull request details, diff information, analyzes code changes, and generates review comments based on the analysis.

Execution Steps
-------------------------
1. **Initialization**: 
    - Imports required libraries.
    - Sets up environment variables for GitHub and GPT-4Free API credentials.
2. **Retrieve Pull Request Details**:
    - The `get_pr_details` function retrieves the pull request details from GitHub using the provided GitHub token and repository name.
3. **Fetch Diff**:
    - The `get_diff` function fetches the diff of the pull request from the provided diff URL.
4. **Parse JSON and Markdown**:
    - The `read_json` and `read_text` functions parse JSON and Markdown code blocks from strings.
5. **Get AI Response**:
    - The `get_ai_response` function sends a prompt to GPT-4Free API and receives a response. The response is either parsed as JSON or returned as a string depending on the `as_json` parameter.
6. **Analyze Code Changes**:
    - The `analyze_code` function analyzes the diff of the pull request to identify code changes. It generates prompts for GPT-4Free to review the code changes and create review comments.
7. **Create Prompts for AI**:
    - The `create_analyze_prompt` function creates a prompt for GPT-4Free based on the code changes, pull request details, and a predefined format for the response.
    - The `create_review_prompt` function creates a prompt for GPT-4Free to write a general review comment based on the pull request details and diff.
8. **Main Function**:
    - The `main` function coordinates the execution of the code. It retrieves pull request details, diff, and uses the AI functions to generate review comments and post them to GitHub.

Usage Example
-------------------------

```python
    # Set environment variables for GitHub and GPT-4Free API credentials
    os.environ['GITHUB_TOKEN'] = 'your_github_token'
    os.environ['GITHUB_REPOSITORY'] = 'your_github_repo'
    os.environ['G4F_PROVIDER'] = 'your_g4f_provider'
    os.environ['G4F_MODEL'] = 'gpt-4'  # or other supported GPT-4Free models

    # Run the main function
    main()
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".