import json
import logging
from pathlib import Path

import requests
from lxml import html

logging.basicConfig(format="%(message)s", level=logging.INFO)


def read_config():
    with open("config.json") as f:
        return json.load(f)


class Day:
    def __init__(self, num, *, test_results, input_results=None, get_test2_data=True):
        self.test_results = test_results
        self.input_results = input_results

        self.get_test2_data = get_test2_data

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
            self._test2_file.exists()
            or len(self.test_results) == 1
            or not self.get_test2_data
        ):
            return
        logging.info("Test file missing, scraping...")
        data = self._scrape_test_data()
        if len(data) == 0 or len(data) >= 3:  # noqa: PLR2004
            logging.warn("⚠ Warning, test data cannot be downloaded ⚠")
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
    def test_data(self):
        res = []
        with open(self._test1_file) as f:
            res.append(f.read())
        if self._test2_file.exists():
            with open(self._test2_file) as f:
                res.append(f.read())
        return res

    @property
    def test2_data(self):
        with open(self._test2_file) as f:
            return f.read()

    def validate_puzzle(self, i, fn, *, test_only=False):
        logging.info(f"\n🌞 Results for puzzle {i + 1} 🌞")
        res_test = fn(self.test_data[i])
        logging.info(f"🧪 Result on test data: {res_test}")
        if res_test == self.test_results[i]:
            logging.info("✅ Test data result is ok")
        else:
            logging.error("⛔ Test data result is wrong")
        if test_only:
            return
        res_input = fn(self.input_data)
        logging.info(f"🚀 Result on input data: {res_input}")
        if self.input_results is not None and len(self.input_results) > i:
            if res_input == self.input_results[i]:
                logging.info("✅ Input data result is ok")
            else:
                logging.error("⛔ Input data result is wrong")

    def validate(self, fn1, fn2=None, *, test_only=False):
        self.validate_puzzle(0, fn1, test_only=test_only)
        if fn2 is not None:
            self.validate_puzzle(1, fn2, test_only=test_only)
