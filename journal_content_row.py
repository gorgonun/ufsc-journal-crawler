from dataclasses import dataclass


@dataclass
class JournalContentRow:
    description: str
    general_details: dict[str, str]
    advertisement_details: dict[str, str]
