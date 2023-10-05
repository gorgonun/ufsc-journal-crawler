from journal_content_row import JournalContentRow
from journal_row import JournalRow


class RowConverter():

    @classmethod
    def to_dict(cls, row: JournalRow, content: JournalContentRow):
        return {
            "category": row.category,
            "link": row.link,
            "date": row.date.isoformat(),
            "title": row.title,
            "description": content.description,
            "general_details": content.general_details,
            "advertisement_details": content.advertisement_details
        }
