from tkinter import *
from tkinter import filedialog
from read_from_file import read 
from alpha import Alpha
from alpha_plus import AlphaPlus
import PIL.Image
import PIL.ImageTk
from copy import *
from tkinter import messagebox

class StartMenu:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("700x500") #Width x Height
        self.root.title("Alpha miner")
        self.menubar = Menu(self.root, title="menu")
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.runmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu = Menu(self.menubar, tearoff=0)
        
        #self.log = []
        self.opened_filename = ''
        self.opened_file = None
        self.alpha = None
        self.alpha_plus = None
        self.graph_name = ''

    def donothing(self):
        filewin = Toplevel(self.root)
        button = Button(filewin, text="Do nothing button")
        button.pack()

    def open_file(self):
        self.root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
        #print(self.root.filename)
        self.opened_filename = self.root.filename
        self.opened_file = read(self.opened_filename)
        print(self.opened_file)
        self.show_log()


    def run_alpha(self):
        log = []
        log_row = []
        for rows in self.text.get(1.0, END):
            if rows == '\n':
                if log_row != []:
                    log.append(log_row)
                log_row = []
            if rows.isalpha():
                log_row.append(rows)
        #opened_file = deepcopy(self.opened_file)
        if self.radio_v.get() == 2:
            self.alpha = Alpha(log, splines='node')
        else:
            self.alpha = Alpha(log)
        print(self.alpha)
        print("direct succesor:", self.alpha.ds)
        print("causality:",self.alpha.cs)
        print("inversion causality:",self.alpha.inv_cs)
        print("parralell:",self.alpha.pr)
        print("no relation:",self.alpha.ind)
        self.graph_name = self.opened_filename.split('/')[-1][:-4]
        self.alpha.create_graph(self.graph_name, view=False)
        self.show_graph()

    
    def run_alpha_plus(self):
        log = []
        log_row = []
        for rows in self.text.get(1.0, END):
            if rows == '\n':
                if log_row != []:
                    log.append(log_row)
                log_row = []
            if rows.isalpha():
                log_row.append(rows)
            
        #print("tu:", log)
        #opened_file = deepcopy(self.opened_file)
        if self.radio_v.get()  == 2:
            self.alpha_plus = AlphaPlus(log, splines='node')
        else:
            self.alpha_plus = AlphaPlus(log)

        print(self.alpha_plus)
        print("causality: ", self.alpha_plus.cs)
        print("inversion causality:",self.alpha_plus.inv_cs)
        print("parallel: ", self.alpha_plus.pr)
        print("direct succession: ", self.alpha_plus.ds)
        print("loop1: ", self.alpha_plus.get_loop1())
        print("loop2: ", self.alpha_plus.get_loop2())
        print("t_prim: ", self.alpha_plus.t_prim)
        print("l1l: ", self.alpha_plus.l1l)
        print("fl1l: ", self.alpha_plus.fl1l)
        print("log_minus_l1l: ", self.alpha_plus.log_minus_l1l())
        print("no relation: ", self.alpha_plus.ind)
        print("log: ", self.alpha_plus.log)
        self.graph_name = self.opened_filename.split('/')[-1][:-4]
        self.alpha_plus.run_alpha()
        self.alpha_plus.run_alpha_plus(self.graph_name)
        self.show_graph()


        #print("tuuuuuutaj: ", self.text.get(1.0, END))
        

    def create_menubar(self):
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Run", menu=self.runmenu)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        

    def create_file_menu(self):
        self.filemenu.add_command(label="Open", command=self.open_file)
        self.filemenu.add_command(label="Save as pdf", command=self.save_graph_as_pdf)
        #self.filemenu.add_command(label="Close", command=self.donothing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)
    
    def create_run_menu(self):
        self.runmenu.add_command(label="Run alpha miner", command=self.run_alpha)
        self.runmenu.add_command(label="Run alpha+ miner", command=self.run_alpha_plus)

    def create_help_menu(self):
        #self.helpmenu.add_command(label="Help Index",   command=self.donothing)
        self.helpmenu.add_command(label="About...", command=self.show_about)
    
    def show_about(self):
        messagebox.showinfo("About","""This is the simple python program that uses business mining algorithms: alpha and alpha+ in order to create BPMN graphs.\nLogs:
        Program uses .txt logs as input. Example: a b c d.\n Graphs:\n There are 2 types of graph to choose: node and ortho\n Running program:\n Click run in menu and
        choose type of algorithm: alpha or alpha+.\n Output:\n Program generates BPMN graph and shows it in another window. There is an option in file menu to save 
        generated graph as pdf file.""")
        
    def show_graph(self):
        packs = self.root.pack_slaves()
        for l in packs:
            if str(l) != '.!label' and str(l) != '.!label3' and '.!text' not in str(l):
                l.destroy()
        '''new_window = Toplevel(self.root)
        new_window.title('BPMN graph')
        self.im = PhotoImage(file='../graphs/' + self.graph_name + '.png')
        self.label = Label(new_window, image=self.im)
        self.label.pack()'''
        self.im = PhotoImage(file='../graphs/' + self.graph_name + '.png')
        self.label = Label(image=self.im)
        self.label.pack()

    def save_graph_as_pdf(self):
        self.alpha.G.format = 'pdf'
        self.alpha.G.render('../graphs/' + self.graph_name, view=True)
    
    def selected(self):
        print(self.radio_v.get())

    def add_radio_buttons(self):
        l1 = Label(self.root, 
                text='Log:',
                justify = LEFT,
                padx = 20,
                relief='solid')
        l1.pack()
        l1.place(x=0, y=100)
        self.radio_v = IntVar()
        l2 = Label(self.root, 
                text='Choose graph type',
                justify = LEFT,
                padx = 20,
                relief='solid',
                anchor=SW)
        l2.pack()
        l2.place(x=0,y=0)
        self.r1 = Radiobutton(self.root, 
                text="Ortho",
                padx = 20, 
                variable=self.radio_v, 
                value=1,
                command=self.selected)#.pack(anchor=W)
        self.r1.select()
        self.r1.pack(anchor=W)
        self.r1.place(x=0,y=25)
        self.r2 = Radiobutton(self.root, 
                text="Node",
                padx = 20, 
                variable=self.radio_v, 
                value=2,
                command=self.selected)
        self.r2.deselect()
        self.r2.pack(anchor=W)
        self.r2.place(x=0,y=50)

    def show_log(self):
        packs = self.root.pack_slaves()
        for l in packs:
            print(l)
            if str(l) != '.!label':
                l.destroy()
        log_height = 0
        log = ''
        for row in self.opened_file:
            for task in row:
                log += ' ' + (task)
            log += '\n'
            log_height += 1

        '''Label(self.root, 
                text=log,
                justify = LEFT,
                padx = 20,
                relief='solid').pack()'''
        try:
            self.text.delete(1.0, END)
        except:
            pass
        self.text = Text(self.root, height=log_height+1, width=30)
        self.text.pack()
        self.text.place(x=0,y=125)
        self.text.insert(END, log)

    def show_menu(self):
        self.root.config(menu=self.menubar)
        self.root.mainloop()



'''menu = StartMenu()
menu.create_menubar()
menu.create_file_menu()
menu.create_edit_menu()
menu.create_help_menu()
menu.show_menu()'''