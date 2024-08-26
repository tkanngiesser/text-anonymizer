"""Text Anonymizer: A library for anonymizing and de-anonymizing text."""

__version__ = "0.1.0"

from .anonymizer import anonymize, deanonymize

__all__ = ["anonymize", "deanonymize"]
