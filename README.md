# Text Anonymizer

Text Anonymizer is a Python library that anonymizes text by replacing entities with placeholders and allows for de-anonymization. It uses the spaCy library for natural language processing and entity recognition. The intended usage is for anonymizing text data before sending it to a language model (LLM) for processing, and then de-anonymizing the output to restore the original text. This can be useful in various scenarios, such as when working with sensitive data or when you want to maintain the privacy of individuals mentioned in the text. 

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

## Todo

- [ ] Add tests for if anonymization affects LLM (such as OpenAI) response quality
- [ ] Add tests for if anonymization affects Reranking (such as Cohere) quality
- [ ] Change replacements to be realistic instead of placeholders (could possibly affect AI apps)
- [ ] Improve preservation of specific details (numbers, dates, times) while maintaining anonymity
- [ ] Enhance consistency in anonymizing company names and other entities
- [ ] Develop a method to retain more information in anonymized summaries
- [ ] Implement a configurable level of anonymization to balance privacy and information preservation

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

## Evaluation Report

We conducted an evaluation of the Text Anonymizer to assess its impact on text content and information retrieval. Here are the key findings:

### Summary Comparison

1. **Original Summary Length**: 519 characters
2. **Anonymized Summary Length**: 267 characters
3. **Summary Length Difference**: 252 characters

The anonymized summary is significantly shorter, which suggests that some specific details are omitted in the anonymization process.

### Information Retrieval

We asked several questions about the original, anonymized, and deanonymized texts. Here are the key observations:

1. **Sender and Recipient Identification**: 
   - The anonymized text correctly preserved the sender's company (TechInnovate Solutions) but replaced names with placeholders.
   - The recipient's name was anonymized, but their company name was not consistently preserved.

2. **Main Purpose of the Email**: 
   - The main purpose (proposing an AI-driven supply chain optimization system) was preserved in both anonymized and deanonymized versions.

3. **Key Benefits of the AI System**:
   - All four key benefits were preserved in both anonymized and deanonymized versions.
   - Specific numbers (e.g., 95% accuracy) were replaced with placeholders in the anonymized version.

4. **Meeting Details**:
   - The proposed meeting time was anonymized, replacing "next Tuesday at 2 PM EST" with placeholders.

