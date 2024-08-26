import re
import spacy
from typing import List, Dict

nlp = spacy.load("en_core_web_sm")


def recognize_entities(text: str) -> List[Dict]:
    """
    Identifies various types of entities in a given text using NER and regex for URLs.

    Args:
        text: The text to be processed.

    Returns:
        A list of dictionaries, where each dictionary represents an entity and contains the following keys:
        - type: The type of entity (e.g., "PERSON", "ORGANIZATION", "LOCATION", "PHONE", "EMAIL", "URL", "PRODUCT").
        - start: The starting index of the entity in the text.
        - end: The ending index of the entity in the text.
        - text: The original text of the entity.
    """
    doc = nlp(text)
    entities = []

    # NER-based entity recognition
    for ent in doc.ents:
        if ent.label_ not in ["MONEY"]:
            entity = {
                "type": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char,
                "text": ent.text,
            }
            entities.append(entity)

    url_pattern = re.compile(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )
    email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

    for pattern, entity_type in [
        # (policynumber_pattern, "POLICY"),
        # (ssn_pattern, "SSN"),
        (url_pattern, "URL"),
        (email_pattern, "EMAIL"),
        # (phone_pattern, "PHONE"),
    ]:
        for match in pattern.finditer(text):
            entity = {
                "type": entity_type,
                "start": match.start(),
                "end": match.end(),
                "text": match.group(),
            }
            entities.append(entity)

    # Sort entities by their starting position
    entities.sort(key=lambda x: x["start"])

    return entities


def anonymize(text: str, entities: List[Dict]) -> str:
    """
    Replaces identified entities with placeholders.

    Args:
        text: The text to be anonymized.
        entities: A list of dictionaries representing the entities to be anonymized.

    Returns:
        The anonymized text and the anonymization map.
    """

    anonymization_map = {}
    for entity in reversed(entities):  # Process entities from end to start
        placeholder = f"[ENTITY_{entity['type']}_{len(anonymization_map) + 1}]"
        anonymization_map[placeholder] = entity["text"]
        text = text[: entity["start"]] + placeholder + text[entity["end"] :]
    return text, anonymization_map


def deanonymize(text: str, anonymization_map: Dict) -> str:
    """
    Restores the original text by replacing placeholders with their corresponding original entities.

    Args:
        text: The anonymized text.
        anonymization_map: A dictionary that maps placeholders to their corresponding original entities.

    Returns:
        The de-anonymized text.
    """

    for placeholder, original_text in anonymization_map.items():
        text = text.replace(placeholder, original_text)
    return text


if __name__ == "__main__":
    text = """
# Mock Call Transcript: Customer Service Inquiry

Date: August 26, 2024
Time: 2:15 PM
Call Duration: 5 minutes 37 seconds

Agent: Thank you for calling ABC Insurance. This is Sarah speaking. How may I assist you today?

Customer: Hi Sarah, this is John Smith. I'm calling about my policy number INS-123456.

Agent: Hello Mr. Smith. I'd be happy to help you with that. Can you please verify your date of birth and the last four digits of your social security number?

Customer: Sure, my birthday is March 15, 1980, and the last four of my SSN are 7890.

Agent: Thank you for verifying that information, Mr. Smith. What can I help you with regarding your policy?

Customer: I recently moved to a new address, and I need to update it on my policy. My new address is 1234 Oak Street, Apartment 5B, Springfield, IL 62701.

Agent: I'd be happy to update that for you. Just to confirm, you're moving from 789 Elm Avenue, Chicago, IL 60601 to 1234 Oak Street, Apartment 5B, Springfield, IL 62701. Is that correct?

Customer: Yes, that's right.

Agent: Perfect. I've updated your address in our system. Is there a phone number where we can reach you at your new location?

Customer: Yes, my new home phone is (217) 555-1234, and my cell is still (312) 555-5678.

Agent: Thank you, I've added the new home phone number and confirmed your cell number. Is there anything else you need help with today?

Customer: Actually, yes. Can you tell me if my current policy covers flood damage? I'm a bit worried because my new place is near a river.

Agent: I'd be happy to check that for you, Mr. Smith. Let me take a look at your policy details. ... I see that your current policy, INS-123456, does not include flood coverage. However, we do offer flood insurance as an add-on. Would you like me to provide you with a quote for adding flood coverage?

Customer: Yes, please. That would be great.

Agent: Certainly. Based on your new address and current coverage, adding flood insurance would increase your monthly premium by $45. The total coverage for flood damage would be up to $250,000 for the structure and $100,000 for contents.

Customer: That sounds reasonable. Can you go ahead and add that to my policy?

Agent: Of course, Mr. Smith. I'll add the flood coverage to your policy effective today, August 26, 2024. You'll see the change reflected in your next monthly statement. The new total for your monthly premium will be $225.

Customer: Great, thank you for your help, Sarah.

Agent: You're welcome, Mr. Smith. Is there anything else I can assist you with today?

Customer: No, that's all. Thanks again.

Agent: Thank you for choosing ABC Insurance, Mr. Smith. Have a great day!

Customer: You too. Goodbye.

Agent: Goodbye.

[End of call]
"""

    # Recognize entities
    entities = recognize_entities(text)
    print("Recognized Entities:")
    for entity in entities:
        print(f"{entity['type']}: {entity['text']}")

    # Anonymize text
    anonymized_text, anonymization_map = anonymize(text, entities)
    print("\nAnonymized Text:")
    print(anonymized_text)

    # De-anonymize text
    de_anonymized_text = deanonymize(anonymized_text, anonymization_map)
    print("\nDe-anonymized Text:")
    print(de_anonymized_text)
