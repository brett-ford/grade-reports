import csv
from googleapiclient.discovery import build
from authenticate import Authenticate
from data import Data


class Setup:
    """
    Create a Google Sheet for each student.
    Add headers to each sheet.
    Share the sheet with the student and adviser.
    Add student email, advisor email, and spreadsheet id to storage.csv
    """

    def __init__(self, d):
        self.credentials = Authenticate.get_credentials()
        self.run_setup(d)

    def run_setup(self, data):
        """Sets up a Google Sheet with column headers for each student."""
        print('Setup...')
        student_data = data.student_data  # DataFrame only

        service = build('sheets', 'v4', credentials=self.credentials)  # Call the Sheets API

        for s in student_data.index:
            # Create a sheet for the student.
            first = student_data.loc[s]['First']
            last = student_data.loc[s]['Last']
            course = student_data.loc[s]['Course']
            title = 'Grades -- ' + course + ' -- ' + first + ' ' + last
            student_email = student_data.loc[s]['Student Email']
            adviser_email = student_data.loc[s]['Advisor Email']

            try:
                body = {'properties': {'title': title}}
                spreadsheet = service.spreadsheets().create(body=body,
                                                            fields='spreadsheetId').execute()
                ss_id = spreadsheet.get('spreadsheetId')
            except Exception as e:
                print('Did not create {}:'.format(title))
                print(e)
            else:
                print(title)
                print('Spreadsheet ID: {}'.format(ss_id))

                # Add the column headers.
                try:
                    values = [data.report_headers]
                    body = {'values': values, 'majorDimension': 'rows'}
                    service.spreadsheets().values().append(spreadsheetId=ss_id,
                                                           valueInputOption='RAW',
                                                           range='Sheet1!A1',
                                                           body=body).execute()
                except Exception as e:
                    print('Did not add headers: {}'.format(title))
                    print(e)
                else:
                    print('Headers')

                    # Share file with student and adviser.
                    def callback(request_id, response, exception):
                        if exception:
                            print(exception)  # Handle error.
                        else:
                            print('Request ID: {}'.format(request_id))
                            print('Permission ID: {}'.format(response.get('id')))

                    try:
                        drive_service = build('drive', 'v3', credentials=self.credentials)
                        batch = drive_service.new_batch_http_request(callback=callback)
                        student_permission = {'type': 'user', 'role': 'reader', 'emailAddress': student_email}
                        adviser_permission = {'type': 'user', 'role': 'reader', 'emailAddress': adviser_email}
                        batch.add(drive_service.permissions().create(fileId=ss_id,
                                                                     body=student_permission,
                                                                     fields='id'))
                        batch.add(drive_service.permissions().create(fileId=ss_id,
                                                                     body=adviser_permission,
                                                                     fields='id'))
                        batch.execute()
                    except Exception as e:
                        print('Not shared: {}, {}'.format(student_email, adviser_email))
                        print(e)
                    else:
                        print('Shared: {}, {}'.format(student_email, adviser_email))

                    # Creates csv file to store contact info.
                        try:
                            with open('storage.csv', 'a', newline='') as storage:
                                writer = csv.writer(storage)
                                writer.writerow([student_email, adviser_email, ss_id])
                        except Exception as e:
                            print('Not added to storage: {}'.format(student_email))
                            print(e)
                        else:
                            print('Storage')
            print()


if __name__ == '__main__':
    setup_data = Data()
    Setup(setup_data)
