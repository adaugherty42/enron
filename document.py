from dataclasses import dataclass


@dataclass
class Document:
    author: str
    term_frequencies: dict
    subject: str
    body: str
