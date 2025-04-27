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
This code block demonstrates a script that automates Facebook advertising campaigns for a specific set of product categories and target audiences. 

Execution Steps
-------------------------
1. **Initialize WebDriver**: The script sets up a Chrome WebDriver instance to interact with the Facebook website. 
2. **Define Campaign Parameters**: The script defines a list of advertising campaigns (`campaigns`) and a list of JSON files (`filenames`) containing group information.
3. **Initialize Facebook Promoter**: It creates an instance of the `FacebookPromoter` class, passing the WebDriver, group filenames, and a flag to disable video advertisements (`no_video`).
4. **Run Campaigns**: The script enters a loop that continuously runs the campaigns, defined by the `campaigns` list, using the specified group files. 
5. **Sleep**: After each campaign run, the script waits for 180 seconds (3 minutes) before restarting the loop. 
6. **Handle Keyboard Interrupt**: If the user interrupts the script (Ctrl+C), a message indicating the interruption is logged. 

Usage Example
-------------------------\

```python
    from src.webdriver.driver import Driver, Chrome
    from src.endpoints.advertisement.facebook import FacebookPromoter
    from src.logger.logger import logger

    d = Driver(Chrome)
    d.get_url(r"https://facebook.com")

    filenames = [
        "usa.json",
        "he_ils.json",
        "ru_ils.json",
        "katia_homepage.json",
        "my_managed_groups.json",
    ]

    campaigns = [
        'brands',
        'mom_and_baby',
        'pain',
        'sport_and_activity',
        'house',
        'bags_backpacks_suitcases',
        'man'
    ]

    promoter = FacebookPromoter(d, group_file_paths=filenames, no_video = True)

    try:
        while True:
            promoter.run_campaigns(campaigns=campaigns, group_file_paths=filenames)
            print(f"Going sleep {time.localtime}")
            time.sleep(180)

    except KeyboardInterrupt:
        logger.info("Campaign promotion interrupted.")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".