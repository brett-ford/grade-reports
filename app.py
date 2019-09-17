#!/usr/bin/env python3

import authenticate
from data import Data
import update


def main():
    """Produces the grade reports and updates student spreadsheets.
    Run setup first, if necessary."""
    print('***** Grade Reports *****')
    credentials = authenticate.get_credentials()  # Authenticate
    data = Data(credentials)  # Read grade spreadsheets
    update.update_spreadsheets(credentials, data)  # Update the students' spreadsheets
    print('***** Finished *****')


if __name__ == '__main__':
    main()
