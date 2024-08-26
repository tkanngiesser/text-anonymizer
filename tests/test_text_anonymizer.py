import pytest
from text_anonymizer.main import recognize_entities, anonymize, deanonymize

@pytest.fixture
def sample_text():
    return "John Smith from Acme Corporation located in New York City called me on 0123456789."

@pytest.fixture
def sample_entities():
    return [
        {"type": "PERSON", "start": 0, "end": 10, "text": "John Smith"},
        {"type": "ORG", "start": 16, "end": 31, "text": "Acme Corporation"},
        {"type": "GPE", "start": 43, "end": 56, "text": "New York City"},
    ]

def test_recognize_entities(sample_text):
    entities = recognize_entities(sample_text)
    assert len(entities) >= 3
    assert any(e["type"] == "PERSON" and e["text"] == "John Smith" for e in entities)
    assert any(e["type"] == "ORG" and e["text"] == "Acme Corporation" for e in entities)
    assert any(e["type"] == "GPE" and e["text"] == "New York City" for e in entities)

def test_anonymize(sample_text, sample_entities):
    anonymized_text, anonymization_map = anonymize(sample_text, sample_entities)
    
    assert "John Smith" not in anonymized_text
    assert "Acme Corporation" not in anonymized_text
    assert "New York City" not in anonymized_text
    
    assert "[ENTITY_PERSON_1]" in anonymized_text
    assert "[ENTITY_ORG_2]" in anonymized_text
    assert "[ENTITY_GPE_3]" in anonymized_text
    
    assert len(anonymization_map) == 3
    assert anonymization_map["[ENTITY_PERSON_1]"] == "John Smith"
    assert anonymization_map["[ENTITY_ORG_2]"] == "Acme Corporation"
    assert anonymization_map["[ENTITY_GPE_3]"] == "New York City"

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
    entities = recognize_entities(sample_text)
    anonymized_text, anonymization_map = anonymize(sample_text, entities)
    de_anonymized_text = deanonymize(anonymized_text, anonymization_map)
    
    assert de_anonymized_text == sample_text

def test_empty_text():
    empty_text = ""
    entities = recognize_entities(empty_text)
    assert len(entities) == 0
    
    anonymized_text, anonymization_map = anonymize(empty_text, entities)
    assert anonymized_text == ""
    assert len(anonymization_map) == 0
    
    de_anonymized_text = deanonymize(anonymized_text, anonymization_map)
    assert de_anonymized_text == ""

def test_text_without_entities():
    text = "This is a simple text without any named entities."
    entities = recognize_entities(text)
    assert len(entities) == 0
    
    anonymized_text, anonymization_map = anonymize(text, entities)
    assert anonymized_text == text
    assert len(anonymization_map) == 0
