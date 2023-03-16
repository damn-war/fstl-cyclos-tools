import json
import csv
import os
from readable_password import readable_password as rpwd


path_to_json = 'data/json/'
json_files = [pos_json for pos_json in os.listdir(
    path_to_json) if pos_json.endswith('.json')]

path_to_csv = 'data/csv/'
csv_header = ["name", "username", "email", "field.kinder", "field.sorgeberechtigte",
              "group", "password.login.value", "password.login.forcechange"]

csv_export_filename = "users.csv"
csv_memberlist_filename = "Mitglieder_Verein.CSV"

privileged_filenames = ["elternrat", "geschäftsführung", "lernbegleiter", "vorstand"]

def validate_json_userdata(json_data):
    # json record is validated if
    # 1. combination of any opf the parents name is in the list of the members of the club
    # 2. email is in the list of the members of the club

    with open(f"data/user-lists/{csv_memberlist_filename}", encoding='utf-8-sig') as csv_filehandler:
        reader = csv.DictReader(csv_filehandler, delimiter=";")
        for row in reader:
            if json_data["inputEmail"] in row["EMail"]:
                return True
            for element in json_data["parents"].items():
                forename = element[1]["inputParentForename"]
                if "inputParentSurname" in element[1]:
                    surname = element[1]["inputParentSurname"]
                elif "inputParentSurename" in element[1]:
                    surname = element[1]["inputParentSurename"]
                if forename in row["Vorname"] and surname in row["Nachname"]: # <- not perfect but first guess
                    return True
    return False


def get_group_for_user(json_data):
    for group in privileged_filenames:
        with open(f"data/user-lists/{group}", "r") as filehandler:
            for line in filehandler:
                for element in json_data["parents"].items():
                    forename = element[1]["inputParentForename"]
                    if "inputParentSurname" in element[1]:
                        surname = element[1]["inputParentSurname"]
                    elif "inputParentSurename" in element[1]:
                        surname = element[1]["inputParentSurename"]
                    if f"{forename} {surname}" in line:
                        return group.capitalize()
    return "Eltern"
        
    


def json_dict_2_csv_string(json_dict):
    csv_string = ""
    for element in json_dict.items():
        for item in element[1]:
            # append to csv string, apply correct names
            csv_string += f"{element[1][item].replace('primary', 'Grundschule').replace('secondary', 'Gesamtschule')} "
        # append newline to end csv row correctly
        csv_string += "\n"
    return csv_string


def get_row_from_json(json_data):
    # input email is used for three fields
    email = json_data["inputEmail"]
    name = email
    username = email
    
    # get kinder and sorgeberechtigte
    kinder = json_dict_2_csv_string(json_data["children"]) if "children" in json_data else ""
    sorgeberechtige = json_dict_2_csv_string(json_data["parents"])

    # create readable random password
    password = rpwd.readable_password(length=8, incl_upper=True, incl_digit=True, incl_punc=False)
    group = get_group_for_user(json_data)
    forcechange = "true"
    row = [name, username, email, kinder,
           sorgeberechtige, group, password, forcechange]
    return row


def load_json_data(file="all"):
    json_data_list = []
    if file == "all":
        # load all the data from the json files in data/json
        for json_filename in json_files:
            with open(path_to_json+json_filename, "r") as json_filehandler:
                # validation step
                json_loaded = json.load(json_filehandler)
                if type(json_loaded) == dict:
                    json_data_list.append()
                elif type(json_loaded) == list:
                    json_data_list += json_loaded
    else:
        with open(path_to_json+file, "r") as json_filehandler:
            json_loaded = json.load(json_filehandler)
            if type(json_loaded) == dict:
                json_data_list.append()
            elif type(json_loaded) == list:
                json_data_list += json_loaded
    print(f"Loaded json(s) with {len(json_data_list)} records.")
    return json_loaded


def main():

    json_data_list = load_json_data("2023-03-15_21-56-35_cyclos_data.json")

    # make sure export dir exists
    if not os.path.exists(path_to_csv):
        os.makedirs(path_to_csv)

    # write row to csv
    with open(path_to_csv+csv_export_filename, "w") as csv_filehandler:
        csv_writer = csv.writer(csv_filehandler, delimiter=';')
        csv_writer.writerow(csv_header)
        for json_data in json_data_list:
            # only write single row to csv if json is a single entry
            if type(json_data) == dict:
                csv_writer.writerow(get_row_from_json(json_data))


if __name__ == "__main__":
    main()
