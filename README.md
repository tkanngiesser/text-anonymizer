# Text Anonymizer

Text Anonymizer is a Python library that anonymizes text by replacing entities with placeholders and allows for de-anonymization. It uses the spaCy library for natural language processing and entity recognition.

## Features

- Text anonymization by replacing entities with placeholders
- De-anonymization to restore original text
- Entity recognition for various types (PERSON, ORGANIZATION, LOCATION, EMAIL, URL, etc.)
- Command-line interface for easy usage

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

### As a Python Library

Here's a simple example of how to use the Text Anonymizer in your Python code:

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

### Command-line Interface

Text Anonymizer also provides a command-line interface for easy usage:

```bash
# Anonymize a text file
text-anonymizer anonymize input.txt output.txt

# De-anonymize a text file
text-anonymizer deanonymize input.txt output.txt --map_file map.json
```

## Documentation

For detailed documentation, including API reference and advanced usage, please visit our [documentation page](https://text-anonymizer.readthedocs.io).

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

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.
