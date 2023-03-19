import json
from readable_password import readable_password as rpwd
from fstl_api_handler import fstl_api
import os



    


def load_json(path_to_json: str):
    with open(path_to_json, "r") as json_filehandler:
        json_loaded = json.load(json_filehandler)
    return json_loaded


def normalize_json_data(json_data):
    if type(json_data) == list:
        return json_data
    elif type(json_data) == dict:
        return [json_data]


def get_useraccount_type(user_data):
    return user_data["type"]


def check_if_user_exists(user_data, fstl):
    if get_useraccount_type(user_data) == "Eltern":
        return fstl.check_if_user_exists(user_data["inputEmail"])
    elif get_useraccount_type(user_data) == "Lernbegleiter":
        return fstl.check_if_user_exists(f"{user_data['Forename']} {user_data['Surname']}")


def get_role_of_user(user_data):
    pass


def main():

    # get the credentials from env vars
    FSTL_CYCLOS_ADMIN_USERNAME = os.getenv("FSTL_CYCLOS_ADMIN_USERNAME")
    FSTL_CYCLOS_ADMIN_PASSWORD = os.getenv("FSTL_CYCLOS_ADMIN_PASSWORD")
    # initialize instance to interact with the API
    print("Initializing API to interact with Cyclos FSTL Community.")
    fstl = fstl_api(FSTL_CYCLOS_ADMIN_USERNAME, FSTL_CYCLOS_ADMIN_PASSWORD)



    # load the incoming json file
        # if array if jsons -> work with it
        # if not -> make to array

    # iterate over each item in this array, for each
        # check if lernbegleiter or eltern user
        # if lernbegleiter
            # check via api if a cyclos user with this name as loginname exists:
                # if yes -> go to next item               
                # if no:
                    # validate the role of the user
                    # create params for user creation

        # if eltern
            # check via api if a cyclos user with this email as loginname exists:            
                # if yes -> go to next item               
                # if no:
                    # validate the role of the user
                    # create params for user creation

    # create an export with the current state of users in cyclos

    pass


if __name__ == "__main__":
    main()