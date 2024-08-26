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
        (url_pattern, "URL"),
        (email_pattern, "EMAIL"),
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


def anonymize(text: str, entities: List[Dict]) -> tuple[str, Dict[str, str]]:
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


def deanonymize(text: str, anonymization_map: Dict[str, str]) -> str:
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
import argparse
import json
from .core import recognize_entities, anonymize, deanonymize


def create_parser():
    parser = argparse.ArgumentParser(description="Text Anonymizer")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Anonymize subcommand
    anonymize_parser = subparsers.add_parser("anonymize", help="Anonymize text")
    anonymize_parser.add_argument("input_file", help="Path to the input text file")
    anonymize_parser.add_argument("output_file", help="Path to the output text file")

    # De-anonymize subcommand
    deanonymize_parser = subparsers.add_parser("deanonymize", help="De-anonymize text")
    deanonymize_parser.add_argument("input_file", help="Path to the input text file")
    deanonymize_parser.add_argument("output_file", help="Path to the output text file")
    deanonymize_parser.add_argument("--map_file", required=True, help="Path to the anonymization map file")

    return parser

def anonymize_text(input_file, output_file):
    with open(input_file, "r") as f:
        text = f.read()

    entities = recognize_entities(text)
    anonymized_text, anonymization_map = anonymize(text, entities)
    
    with open(output_file, "w") as f:
        f.write(anonymized_text)
    
    map_file = f"{output_file}.json"
    with open(map_file, "w") as f:
        json.dump(anonymization_map, f, indent=2)
    
    return output_file, map_file

def deanonymize_text(input_file, output_file, map_file):
    with open(input_file, "r") as f:
        text = f.read()

    with open(map_file, "r") as f:
        anonymization_map = json.load(f)

    de_anonymized_text = deanonymize(text, anonymization_map)
    
    with open(output_file, "w") as f:
        f.write(de_anonymized_text)
    
    return output_file

def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "anonymize":
        output_file, map_file = anonymize_text(args.input_file, args.output_file)
        print(f"Anonymized text saved to {output_file}")
        print(f"Anonymization map saved to {map_file}")
    elif args.command == "deanonymize":
        output_file = deanonymize_text(args.input_file, args.output_file, args.map_file)
        print(f"De-anonymized text saved to {output_file}")

if __name__ == "__main__":
    main()
