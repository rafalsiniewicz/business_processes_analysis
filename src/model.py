from alpha import Alpha
from read_from_file import read 

f = read("log4.txt")
print(f)
a = Alpha(f)
#print(a)
#print(a.ds)
print(a.cs)
#print(a.pr)
#print(a.inv_cs)

a.create_graph('log4')