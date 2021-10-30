#!/usr/local/bin/python3
 
from data import Data
from update import Update


if __name__ == '__main__':

    """
    Produces the grade reports and updates the students' spreadsheets.
    Run setup first, if necessary.
    """

    print('******* Grade Reports *******')
    student_data = Data()  # Get data from the gradebooks.
    Update(student_data).update_spreadsheets()  # Update the students' spreadsheets.
    print('******* Finished *******')
