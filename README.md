# Text Anonymizer

Text Anonymizer is a Python library that anonymizes text by replacing entities with placeholders and allows for de-anonymization. It uses the spaCy library for natural language processing and entity recognition.

## Features

- Text anonymization by replacing entities with placeholders
- De-anonymization to restore original text
- Entity recognition for various types (PERSON, ORGANIZATION, LOCATION, EMAIL, URL, etc.)

## Installation

You can install the Text Anonymizer library using pip:

```bash
pip install text-anonymizer
```

This will also install the required dependencies, including spaCy.

After installation, you need to download the spaCy English language model:

```bash
python -m spacy download en_core_web_sm
```

## Usage

Here's a simple example of how to use the Text Anonymizer:

```python
from text_anonymizer import anonymize, deanonymize

# Original text
text = "John Smith from Acme Corporation called me at john.smith@acme.com."

# Anonymize the text
anonymized_text, anonymization_map = anonymize(text)

print("Anonymized text:", anonymized_text)
# Output: [ENTITY_PERSON_1] from [ENTITY_ORG_1] called me at [ENTITY_EMAIL_1].

# De-anonymize the text
original_text = deanonymize(anonymized_text, anonymization_map)

print("Original text:", original_text)
# Output: John Smith from Acme Corporation called me at john.smith@acme.com.
```

## API Reference

### `anonymize(text: str) -> Tuple[str, Dict[str, str]]`

Anonymizes the given text by replacing identified entities with placeholders.

- `text`: The text to be anonymized.
- Returns: A tuple containing the anonymized text and the anonymization map.

### `deanonymize(anonymized_text: str, anonymization_map: Dict[str, str]) -> str`

Restores the original text by replacing placeholders with their corresponding original entities.

- `anonymized_text`: The anonymized text.
- `anonymization_map`: A dictionary that maps placeholders to their corresponding original entities.
- Returns: The de-anonymized text.

## Development

To set up the development environment:

1. Clone the repository:
   ```bash
   git clone https://github.com/viktorbezdek/text-anonymizer.git
   cd text-anonymizer
   ```

2. Install Poetry (if not already installed):
   ```bash
   pip install poetry
   ```

3. Install dependencies:
   ```bash
   poetry install
   ```

4. Activate the virtual environment:
   ```bash
   poetry shell
   ```

5. Run tests:
   ```bash
   pytest
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
