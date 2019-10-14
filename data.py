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
        self.date = dt.today()
        self.credentials = Authenticate.get_credentials()
        if df is None:
            self.student_data = self.get_data()
        else:
            self.student_data = df  # Pandas DataFrame

    def get_data(self):
        print('Reading grade books...')
        grades = []  # Array to hold the grades.
        course_titles = []  # Array to hold course codes.

        service = build('sheets', 'v4', credentials=self.credentials)  # Call the Sheets API
        sheet = service.spreadsheets()

        for period in self.schedules['2019_2020']:
            title = self.schedules['2019_2020'][period]['title']  # Course title
            gb_id = self.schedules['2019_2020'][period]['gradebook_id']  # Gradebook id
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
