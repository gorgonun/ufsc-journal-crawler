from dataclasses import dataclass
import datetime


@dataclass
class JournalRow:
    category: str
    title: str
    link: str
    date: datetime.date
