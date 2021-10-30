import csv
import time
from googleapiclient.discovery import build
from setup import Setup
from data import Data


class Update:
    """
    Update the existing spreadsheets with the latest grade reports.
    """

    def __init__(self, d):
        self.credentials = d.credentials
        self.date = d.date
        self.semester = d.semester
        self.student_data = d.student_data
        self.time_stamp = self.date.strftime('%Y-%m-%d %H:%M:%S')

    def update_spreadsheets(self):
        """Sends a grade report to students and advisers."""
        print('Running grade reports...')
        index = (lambda i: -13 if self.semester == 1 else -12)(self.semester)

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

            values = [[self.time_stamp] +
                      self.student_data.iloc[s, :3].tolist() +
                      [(lambda j: 'First' if self.semester == 1 else 'Second')(self.semester)] +
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
        print('Checking for new students...')

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
        new_students = Data(df=new_data)

        if len(new_students.student_data) > 0:
            print('New students found.')
            print(new_students.student_data)
            Setup(new_students)
        else:
            print('No new students found.')

    @staticmethod
    def get_letter(g):
        """Returns the letter equivalent of the current grade."""
        grade = int(g)
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
    def remove_students():
        """Removes a student when they drop the course."""
        # TODO Remove sharing.
        # TODO Delete spreadsheet
        # TODO Delete student info from storage.csv
