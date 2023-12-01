import json
import logging
from pathlib import Path

import requests
from lxml import html

logging.basicConfig(level=logging.INFO)


def read_config():
    with open("config.json") as f:
        return json.load(f)


class Day:
    def __init__(self, num, result1=None, result2=None, test2_data=True):
        self.test1 = result1
        self.test2 = result2
        self._num = num
        self._num_str = str(num).zfill(2)
        self._input_file = Path("days/inputs") / f"{self._num_str}_input.txt"
        self._test1_file = Path("days/inputs") / f"{self._num_str}_test_1.txt"
        self._test2_file = Path("days/inputs") / f"{self._num_str}_test_2.txt"
        self._config = read_config()
        self._get_input_file()
        self._get_test_files()

    def _get_input_file(self):
        """
        Download input file if not already present.
        """
        if self._input_file.exists():
            return
        logging.info("Input file not found, downloading...")
        url = f"https://adventofcode.com/2023/day/{self._num}/input"
        r = requests.get(url, timeout=10, cookies={"session": self._config["session"]})
        with open(self._input_file, "w") as f:
            f.write(r.text)

    def _scrape_test_data(self) -> list:
        url = f"https://adventofcode.com/2023/day/{self._num}"
        page = requests.get(url, timeout=10, cookies={"session": self._config["session"]})
        tree = html.fromstring(page.content)
        data = tree.xpath('//article[@class="day-desc"]//pre/code/text()')
        return data

    def _get_test_files(self):
        """
        Scrap test data to test file if not already present.
        """
        if self._test1_file.exists() and (
            self._test2_file.exists() or self.test2 is None or not self.test2_data
        ):
            return
        logging.info("Test file 1 not found, scraping...")
        data = self._scrape_test_data()
        if len(data) == 0 or len(data) >= 3:  # noqa: PLR2004
            logging.warn("Warning, test data cannot be downloaded")
        else:
            for i, text in enumerate(data):
                logging.info(f"Scraped data for test{i+1}:\n{text}")
                with open(getattr(self, f"_test{i+1}_file"), "w") as f:
                    f.write(text)

    @property
    def input_data(self):
        with open(self._input_file) as f:
            return f.read()

    @property
    def test1_data(self):
        with open(self._test1_file) as f:
            return f.read()

    @property
    def test2_data(self):
        with open(self._test2_file) as f:
            return f.read()

    def validate1(self, fn):
        res_test = fn(self.test1_data)
        logging.info("--- Results for first puzzle ---")
        logging.info(f"Result on test data: {res_test}")
        if res_test == self.test1:
            logging.info("✅ Test data result is ok")
        else:
            logging.error("⛔ Test data result is wrong")
        res_input = fn(self.input_data)
        logging.info(f"Result on input data: {res_input}")

    def validate2(self, fn):
        res_test = fn(self.test2_data)
        logging.info("--- Results for second puzzle ---")
        logging.info(f"Result on test data: {res_test}")
        if res_test == self.test2:
            logging.info("✅ Test data result is ok")
        else:
            logging.error("⛔ Test data result is wrong")
        res_input = fn(self.input_data)
        logging.info(f"Result on input data: {res_input}")
