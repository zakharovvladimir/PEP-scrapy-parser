import csv
from collections import Counter
from datetime import datetime as dt
from pathlib import Path

from scrapy.exceptions import DropItem

from .settings import DATETIME_FORMAT

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:

    def __init__(self):
        self.total = Counter()
        self.output_dir = Path(BASE_DIR, 'results')
        self.output_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if 'status' not in item:
            raise DropItem('Status not found')
        self.total[item['status']] += 1
        return item

    def close_spider(self, spider):
        filename = self.output_dir / (
            f'status_summary_{dt.now().strftime(DATETIME_FORMAT)}.csv'
        )
        with open(filename, mode='w', encoding='utf-8') as f:
            file = csv.writer(f, dialect='unix')
            file.writerow(['Статус', 'Количество'])
            for status, count in self.total.items():
                file.writerow([status, count])
            total = sum(self.total.values())
            file.writerow(['Total', total])
