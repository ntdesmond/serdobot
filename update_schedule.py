from schedule.Schedule import Schedule
from core.urls import URL
from core import config
from bs4 import BeautifulSoup
import requests
import json


def get_grades(url: URL) -> dict[str, str]:
    """
    Get a dictionary containing available classes and URLs to their schedule
    :return: dict with grades and URLs
    """
    grades: dict[str, str] = dict()
    html = requests.get(str(url)).text
    soup = BeautifulSoup(html, 'html5lib')
    for a in soup.select(".sf-main-area .sf-iblock-card-area a"):
        grade = a.text.lower().removeprefix('класс ')
        grades[grade] = a['href']
    return grades


if __name__ == '__main__':
    folder = config['Folders']['saved_schedule']
    grades = get_grades(URL(config['Website']['schedule_grades_path']))
    with open(f"{folder}/grades.json", "w", encoding="utf8") as file:
        json.dump(grades, file, ensure_ascii=False)
    for grade, href in grades.items():
        schedule: Schedule = Schedule.download(grade, URL(href))
        print(schedule)
        schedule.save(folder)
