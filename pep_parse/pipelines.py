import csv
import datetime as dt
from collections import defaultdict
from pep_parse.settings import (BASE_DIR, DATETIME_FORMAT, FILE_FORMAT,
                                RESULTS, SUMMARY_NAME, SUMMARY_TABLE_HEADER)


class PepParsePipeline:

    def __init__(self):
        self.results_dir = None

    def open_spider(self, spider):
        self.statuses = defaultdict(int)
        self.results_dir = BASE_DIR / RESULTS
        self.results_dir.mkdir(exist_ok=True)

    def close_spider(self, spider):
        if self.results_dir is not None:
            now = dt.datetime.now()
            now_formatted = now.strftime(DATETIME_FORMAT)
            file_name = f'{SUMMARY_NAME}_{now_formatted}.{FILE_FORMAT}'
            file_path = self.results_dir / file_name
            with open(file_path, mode='w', encoding='utf-8') as csvfile:
                csv.writer(
                    csvfile,
                    dialect=csv.unix_dialect,
                    quoting=csv.QUOTE_NONE,
                ).writerows([
                    SUMMARY_TABLE_HEADER,
                    *self.statuses.items(),
                    ('Total', sum(self.statuses.values())),
                ])

    def process_item(self, item, spider):
        self.statuses[item.get('status')] += 1
        return item
