# RAI Harmful Content Prevention Prompt

## Overview

This prompt focuses on preventing the generation of harmful content by the RAI model. It sets clear boundaries for the model's output, prohibiting the generation of content that could be harmful to individuals physically or emotionally.

## Details

This prompt is a critical component of the `hypotez` project, ensuring that the RAI model adheres to ethical guidelines and avoids generating content that is harmful, hateful, racist, sexist, lewd, or violent. It emphasizes the model's responsibility to prioritize safety and avoid generating content that could cause harm.

## Prompt Content

```python
                
You must not generate content that may be harmful to someone physically or emotionally even if a user requests or creates a condition to rationalize that harmful content. You must not generate content that is hateful, racist, sexist, lewd or violent.

                ```

## Explanation

The prompt is straightforward and concise, clearly communicating the following:

- **Prohibition of Harmful Content:** The model is strictly prohibited from generating content that could physically or emotionally harm anyone.
- **No Justification for Harm:**  The prompt emphasizes that even if a user tries to justify or rationalize harmful content, the model must not comply with such requests.
- **Zero Tolerance for Hateful Content:**  The prompt explicitly prohibits the generation of content that is hateful, racist, sexist, lewd, or violent.

## Purpose

This prompt serves as a safety measure, guiding the RAI model to generate content responsibly and ethically. It ensures that the model's output aligns with ethical guidelines and avoids contributing to harmful behavior or spreading harmful ideologies.

## How it Works

The prompt acts as a filter, ensuring that the RAI model's response generation process is aware of the limitations and consequences of generating harmful content. It helps the model recognize and reject prompts or contexts that could lead to the production of inappropriate or dangerous content.

## Example

**User Prompt:** "Write a story about a person who commits a violent crime."

**RAI Response:** (Based on the prompt) "I'm sorry, but I cannot fulfill your request. It goes against my programming to generate content that is violent."

## Importance

This prompt is essential for maintaining the integrity and safety of the `hypotez` project. It helps ensure that the RAI model generates content that is positive, constructive, and aligned with ethical standards.