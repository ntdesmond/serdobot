from os.path import splitext, split as splitpath
from bs4 import BeautifulSoup
from core.urls import URL
import pandas as pd
import requests
import json


def shorten_name(name: str):
    parts = name.split()
    if len(parts) > 1:
        return ' '.join([parts[0]] + [f"{name_part[0]}." for name_part in parts[1:]])
    else:
        return name


class Schedule:
    def __init__(self, grade: str, tables: dict[str, pd.DataFrame]):
        self._grade = grade
        self._tables = tables

    @property
    def grade(self) -> str:
        return self._grade

    @property
    def tables(self) -> dict[str, pd.DataFrame]:
        return self._tables

    def __str__(self) -> str:
        return f"Schedule for {self.grade}: " + \
               ", ".join([
                   f"{day} ({self.tables[day].shape[0]} lesson{'s' if self.tables[day].shape[0] > 1 else ''})"
                   for day in self.tables
               ])

    def save(self, folder: str) -> None:
        """
        Save the schedule object to a json file
        :return: None
        """
        tables_dict = dict()
        for name, table in self.tables.items():
            table = table.sort_values(table.columns[0]).to_dict(orient='split')
            del table['index']
            tables_dict[name] = table
        with open(f"{folder}/{self.grade}.json", "w", encoding="utf8") as file:
            json.dump(tables_dict, file, ensure_ascii=False)

    @classmethod
    def load(cls, filename: str):
        """
        Restore the schedule object from the json file
        :param filename: The file to read the data from
        :return: Schedule
        """
        with open(filename, "rb") as file:
            tables_dict: dict[str, dict] = json.load(file)
        grade: str = splitext(splitpath(filename)[1])[0]
        tables = dict()
        for name, table in tables_dict.items():
            tables[name] = pd.DataFrame.from_records(table['data'], columns=table['columns'])
        return cls(grade, tables)

    @classmethod
    def download(cls, grade: str, href: URL):
        """
        Download the schedule from the website and parse it
        :param grade: The grade to download schedule for
        :param href: The link to the schedule
        :return: Schedule
        """
        html = requests.get(str(href)).text
        tables: dict[str, pd.DataFrame] = dict()
        soup = BeautifulSoup(html, 'html5lib')
        contents = soup.select(".news-list > h2, .news-list > h2 + div table")
        while len(contents) > 0:
            table = pd.read_html(contents[1].decode(), flavor='html5lib', keep_default_na=False)[0]
            table['Учитель'] = table['Учитель'].map(shorten_name)
            tables[contents[0].text] = table
            contents = contents[2:]
        return cls(grade, tables)
