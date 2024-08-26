import pytest
from text_anonymizer.core import recognize_entities, anonymize, deanonymize

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
