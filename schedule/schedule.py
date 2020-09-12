from datetime import datetime
import json


class Schedule:
    def __init__(self, date: datetime, lesson_timing: str = None):
        self.date = date
        self.lesson_timing = lesson_timing
        self.timeslots = []
        self.lessons: dict[str, list] = {}

    @property
    def date(self) -> datetime:
        return self._date

    @date.setter
    def date(self, date: datetime) -> None:
        self._date = date

    @property
    def lesson_timing(self) -> str:
        return self._lesson_timing

    @lesson_timing.setter
    def lesson_timing(self, timing: str) -> None:
        self._lesson_timing = timing

    def add_grade(self, grade: str, lessons: list[str] = None) -> None:
        """
        Add the grade to the schedule. If the second parameter is passed, fills the lessons for the given grade.
        :param grade: The grade to add
        :param lessons: (optional) The lessons for the grade
        :return: None
        :raises Exception: if the grade is already in te schedule
        """
        if grade in self.lessons:
            raise Exception(f"Grade {grade} has been already added!")
        if lessons is None:
            self.lessons[grade] = []
        else:
            self.lessons[grade] = lessons

    def add_timeslot(self, start: str, end: str) -> None:
        """
        Add the timeslot to the schedule (lesson start/end).
        :param start: The starting time of the lesson
        :param end: The end of the lesson
        :return: None
        """
        self.timeslots.append((start.replace(".", ":"), end.replace(".", ":")))

    def add_lesson(self, grade: str, lesson: str) -> None:
        """
        Add the lesson to the schedule for the given grade. If the grade is not in the schedule yet, adds it.
        :param grade: The grade to add the lesson to
        :param lesson: The lesson to add
        :return: None
        """
        if grade not in self.lessons:
            self.add_grade(grade)
        self.lessons[grade].append(lesson)

    def add_by_index(self, grade_index: int, lesson: str) -> None:
        """
        Add the lesson to the schedule for the given grade by its index. Useful while parsing the schedule table.
        :param grade_index: int: The index of the grade to add the lesson to
        :param lesson: The lesson to add
        :return: None
        """
        self.lessons[list(self.lessons.keys())[grade_index]].append(lesson)

    def filter(self, grade: str):
        """
        Create a new Schedule object with only grades that match the given filter.
        :param grade: The grade to filter by. e.g. "11a" matches only "11a", while "10" would match "10a" and "10b"
        :return: Schedule
        """
        filtered = Schedule(self.date, self.lesson_timing)
        for key in self.lessons:
            if key == grade or key.rstrip("абв") == grade:
                filtered.add_grade(key, self.lessons[key])
        return filtered

    def trim_empty(self) -> None:
        """
        Remove all the "empty" lessons at the end for each grade
        :return: None
        """
        for grade_key in self.lessons.keys():
            while self.lessons[grade_key][-1] == "":
                self.lessons[grade_key].pop()

    def __str__(self) -> str:
        return json.dumps({
            "date": f'{self.date.strftime("%d.%m.%Y")} ({round(self.date.timestamp())})',
            "timing": self.lesson_timing,
            "timeslots": self.timeslots,
            "lessons": self.lessons
        }, indent="  ", ensure_ascii=False)

    def to_file(self, filename: str) -> None:
        """
        Save the schedule object to a json file
        :param filename: The file to write the schedule to
        :return: None
        """
        with open(filename, "w") as file:
            json.dump({
                "date": self.date.strftime("%d.%m.%Y"),
                "timing": self.lesson_timing,
                "timeslots": self.timeslots,
                "lessons": self.lessons
            }, file, ensure_ascii=False)

    @classmethod
    def from_file(cls, filename: str):
        """
        Restore the schedule object from the json file
        :param filename: The file to read the data from
        :return: Schedule
        """
        with open(filename, "r") as file:
            schedule: dict = json.load(file)
        schedule_obj = cls(datetime.strptime(schedule["date"], "%d.%m.%Y"), schedule["timing"])
        for grade in schedule["lessons"]:
            schedule_obj.add_grade(grade, schedule["lessons"][grade])
        for timeslot in schedule["timeslots"]:
            schedule_obj.add_timeslot(timeslot[0], timeslot[1])
        return schedule_obj
