# Module for working with AliExpress API languages
=================================================================================

The module contains the `Language` class, which defines a set of language codes used in AliExpress API requests. This class provides a convenient way to access and use these language codes within the project.

## Details

The `Language` class defines a set of constants representing the supported language codes for AliExpress API. This approach ensures consistency and maintainability when working with language-related operations.

## Classes

### `class Language`

**Description**: This class defines a set of constants representing language codes for AliExpress API.

**Attributes**:

- `EN` (str): Represents the English language code.
- `RU` (str): Represents the Russian language code.
- `PT` (str): Represents the Portuguese language code.
- `ES` (str): Represents the Spanish language code.
- `FR` (str): Represents the French language code.
- `ID` (str): Represents the Indonesian language code.
- `IT` (str): Represents the Italian language code.
- `TH` (str): Represents the Thai language code.
- `JA` (str): Represents the Japanese language code.
- `AR` (str): Represents the Arabic language code.
- `VI` (str): Represents the Vietnamese language code.
- `TR` (str): Represents the Turkish language code.
- `DE` (str): Represents the German language code.
- `HE` (str): Represents the Hebrew language code.
- `KO` (str): Represents the Korean language code.
- `NL` (str): Represents the Dutch language code.
- `PL` (str): Represents the Polish language code.
- `MX` (str): Represents the Mexican language code.
- `CL` (str): Represents the Chilean language code.
- `IW` (str): Represents the Hebrew language code (alternative spelling).
- `IN` (str): Represents the Indian language code.


## Examples

```python
from src.suppliers.aliexpress.api.models.languages import Language

# Accessing language codes:
print(Language.EN)  # Output: 'EN'
print(Language.RU)  # Output: 'RU'
print(Language.DE)  # Output: 'DE'
```