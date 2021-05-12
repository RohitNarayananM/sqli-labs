from collections import Counter

f=open('interaction1.txt','r').read()

x=counter(f)
x=list(x)[17:-7]
for i in range(len(x)):
	f=f.replace(x[i],chr(i+32)+" ")
q=open('new.txt','w+')
q.write(f)
q.close()


