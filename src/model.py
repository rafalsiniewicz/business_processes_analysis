from alpha import Alpha
from alpha_plus import AlphaPlus
from read_from_file import read 
from menu import StartMenu

menu = StartMenu()
menu.create_menubar()
menu.create_file_menu()
#menu.create_edit_menu()
menu.create_help_menu()
menu.create_run_menu()
menu.add_radio_buttons()
menu.show_menu()


'''filename = '../logs/log5'
f = read(filename + '.txt')
print(f)
a = Alpha(f)
print(a)
print("direct succesor:", a.ds)
print("causality:",a.cs)
print("inversion causality:",a.inv_cs)
print("parralell:",a.pr)
print("no relation:",a.ind)

a.create_graph(filename, render=True)'''

'''a = AlphaPlus(f)
print("causality: ", a.cs)
print("inversion causality:",a.inv_cs)
print("parallel: ", a.pr)
print("direct succession: ", a.ds)
print("loop1: ", a.get_loop1())
print("loop2: ", a.get_loop2())
print("t_prim: ", a.t_prim)
print("l1l: ", a.l1l)
print("fl1l: ", a.fl1l)
print("log_minus_l1l: ", a.log_minus_l1l())
print("no relation: ", a.ind)
print("log: ", a.log)
a.run_alpha()
a.run_alpha_plus(filename)'''


