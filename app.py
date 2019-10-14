#!/usr/bin/env python3

from data import Data
from update import Update


def main():
    """Produces the grade reports and updates the students' spreadsheets.
    Run setup first, if necessary."""
    print('***** Grade Reports *****')
    data = Data()  # Get data from the gradebooks.
    Update(data)  # Update the students' spreadsheets.
    print('***** Finished *****')


if __name__ == '__main__':
    main()
