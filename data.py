from datetime import datetime as dt

import pandas as pd
from googleapiclient.discovery import build

from authenticate import Authenticate
from schedule import Schedule


class Data(Schedule):
    """Creates a data object after reading information from the grade books."""

    ss_range = 'Summary!B3:V40'  # Spreadsheet range

    data_headers = ['First', 'Last', 'Course', 'Student Email', 'Advisor Email',
                    'Grade', 'Period', 'ISP', 'Current 1', 'Current 2', 'Interim 1',
                    'Quarter 1', 'Interim 2', 'Exam 1', 'Semester 1', 'Interim 3',
                    'Quarter 3', 'Interim 4', 'Exam 2', 'Semester 2', 'Final']

    report_headers = ['Time Stamp', 'First', 'Last', 'Course', 'Semester', 'Letter',
                      'Current 1', 'Current 2',
                      'Interim 1', 'Quarter 1', 'Interim 2', 'Exam 1', 'Semester 1',
                      'Interim 3', 'Quarter 3', 'Interim 4', 'Exam 2', 'Semester 2',
                      'Final']

    def __init__(self, df=None):
        self.credentials = Authenticate.get_credentials()
        self.date = dt.today()
        self.semester = self.get_semester()
        self.academic_year = self.get_academic_year()
        if df is None:
            self.periods = self.get_periods()
            self.student_data = self.get_data()
        else:
            self.student_data = df  # Pandas DataFrame

    def get_semester(self):
            """Returns current semester."""
            s2_start = dt(2020, 1, 22)  # Semester 2 start date.
            if self.date >= s2_start:
                return 2
            return 1

    def get_academic_year(self):
            """Returns academic year as a string: 2019_2020"""
            if self.semester == 1:
                return str(self.date.year) + '_' + str(self.date.year + 1)
            return str(self.date.year - 1) + '_' + str(self.date.year)
    
    def get_periods(self):
        """Prompts user for periods for which to seek gradebook info."""
        user_input = input('Enter Period(s) or \'all\':')
        active_periods = list(self.schedules[self.academic_year].keys())
        if user_input == 'all':
            periods = active_periods.copy()
            print('Update Periods: {}'.format(periods))
            return periods
        choices = list(user_input)
        periods = []
        for choice in choices:
            try:
                p = int(choice)
            except ValueError:
                pass
            else:
                if p in active_periods:
                    periods.append(p)
        if periods:
            print('Update Periods: {}'.format(periods))
            return periods
        else:
            print('Invalid input.')
            print('***** Finished *****')
            exit()

    def get_data(self):
        print('Reading grade books...')
        grades = []  # Array to hold the grades.
        course_titles = []  # Array to hold course titles.

        service = build('sheets', 'v4', credentials=self.credentials)  # Call the Sheets API
        sheet = service.spreadsheets()

        for period in self.periods:
            title = self.schedules[self.academic_year][period]['title']  # Course title
            gb_id = self.schedules[self.academic_year][period]['gradebook_id']  # Gradebook id
            if title not in course_titles:
                try:
                    result = sheet.values().get(spreadsheetId=gb_id, range=self.ss_range).execute()
                    values = result.get('values', [])
                except Exception as e:
                    print('Did not read: {}'.format(title))
                    print(e)
                else:
                    if not values:
                        print('No data found: {}'.format(title))
                    else:
                        course_titles.append(title)
                        for row in values:
                            grades.append(row)

        data = pd.DataFrame(grades, columns=self.data_headers)
        print(data)
        return data  # Pandas DataFrame


if __name__ == '__main__':
    Data()
