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

    # which logic is required to make everything fine?
    #   - each new member of eltern is per default in the eltern group
    #   - at registering one can choose between "eltern" and "ehemalige"
    #   - members of the other groups must be added manually by the admin, can be automated as well
    #   - every member of the "eltern" group must has several brokers, namely:
    #       - Elternrat
    #       - Vorstand
    #       - each member of the group "Vorstand"
    #       - each member of the group "Elternrat"
    #       - each member of the group "Team FSTL"
    #       - each member of the group "Leistung FSTL"
    #   - there are no other brokers as the above listed <- use broker as identifier
    #   - users in the group ehemalige do not need brokers

    # Operations done in the script:
    #   get all active members of the group "eltern"
    #   get all active brokers
    #   add each broker to each member
    #   delete broker from user if not in list of active brokers

    print("Getting the list of all active eltern accounts.")
    eltern_list = fstl.get_users(group="eltern", status=["active"])
    print("Getting the list of all active broker accounts.")
    broker_list = fstl.get_users(role="broker", status=["active"])

    # go over all activated eltern accounts
    for eltern in eltern_list:
        # add all broker of list to any eltern account
        for broker in broker_list:
            print(
                f"Adding Broker {broker['display']} to eltern account {eltern['display']}"
            )
            # add vorstand as the main broker
            if broker["display"] == "Vorstand":
                fstl.add_broker_to_user(eltern["id"], broker["id"], main_broker=True)
            # and all other brokers not as main broker
            else:
                fstl.add_broker_to_user(eltern["id"], broker["id"])
        # get the list of brokers of an eltern account
        broker_list_of_eltern = fstl.get_brokers_of_user(eltern["id"])["brokers"]
        # if there is a broker in this list, which is not in the list of active brokers
        # (i.e. as an artifact of deletion of a broker)
        # delete this broker from this eltern account
        for broker_id in [broker["broker"]["id"] for broker in broker_list_of_eltern]:
            if broker_id not in [broker["id"] for broker in broker_list]:
                print(
                    f"Removing not activ Broker with id {broker_id} from eltern account {eltern['display']}"
                )
                fstl.delete_broker_from_user(eltern["id"], broker_id)
