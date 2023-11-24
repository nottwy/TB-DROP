import os

f = open('C:/Users/12046/Desktop/picture/S04/status.txt','r')
status = f.read ()
print((status))
f=str(status)
print(f=='error\n')