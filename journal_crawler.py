import os
import datetime
import time
from urllib.parse import urlparse
from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests
from journal_row import JournalRow


@dataclass
class JournalCheckpoint():
    offset: int


class JournalCrawler():
    def __init__(self, base_url: str, latest_checkpoint: JournalCheckpoint | None = None, count_by_page=15):
        self.base_url = base_url
        self.schema = urlparse(base_url).scheme
        self.hostname = urlparse(base_url).hostname
        self.latest_checkpoint = latest_checkpoint or JournalCheckpoint(0)
        self.count_by_page = count_by_page

    def generate_url(self, checkpoint: JournalCheckpoint):
        return f"{self.base_url}?offset={checkpoint.offset}"

    def get_data(self, checkpoint: JournalCheckpoint | None = None):
        current_checkpoint = checkpoint or self.latest_checkpoint
        print(f"Starting crawl from pages {current_checkpoint.offset}")

        return requests.get(self.generate_url(current_checkpoint), timeout=10)

    def parse_data(self, response: requests.Response):
        return BeautifulSoup(response.text, 'html.parser')

    def extract_rows_from_table(self, soup: BeautifulSoup):
        table = soup.find('table', class_='box').find_all('tr')
        count = 0

        for line in table:
            row = line.find_all('td')
            if row:
                try:
                    category = row[0]
                    link = row[1]
                    date = row[2]
                    count += 1

                    if category and link and date:
                        yield JournalRow(
                            category.text,
                            link.text,
                            (
                                f"{self.schema}://" +
                                os.path.join(self.hostname, link.find('a')['href'])
                            ),
                            datetime.datetime.strptime(date.text, "%d/%m/%Y").date()
                        )
                    else:
                        raise IndexError(f"Row {row} is not valid")

                except IndexError as e:
                    if count == self.count_by_page:
                        continue
                    else:
                        raise IndexError(f"Row {row} is not valid") from e

    def crawl_data(self, since: datetime.date | None = None, until: datetime.date | None = None, since_page: int | None = None, until_page: int | None = None, wait_time: int = 0):
        if since_page:
            self.latest_checkpoint = JournalCheckpoint(since_page * 15)

        while True:
            response = self.get_data(self.latest_checkpoint)
            soup = self.parse_data(response)

            for row in self.extract_rows_from_table(soup):
                if until and row.date > until:
                    continue
                if since and row.date < since:
                    return
                yield row

            self.latest_checkpoint = JournalCheckpoint(
                self.latest_checkpoint.offset + 15)
            if until_page and (self.latest_checkpoint.offset / 15) > until_page:
                break

            time.sleep(wait_time)
