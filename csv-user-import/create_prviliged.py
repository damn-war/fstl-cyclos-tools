import csv
import os
from readable_password import readable_password as rpwd

path_to_csv = 'data/csv/'
csv_header = ["name", "username", "email", "field.kinder", "field.sorgeberechtigte",
              "group", "password.login.value", "password.login.forcechange"]

csv_export_filename = "privileged.csv"
csv_memberlist_filename = "Mitglieder_Verein.CSV"

privileged_filenames = ["geschäftsführung", "lernbegleiter"]


def main():

    #row = [name, username, email, kinder,
    #       sorgeberechtige, group, password, forcechange]

    users = []

    with open(path_to_csv+csv_export_filename, "w") as csv_filehandler:
        csv_writer = csv.writer(csv_filehandler, delimiter=';')
        csv_writer.writerow(csv_header)
        for group in privileged_filenames:
            with open(f"data/user-lists/{group}", "r") as filehandler:
                for line in filehandler:
                    forename, surname = line.replace("\n", "").split(" ")
                    print(forename, surname)
                    email = ""
                    with open(f"data/user-lists/{csv_memberlist_filename}", encoding='utf-8-sig') as csv_filehandler:
                        reader = csv.DictReader(csv_filehandler, delimiter=";")
                        for row in reader:
                            if forename in row["Vorname"] and surname in row["Nachname"]: # <- not perfect but first guess
                                email = row["EMail"]
                    name = f"{forename} {surname}"
                    username = name
                    kinder = ""
                    sorgeberechtige = ""
                    role = group.capitalize()
                    password = rpwd.readable_password(length=8, incl_upper=True, incl_digit=True, incl_punc=False)
                    forcechange = "true"
                    row = [name, username, email, kinder,
                        sorgeberechtige, role, password, forcechange]
                    if email != "":
                        csv_writer.writerow(row)


if __name__ == "__main__":
    main()
