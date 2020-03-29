from alpha import Alpha
from read_from_file import read 

filename = "log4"
f = read(filename + '.txt')
print(f)
a = Alpha(f)
#print(a)
#print(a.ds)
#print(a.cs)
#print(a.pr)
#print(a.inv_cs)

a.create_graph(filename)