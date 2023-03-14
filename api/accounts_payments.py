#!/usr/bin/python3

from FSTL_API import fstl_api
import os

def reset_all_balances():
    pass

if __name__ == "__main__":

    # get the credentials from env vars
    ADMIN_USERNAME = os.getenv("FSTL_CYCLOS_ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("FSTL_CYCLOS_ADMIN_PASSWORD")

    # initialize instance to interact with the API
    print("Initializing API to interact with Cyclos FSTL Community.")
    fstl = fstl_api(ADMIN_USERNAME, ADMIN_PASSWORD)

    print(fstl.get_balance_of_users())