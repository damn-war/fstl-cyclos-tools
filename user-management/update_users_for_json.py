import json


def load_json(path_to_json: str):
    with open(path_to_json, "r") as json_filehandler:
        json_loaded = json.load(json_filehandler)
    return json_loaded


def normalize_json_data(json_data):
    if type(json_data) == list:
        return json_data
    elif type(json_data) == dict:
        return [json_data]


def main():

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