#!/usr/bin/env python3

import authenticate
from data import Data
import update

"""
Run setup first, if not already done.
Run this to produce the reports.
"""


def main():
    # Main
    print('***** Grade Reports *****')
    credentials = authenticate.get_credentials()  # Authenticate
    data = Data(credentials)  # Read grade spreadsheets
    update.update_spreadsheets(credentials, data)  # Update student spreadsheets
    print('***** Finished *****')


if __name__ == '__main__':
    main()
