# Text Anonymizer

Text Anonymizer is a Python tool that recognizes entities in text, anonymizes them, and allows for de-anonymization. It uses the spaCy library for natural language processing and entity recognition.

## Features

- Entity recognition for various types (PERSON, ORGANIZATION, LOCATION, etc.)
- Text anonymization by replacing entities with placeholders
- De-anonymization to restore original text

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/viktorbezdek/text-anonymizer.git
   cd text-anonymizer
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Download the spaCy English language model:
   ```
   python -m spacy download en_core_web_lg
   ```

## Usage

The main functionality is provided in the `main.py` file. You can use the following functions:

- `recognize_entities(text: str) -> List[Dict]`: Identifies entities in the given text.
- `anonymize(text: str, entities: List[Dict]) -> Tuple[str, Dict]`: Replaces identified entities with placeholders.
- `deanonymize(text: str, anonymization_map: Dict) -> str`: Restores the original text by replacing placeholders.

Example usage:

```python
from text_anonymizer.main import recognize_entities, anonymize, deanonymize

text = "John Smith from Acme Corporation called me."

# Recognize entities
entities = recognize_entities(text)

# Anonymize text
anonymized_text, anonymization_map = anonymize(text, entities)

# De-anonymize text
de_anonymized_text = deanonymize(anonymized_text, anonymization_map)
```

## Running the Example

To run the example provided in the `main.py` file:

```
python src/text_anonymizer/main.py
```

This will demonstrate entity recognition, anonymization, and de-anonymization on a sample text.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.