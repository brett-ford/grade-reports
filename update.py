import csv
import time
from datetime import datetime as dt

from googleapiclient.discovery import build

from setup import Setup
from data import Data


class Update:
    """Update the existing spreadsheets with the latest grade reports."""

    def __init__(self, data):
        self.date = data.date
        self.credentials = data.credentials
        self.student_data = data.student_data

    def update_spreadsheets(self):
        """Sends a grade report to students and advisers."""
        print('Running grade reports...')

        time_stamp = self.date.strftime('%Y-%m-%d %H:%M:%S')
        semester = self.get_semester(self.date)
        index = (lambda i: -13 if semester == 'First' else -12)(semester)

        self.new_students()  # Check for new students first

        # Read storage.csv and create a dictionary of existing students.
        existing_students = {}  # Dictionary of tuples.
        with open('storage.csv', 'r') as storage:
            reader = csv.reader(storage)
            for row in reader:
                existing_students[row[0]] = (row[1], row[2])

        service = build('sheets', 'v4', credentials=self.credentials)  # Call the Sheets API.

        # Update each student's sheet with current grade information.
        for s in self.student_data.index:
            time.sleep(3)
            spreadsheet_id = existing_students[self.student_data.loc[s]['Student Email']][1]

            values = [[time_stamp] +
                      self.student_data.iloc[s, :3].tolist() +
                      [semester] +
                      [self.get_letter(self.student_data.iloc[s, index])] +
                      self.student_data.iloc[s, 8:].tolist()]
            body = {'values': values, 'majorDimension': 'rows'}
            try:
                result = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id,
                                                                valueInputOption='RAW',
                                                                range='Sheet1!A1',
                                                                body=body).execute()
            except Exception as e:
                print('Not updated: {}'.format(self.student_data.loc[s]['Student Email']))
                print(e)
            else:
                print(values[0])  # Verify success.
                print('{} cells appended.'.format(result.get('updates').get('updatedCells')))

    def new_students(self):
        """Checks data for new students."""
        print('New students...')

        # Creates list of existing students.
        existing_students = []
        with open('storage.csv', 'r') as storage:
            reader = csv.reader(storage)
            for row in reader:
                existing_students.append(row[0])

        def mask(email):
            if email in existing_students:
                return False
            return True

        # Reduces student_data DataFrame to new students only.
        new_data = self.student_data[self.student_data['Student Email'].apply(mask)]
        new = Data(df=new_data)

        if len(new.student_data) > 0:
            print('New students found.')
            print(new.student_data)
            Setup(new)
        else:
            print('No new students.')

    @staticmethod
    def get_letter(grade):
        """Determines the letter equivalent of the current grade."""
        grade = int(grade)
        letters = {range(90, 93): 'A-', range(93, 97): 'A', range(97, 110): 'A+',
                   range(80, 83): 'B-', range(83, 87): 'B', range(87, 90): 'B+',
                   range(70, 73): 'C-', range(73, 77): 'C', range(77, 80): 'C+',
                   range(60, 63): 'D-', range(63, 67): 'D', range(68, 70): 'D+',
                   range(60): 'E'
                   }
        for scale in letters:
                if grade in scale:
                    return letters[scale]

    @staticmethod
    def get_semester(date):
        """Determines the current semester."""
        semester_2_start = dt(2020, 1, 22)
        if date > semester_2_start:
            return 'Second'
        return 'First'

    @staticmethod
    def remove_students():
        """Removes a student when they drop the course."""
        # Remove sharing
        # Delete spreadsheet
        # Delete student info from storage.csv
        pass
