# FSTL JSON to CSV

For our registration at the cyclos plattform we do not use Cyclos internal services but our own website.
This website is distributed to the members.

At registration at the website, a json as shown in `data/json/example.json` is the result for each registered user.
Cyclos only allows to import ferom CSV.
So, we have to trasform the JSON to CSV, verify the users and apply appropriate roles for each user.

This is done by the `json_2_csv.py` script.

## Prerequisites

It is assumed, that the required data is stored in the data folder as follows:
- `data/json/`: Incoming json from registration website
- `data/csv/users.csv`: Result of the script - CSV with all users
- `data/user_lists/`: Some information to apply the appropriate roles and verify the users
Clearky, in `data/json` only an example and in `data/user_list` no information is checked into this repo. ;)

## Create Virtual Env with required packages
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the Script
```bash
python json_2_csv.py
```
The scipt takes all the json files in `data/json/` and does the following steps:
- verify if the user is a member of the list
- apply the appropriate role
- export all users to `/data/csv/users.csv`