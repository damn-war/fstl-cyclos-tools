import json
from readable_password import readable_password as rpwd
from fstl_api_handler import fstl_api
import os
import argparse


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("json_import_path", type=str,
                    help="path to json to import")
    parser.add_argument("json_export_path", type=str,
                help="path to json to export")
    args = parser.parse_args()
    return args


def normalize_json_data(json_data):
    if type(json_data) == list:
        return json_data
    elif type(json_data) == dict:
        return [json_data]


def load_json(path_to_json: str):
    with open(path_to_json, "r") as json_filehandler:
        json_loaded = json.load(json_filehandler)
    return normalize_json_data(json_loaded)


def get_useraccount_type(user_data):
    if user_data["children"] is not None:
        return "Eltern"
    else:
        return "Team_FSTL"


def check_if_user_exists(user_data, fstl):
    if get_useraccount_type(user_data) == "Eltern":
        display_name = f'{user_data["parents"]["1"]["inputParentForename"]} {user_data["parents"]["1"]["inputParentSurname"]}'
        return fstl.check_if_user_exists(display_name)
    elif get_useraccount_type(user_data) == "Team_FSTL":
        return fstl.check_if_user_exists(f"{user_data['Forename']} {user_data['Surname']}")


def get_group_for_user(user_data, path_to_mapfiles="data/privileged_members/"):
    priv_files = os.listdir(path_to_mapfiles)
    # check if user data is in list of privileged users
    # return the corresponding role
    account_type = get_useraccount_type(user_data)
    if account_type == "Team_FSTL":
        return "Team_FSTL"
    elif account_type == "Eltern":
        for group in priv_files:
            with open(f"{path_to_mapfiles}{group}", "r") as filehandler:
                for line in filehandler:
                    for element in user_data["parents"].items():
                        forename = element[1]["inputParentForename"]
                        if "inputParentSurname" in element[1]:
                            surname = element[1]["inputParentSurname"]
                        elif "inputParentSurename" in element[1]:
                            surname = element[1]["inputParentSurename"]
                        if f"{forename} {surname}" in line:
                            return group.capitalize()
        return "Eltern"
    else:
        return None

def json_dict_2_multiline_string(json_dict):
    multiline_string = ""
    for element in json_dict.items():
        for item in element[1]:
            # append to csv string, apply correct names
            multiline_string += f"{element[1][item].replace('primary', 'Grundschule').replace('secondary', 'Gesamtschule')} "
        # append newline to end csv row correctly
        multiline_string += "\n"
    return multiline_string[0:-1]


def create_params_for_user(user_data):
    group = get_group_for_user(user_data, path_to_mapfiles="data/privileged_members/")
    email = user_data["inputEmail"]
    username = email
    
    if get_useraccount_type(user_data) == "Eltern":
        name = f'{user_data["parents"]["1"]["inputParentForename"]} {user_data["parents"]["1"]["inputParentSurname"]}'
        kinder = json_dict_2_multiline_string(user_data["children"]) if "children" in user_data else ""
        sorgeberechtige = json_dict_2_multiline_string(user_data["parents"])
    elif get_useraccount_type(user_data) == "Team_FSTL":
        name = f'{user_data["inputForename"]} {user_data["inputSurname"]}'
    # get kinder and sorgeberechtigte

    # create readable random password
    password = rpwd.readable_password(length=8, incl_upper=True, incl_digit=True, incl_punc=False)
    group = get_group_for_user(user_data)
    params = {
        "name": name,
        "username": username,
        "email": email,
        "sorgeberechtige": sorgeberechtige,
        "kinder": kinder,
        "group":group,
        "password":password
    }
    return params

def main():


    args = parse()
    json_import_path = args.json_import_path
    json_export_path = args.json_export_path

    # check if export file exists
    if not os.path.exists("/".join(json_export_path.split("/")[:-1])):
        os.makedirs("/".join(json_export_path.split("/")[:-1]))
    if not os.path.isfile(json_export_path):
        with open(json_export_path, mode='w', encoding='utf-8') as f:
            json.dump([], f)
    

    # get the credentials from env vars
    FSTL_CYCLOS_ADMIN_USERNAME = os.getenv("FSTL_CYCLOS_ADMIN_USERNAME")
    FSTL_CYCLOS_ADMIN_PASSWORD = os.getenv("FSTL_CYCLOS_ADMIN_PASSWORD")
    # initialize instance to interact with the API
    print("Initializing API to interact with Cyclos FSTL Community.")
    fstl = fstl_api(FSTL_CYCLOS_ADMIN_USERNAME, FSTL_CYCLOS_ADMIN_PASSWORD)

    # load the incoming json file
        # if array if jsons -> work with it
        # if not -> make to array
    loaded_data = load_json(json_import_path)
    print(len(loaded_data))
    for user_data in loaded_data:
        if not check_if_user_exists(user_data, fstl):
            user_params = create_params_for_user(user_data)
            export_values = ["username", "password"]
            
            export_dict = {key: user_params[key] for key in export_values}
            print(export_dict)
            with open(json_export_path) as fp:
                listObj = json.load(fp)
            if not any(d['username'] == export_dict['username'] for d in listObj):
                listObj.append(export_dict)
            else:
                for elem in listObj:
                    if elem['username'] == export_dict['username']:
                        elem['password'] = export_dict['password']
            with open(json_export_path, mode='w', encoding='utf-8') as json_file:
                json.dump(listObj, json_file, 
                                    indent=4,  
                                    separators=(',',': '))
            print(fstl.create_user(user_params))

    pass


if __name__ == "__main__":
    main()