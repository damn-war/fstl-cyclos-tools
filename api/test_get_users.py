#!/usr/bin/python3

from FSTL_API import fstl_api
import os

if __name__ == "__main__":

    # get the credentials from env vars
    ADMIN_USERNAME = os.getenv("FSTL_CYCLOS_ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("FSTL_CYCLOS_ADMIN_PASSWORD")

    # overview of the internal names of the most important groups
    # caution: internal names, case sensitive
    # unluckily, groups are not (directly) available via the API
    # commented since not used in the code
    # groups = ("eltern", "leitung_fstl", "team_fstl", "vorstand", "ehemalige", "elternrat", "elternrat_mitglied")
    # privileged_groups = ("leitung_fstl", "team_fstl", "vorstand", "elternrat"")
    # normal_groups = ("eltern", "ehemalige")
    # possible_user_stati = ("active", "blocked", "disabled", "pending", "purged", "removed")

    # initialize instance to interact with the API
    print("Initializing API to interact with Cyclos FSTL Community.")
    fstl = fstl_api(ADMIN_USERNAME, ADMIN_PASSWORD)

    # just a test call

    users = fstl.get_users()

    print(users)
   
    print( any(d["display"] == "admin_bacwkup" for d in users))

    