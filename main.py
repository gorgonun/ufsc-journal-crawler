import datetime
import json
import random
import sys
import time
from journal_content_crawler import JournalContentCrawler
from journal_crawler import JournalCrawler
from row_converter import RowConverter


def main():
    if len(sys.argv) < 2:
        raise ValueError("Usage: python main.py <url> [<since>, <until>]")

    url = sys.argv[1]

    crawler = JournalCrawler(url)
    content_crawler = JournalContentCrawler()
    since = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d").date() if len(sys.argv) >= 3 else datetime.date.today()
    until = datetime.datetime.strptime(sys.argv[3], "%Y-%m-%d").date() if len(sys.argv) >= 4 else datetime.date.today()

    print(f"Starting crawl from {url} until {until}")

    data = crawler.crawl_data(since=since, until=until, wait_time=random.randint(1, 60))

    for line in data:
        content = content_crawler.crawl_data(line.link)

        with open(f"data/{line.date.isoformat()}.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(RowConverter.to_dict(line, content), ensure_ascii=False) + "\n")

        time.sleep(random.randint(1, 5))


if __name__ == '__main__':
    main()
