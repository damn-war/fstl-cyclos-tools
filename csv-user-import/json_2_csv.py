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


def get_group_for_user():
    pass


def json_dict_2_csv_string(json_dict):
    csv_string = ""
    for element in json_dict.items():
        for item in element[1]:
            csv_string += f"{element[1][item].replace('primary', 'Primar').replace('secondary', 'Sekundar')} "
        csv_string += "\n"
    return csv_string


def get_row_from_json(json_data):
    email = json_data["inputEmail"]
    name = email
    username = email
    kinder = json_dict_2_csv_string(json_data["children"])
    sorgeberechtige = json_dict_2_csv_string(json_data["parents"])
    password = rpwd.readable_password(length=8, incl_upper=True, incl_digit=True, incl_punc=False)
    group = "Eltern"
    forcechange = "true"
    row = [name, username, email, kinder,
           sorgeberechtige, group, password, forcechange]
    return row


def main():

    json_data_list = []
    for json_filename in json_files:
        with open(path_to_json+json_filename, "r") as json_filehandler:
            json_data_list.append(json.load(json_filehandler))

    if not os.path.exists(path_to_csv):
        os.makedirs(path_to_csv)
    with open(path_to_csv+"users.csv", "w") as csv_filehandler:
        csv_writer = csv.writer(csv_filehandler, delimiter=';')
        csv_writer.writerow(csv_header)
        for json_data in json_data_list:
            csv_writer.writerow(get_row_from_json(json_data))


if __name__ == "__main__":
    main()
