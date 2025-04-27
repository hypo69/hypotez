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
The code defines a class named `FacebookPromoter` which handles the promotion of AliExpress products and events in Facebook groups. It uses a WebDriver to automate browser interactions and avoids duplicate posts by tracking already promoted items. 

Execution Steps
-------------------------
1. The code initializes a WebDriver instance (`d`).
2. It creates an instance of `FacebookPromoter`, providing the WebDriver, promoter name, and paths to group data files.
3. The `process_groups()` method is called to start the promotion process. This method iterates through groups, retrieves relevant items for promotion (categories or events), and performs the promotion action. 
4. The `promote()` method handles the actual posting of the promotional content, using the WebDriver to interact with the Facebook group.
5. The code updates the group data after each promotion to prevent duplicate posts.

Usage Example
-------------------------

```python
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter
from src.webdriver.driver import Driver
from src.utils.jjson import j_loads_ns

# Configure WebDriver instance (replace with your actual WebDriver configuration)
d = Driver()

# Create FacebookPromoter instance
promoter = FacebookPromoter(
    d=d, 
    promoter="aliexpress", 
    group_file_paths=["path/to/group/file1.json", "path/to/group/file2.json"]
)

# Start promoting products or events
promoter.process_groups(
    campaign_name="Campaign1",
    events=[], 
    group_categories_to_adv=["sales"],
    language="en",
    currency="USD"
)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".