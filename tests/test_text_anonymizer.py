import pytest
import os
from unittest.mock import mock_open, patch
from text_anonymizer.core import recognize_entities, anonymize, deanonymize
from text_anonymizer.main import create_parser, anonymize_text, deanonymize_text
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

@pytest.fixture
def sample_text():
    return "John Smith from Acme Corporation located in New York City called me at john.smith@acme.com."

def test_recognize_entities(sample_text):
    entities = recognize_entities(sample_text)
    assert len(entities) >= 4
    assert any(e["type"] == "PERSON" and e["text"] == "John Smith" for e in entities)
    assert any(e["type"] == "ORG" and e["text"] == "Acme Corporation" for e in entities)
    assert any(e["type"] == "GPE" and e["text"] == "New York City" for e in entities)
    assert any(e["type"] == "EMAIL" and e["text"] == "john.smith@acme.com" for e in entities)

def test_anonymize(sample_text):
    anonymized_text, anonymization_map = anonymize(sample_text)
    
    assert "John Smith" not in anonymized_text
    assert "Acme Corporation" not in anonymized_text
    assert "New York City" not in anonymized_text
    assert "john.smith@acme.com" not in anonymized_text
    
    assert "[ENTITY_PERSON_1]" in anonymized_text
    assert "[ENTITY_ORG_1]" in anonymized_text
    assert "[ENTITY_GPE_1]" in anonymized_text
    assert "[ENTITY_EMAIL_1]" in anonymized_text
    
    assert len(anonymization_map) == 4
    assert anonymization_map["[ENTITY_PERSON_1]"] == "John Smith"
    assert anonymization_map["[ENTITY_ORG_1]"] == "Acme Corporation"
    assert anonymization_map["[ENTITY_GPE_1]"] == "New York City"
    assert anonymization_map["[ENTITY_EMAIL_1]"] == "john.smith@acme.com"

def test_deanonymize():
    anonymized_text = "[ENTITY_PERSON_1] works at [ENTITY_ORG_2] in [ENTITY_GPE_3]."
    anonymization_map = {
        "[ENTITY_PERSON_1]": "Jane Doe",
        "[ENTITY_ORG_2]": "Tech Corp",
        "[ENTITY_GPE_3]": "San Francisco"
    }
    
    de_anonymized_text = deanonymize(anonymized_text, anonymization_map)
    
    assert de_anonymized_text == "Jane Doe works at Tech Corp in San Francisco."

def test_full_process(sample_text):
    anonymized_text, anonymization_map = anonymize(sample_text)
    de_anonymized_text = deanonymize(anonymized_text, anonymization_map)
    
    assert de_anonymized_text == sample_text

def test_empty_text():
    empty_text = ""
    anonymized_text, anonymization_map = anonymize(empty_text)
    assert anonymized_text == ""
    assert len(anonymization_map) == 0
    
    de_anonymized_text = deanonymize(anonymized_text, anonymization_map)
    assert de_anonymized_text == ""

def test_text_without_entities():
    text = "This is a simple text without any named entities."
    anonymized_text, anonymization_map = anonymize(text)
    assert anonymized_text == text
    assert len(anonymization_map) == 0

def test_multiple_entities_of_same_type():
    text = "Alice and Bob work at Tech Corp and Acme Inc in New York and London."
    anonymized_text, anonymization_map = anonymize(text)
    
    assert "[ENTITY_PERSON_1]" in anonymized_text
    assert "[ENTITY_PERSON_2]" in anonymized_text
    assert "[ENTITY_ORG_1]" in anonymized_text
    assert "[ENTITY_ORG_2]" in anonymized_text
    assert "[ENTITY_GPE_1]" in anonymized_text
    assert "[ENTITY_GPE_2]" in anonymized_text
    
    assert len(anonymization_map) == 6
    
    # Check if the entities are correctly mapped
    assert any("Alice" in value for value in anonymization_map.values())
    assert any("Bob" in value for value in anonymization_map.values())
    assert any("Tech Corp" in value for value in anonymization_map.values())
    assert any("Acme Inc" in value for value in anonymization_map.values())
    assert any("New York" in value for value in anonymization_map.values())
    assert any("London" in value for value in anonymization_map.values())

def test_url_recognition():
    text = "Visit our website at https://www.example.com for more information."
    anonymized_text, anonymization_map = anonymize(text)
    
    assert "https://www.example.com" not in anonymized_text
    assert "[ENTITY_URL_1]" in anonymized_text
    assert anonymization_map["[ENTITY_URL_1]"] == "https://www.example.com"

def test_email_recognition():
    text = "Contact us at support@example.com for assistance."
    anonymized_text, anonymization_map = anonymize(text)
    
    assert "support@example.com" not in anonymized_text
    assert "[ENTITY_EMAIL_1]" in anonymized_text
    assert anonymization_map["[ENTITY_EMAIL_1]"] == "support@example.com"

def test_create_parser():
    parser = create_parser()
    assert parser.description == "Text Anonymizer"
    
    # Test anonymize subcommand
    anonymize_parser = parser._subparsers._group_actions[0].choices['anonymize']
    assert '--input_file' in anonymize_parser._option_string_actions
    assert '--output_file' in anonymize_parser._option_string_actions
    
    # Test deanonymize subcommand
    deanonymize_parser = parser._subparsers._group_actions[0].choices['deanonymize']
    assert '--input_file' in deanonymize_parser._option_string_actions
    assert '--output_file' in deanonymize_parser._option_string_actions
    assert '--map_file' in deanonymize_parser._option_string_actions

@patch('builtins.open', new_callable=mock_open, read_data="John Doe works at Acme Inc.")
@patch('json.dump')
def test_anonymize_text(mock_json_dump, mock_file):
    input_file = "input.txt"
    output_file = "output.txt"
    
    result_output, result_map = anonymize_text(input_file, output_file)
    
    assert result_output == output_file
    assert result_map == f"{output_file}.json"
    assert mock_file.call_count == 3  # Once for reading, twice for writing
    mock_json_dump.assert_called_once()

@patch('builtins.open', new_callable=mock_open, read_data="[ENTITY_PERSON_1] works at [ENTITY_ORG_1].")
@patch('json.load', return_value={"[ENTITY_PERSON_1]": "John Doe", "[ENTITY_ORG_1]": "Acme Inc"})
def test_deanonymize_text(mock_json_load, mock_file):
    input_file = "input.txt"
    output_file = "output.txt"
    map_file = "map.json"
    
    result = deanonymize_text(input_file, output_file, map_file)
    
    assert result == output_file
    assert mock_file.call_count == 3  # Once for reading input, once for reading map, once for writing output
    mock_json_load.assert_called_once()

@pytest.mark.skipif(not os.environ.get("ANTHROPIC_API_KEY"), reason="Anthropic API key not set")
def test_anonymization_effect_on_llm_response():
    anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    original_text = "John Doe from Acme Corp in New York is working on a new project. His email is john.doe@acme.com."
    anonymized_text, anonymization_map = anonymize(original_text)
    
    # Function to get LLM response
    def get_llm_response(text):
        prompt = f"{HUMAN_PROMPT} Please summarize the following text: {text}{AI_PROMPT}"
        response = anthropic.completions.create(
            model="claude-2",
            max_tokens_to_sample=300,
            prompt=prompt
        )
        return response.completion.strip()
    
    # Get responses for original and anonymized text
    original_response = get_llm_response(original_text)
    anonymized_response = get_llm_response(anonymized_text)
    
    # Deanonymize the anonymized response
    deanonymized_response = deanonymize(anonymized_response, anonymization_map)
    
    # Compare responses
    assert len(original_response) > 0
    assert len(deanonymized_response) > 0
    
    # Check if the deanonymized response contains key information from the original text
    assert "John Doe" in deanonymized_response
    assert "Acme Corp" in deanonymized_response
    assert "New York" in deanonymized_response
    
    # Compare the overall structure and length of the responses
    assert abs(len(original_response) - len(deanonymized_response)) < 50  # Allow for some variation
    
    # You might want to use more sophisticated comparison methods here,
    # such as semantic similarity measures, depending on your specific needs.
