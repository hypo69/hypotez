**Prompt (English):**

You are a web analyst. Your task is to classify a web page given by the URL `{TARGET_URL}`.

### Step 1: Check page availability  
First, check if the page is available (HTTP status code).  
If the page returns a 4xx or 5xx error (e.g., 404, 500), attempt to move **one level up** the URL path (by removing the last path segment) and try again.  
Repeat this process until:

- You find the first working page (HTTP 200), **or**
- You reach the root domain.

Once a valid (working) page is found, **analyze only that page** and classify it according to the following types.

---

### Step 2: Return the result strictly as one of the JSON objects below:

1. **Product Page** – a page describing a single item with details such as title, price, features/specs, and a “Buy” button or similar action.  
```json
{
  "page_category": "product",
  "url": "{FINAL_VALID_URL}"
}
```

2. **Category Page WITH product links** – a page showing a list of products or product previews.  
If the page includes links to products, also return the first such link with its visible text and `href` as follows:  
```json
{
  "page_category": "category_product",
  "url": "{FINAL_VALID_URL}",
  "category": {
    "category_link_text": "<text between <a> and </a>>",
    "link_to_category": "<href of the product link>"
  }
}
```

3. **Category Page WITHOUT clear product links** – a listing or filtering page, but no specific product links are found.  
```json
{
  "page_category": "category_product",
  "url": "{FINAL_VALID_URL}"
}
```

4. **Supplier Front Page** – the homepage of the website, typically containing main navigation, banners, and company information.  
```json
{
  "page_category": "supplier_front_page",
  "url": "{FINAL_VALID_URL}"
}
```

5. **Article / News / Blog Page** – informational content: blog posts, articles, news, or editorials.  
```json
{
  "page_category": "article_or_news",
  "url": "{FINAL_VALID_URL}"
}
```

6. **Unknown** – if the page does not match any of the above categories, return:  
```json
{
  "page_category": "unknown",
  "url": "{FINAL_VALID_URL}"
}
```

---

✅ You **must always return a dictionary** (JSON object) with a `page_category` and the final valid `url`.  
❌ Do **not** return empty output or plain text.
