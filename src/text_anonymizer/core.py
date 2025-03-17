import re
from typing import List, Dict, Optional
import spacy
from spacy.matcher import PhraseMatcher
from typing import List, Dict, Tuple

nlp = spacy.load("en_core_web_sm")


def recognize_entities(
    text: str, company_terms: Optional[List[str]] = None, company_name=None
) -> List[Dict]:
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ not in ["MONEY"]:
            entities.append(
                {
                    "type": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "text": ent.text,
                }
            )
    url_pattern = re.compile(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )
    email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    for pattern, entity_type in [(url_pattern, "URL"), (email_pattern, "EMAIL")]:
        for match in pattern.finditer(text):
            entities.append(
                {
                    "type": entity_type,
                    "start": match.start(),
                    "end": match.end(),
                    "text": match.group(),
                }
            )
    if company_terms:
        matcher = PhraseMatcher(nlp.vocab)
        patterns = [nlp.make_doc(term) for term in company_terms]
        matcher.add(company_name, None, *patterns)
        for match_id, start, end in matcher(doc):
            span = doc[start:end]
            entities.append(
                {
                    "type": "COMPANY",
                    "start": span.start_char,
                    "end": span.end_char,
                    "text": span.text,
                }
            )
    entities.sort(key=lambda x: x["start"])
    return entities


def anonymize(
    text: str, company_terms: Optional[List[str]] = None, company_name=None
) -> Tuple[str, Dict[str, str]]:
    """
    Anonymizes the given text by replacing identified entities with placeholders.

    Args:
        text: The text to be anonymized.

    Returns:
        A tuple containing the anonymized text and the anonymization map.
    """
    entities = recognize_entities(
        text=text, company_terms=company_terms, company_name=company_name
    )
    anonymization_map = {}
    entity_counters = {}
    for entity in reversed(entities):  # Process entities from end to start
        entity_type = entity["type"]
        if entity_type not in entity_counters:
            entity_counters[entity_type] = 1
        else:
            entity_counters[entity_type] += 1
        placeholder = f"[ENTITY_{entity_type}_{entity_counters[entity_type]}]"
        anonymization_map[placeholder] = entity["text"]
        text = text[: entity["start"]] + placeholder + text[entity["end"] :]
    return text, anonymization_map


def deanonymize(anonymized_text: str, anonymization_map: Dict[str, str]) -> str:
    """
    Restores the original text by replacing placeholders with their corresponding original entities.

    Args:
        anonymized_text: The anonymized text.
        anonymization_map: A dictionary that maps placeholders to their corresponding original entities.

    Returns:
        The de-anonymized text.
    """
    for placeholder, original_text in anonymization_map.items():
        anonymized_text = anonymized_text.replace(placeholder, original_text)
    return anonymized_text
