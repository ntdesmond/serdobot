import re
from datetime import datetime
from schedule.schedule import Schedule


class Parser:
    def strip_tags(self, html_piece: str) -> str:
        """
            Remove all HTML tags and replace &nbsp; entities to unicode ones. Strip all the spaces then.
            :param html_piece: the string to be edited
            :return: the new stripped string without tags and with unicode nbsp entities
        """
        tag_pattern = re.compile(r"<.+?>\s*", re.S)
        return tag_pattern.sub("", html_piece).replace("&nbsp;", "\xa0").strip()

    # consider creating Schedule class
    def parse(self, html: str) -> Schedule:
        row_pattern = re.compile(r"<tr.*?>\s*(?P<cells><td.*?>.+?</td>)\s*</tr>", re.S)
        cell_pattern = re.compile(r"<td.*?>\s*(?P<content>.*?)\s*</td>", re.S)
        time_pattern = re.compile(r"(?P<start>\d{1,2}[:.]\d{2}).(?P<end>\d{1,2}[:.]\d{2})")
        rows: iter = row_pattern.finditer(html)
        # day_info (first table cell): weekday; date; timing_type (split by \xa0)
        day_info: list[str] = self.strip_tags(cell_pattern.search(next(rows).group("cells")).group()).split('\xa0')
        schedule = Schedule(datetime.strptime(day_info[1], "%d.%m.%Y"), '\xa0'.join(day_info[2:]))
        grades_added: bool = False

        for row in rows:
            cells = cell_pattern.findall(row.group("cells"))

            # first column contains only lesson numbers - no need to go through it
            # second (i=1) contains lesson timeslots, need a special treatment for it
            for i in range(1, len(cells)):
                cell_text = self.strip_tags(cells[i])
                if grades_added:
                    if i == 1:
                        timeslot = time_pattern.search(cell_text).groupdict()
                        schedule.add_timeslot(timeslot["start"], timeslot["end"])
                    else:
                        schedule.add_by_index(i - 2, cell_text)
                else:
                    if i != 1:
                        # adding the grades using the first (second) table row
                        schedule.add_grade(cell_text)

            grades_added = True

        schedule.trim_empty()
        return schedule
