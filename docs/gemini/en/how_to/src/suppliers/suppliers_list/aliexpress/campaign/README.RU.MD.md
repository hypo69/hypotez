**How to Use the `campaign` Module**
=========================================================================================

**Description**
-------------------------
The `campaign` module is designed to manage the process of creating and publishing Facebook advertising campaigns. It provides functionalities for initializing campaign parameters (name, language, currency), creating directory structures, saving configurations for a new campaign, collecting and saving product data through `ali` or `html`, generating advertising materials, validating the campaign, and publishing it on Facebook.

**Execution Steps**
-------------------------
1. **Initialize campaign parameters:** Set the name, language, and currency for the campaign.
2. **Create directories:** Establish folders for the campaign and its categories.
3. **Save campaign configuration:** Store the campaign settings for future reference.
4. **Collect product data:** Gather information about the products to be advertised using either the `ali` or `html` methods.
5. **Save product data:** Store the collected product information for use in campaign materials.
6. **Generate advertising materials:** Create assets such as images, text, and videos for the campaign.
7. **Validate the campaign:** Check the campaign for errors and ensure it's ready for publication.
8. **Publish the campaign on Facebook:** Submit the campaign to Facebook for advertising.

**Usage Example**
-------------------------

```python
# Initialize campaign parameters
campaign_name = "Summer Sale"
language = "en"
currency = "USD"

# Create directories
campaign_dir = create_campaign_directory(campaign_name)
category_dirs = create_category_directories(campaign_dir)

# Save campaign configuration
save_campaign_config(campaign_name, language, currency)

# Collect and save product data
products = collect_products_from_ali("summer_clothes")
save_products_data(products)

# Generate advertising materials
generate_campaign_assets(campaign_dir)

# Validate the campaign
validate_campaign(campaign_dir)

# Publish the campaign
publish_campaign_to_facebook(campaign_name)
```