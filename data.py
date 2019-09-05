from datetime import datetime as dt

import pandas as pd
from googleapiclient.discovery import build

from authenticate import get_credentials
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

    def __init__(self, c, d=None):
        Schedule.__init__(self)
        self.date = dt.today()
        if d is None:
            self.student_data = self.get_data(c)
        else:
            self.student_data = d  # Pandas DataFrame

    def get_data(self, c):
        print('Reading grade books...')
        grades = []  # Array to hold the grades

        service = build('sheets', 'v4', credentials=c)  # Call the Sheets API
        sheet = service.spreadsheets()

        for course in self.mb_2019_2020:
            ss_id = self.mb_2019_2020[course]  # Spreadsheet ID
            try:
                result = sheet.values().get(spreadsheetId=ss_id, range=self.ss_range).execute()
                values = result.get('values', [])
            except Exception as e:
                print('Did not read: {}'.format(course))
                print(e)
            else:
                if not values:
                    print('No data found: {}'.format(course))
                else:
                    for row in values:
                        grades.append(row)

        data = pd.DataFrame(grades, columns=self.data_headers)
        print(data)
        return data  # Pandas DataFrame


def test():
    """Test for data.py"""
    test_credentials = get_credentials()
    Data(test_credentials)


if __name__ == '__main__':
    test()
