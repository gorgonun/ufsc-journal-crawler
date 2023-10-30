import requests
from bs4 import BeautifulSoup
from journal_content_row import JournalContentRow


class JournalContentCrawler():
    def get_data(self, url: str):
        return requests.get(url, timeout=10)

    def parse_data(self, response: requests.Response):
        return BeautifulSoup(response.text, 'html.parser')

    def extract_content(self, soup: BeautifulSoup) -> JournalContentRow:
        table = soup.find('table', class_='box').find_all('tr')

        for i, line in enumerate(table):
            if i != 4:
                continue
            row = line.find_all('td')
            if row:
                try:
                    description = row[2].get_text()
                    general_details = {}
                    advertisement_details = {}
                    cursor = 3

                    if row[cursor].get_text(strip=True) == "Detalhes Gerais:":
                        for i in range(cursor + 1, len(row), 2):
                            general_details[row[i].get_text(
                            )] = row[i + 1].get_text(strip=True)
                            if row[i + 2].get_text(strip=True) == "Detalhes do anúncio":
                                cursor = i + 2
                                break

                    if row[cursor].get_text(strip=True) == "Detalhes do anúncio":
                        cursor_fix = 0

                        for i in range(cursor + 1, len(row), 2):
                            if row[i + cursor_fix].get_text(strip=True) == "Indique a existência ou necessidade do item e apresente caracterísicas dele.":
                                cursor_fix += 1
                                continue
                            advertisement_details[row[i + cursor_fix].get_text(
                                strip=True)] = row[i + 1 + cursor_fix].get_text(strip=True)
                            if row[i + cursor_fix].get_text(strip=True).startswith('Adicionado'):
                                break

                    return JournalContentRow(description, general_details, advertisement_details)
                except IndexError as e:
                    raise IndexError(f"Row {row} is not valid") from e

    def crawl_data(self, url: str):
        response = self.get_data(url)
        soup = self.parse_data(response)
        return self.extract_content(soup)
