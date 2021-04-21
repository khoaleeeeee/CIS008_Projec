from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Treeview
import pandas as pd
import movie_revenue_tool as mrt

from matplotlib.figure import Figure
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class DataAnalysis_Project:
    def __init__(self):
        window = Tk()
        window.title("Final Project")
        window.geometry("450x500")
        window.config(pady=20)

        #----------------------------------------------------
        # Create a menu bar
        menubar = Menu(window)
        window.config(menu = menubar)

        helpMenu = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "Help", menu = helpMenu)
        helpMenu.add_command(label = "How to Use", command = self.howToUse)
        # opens messagebox to show instructions on how to use
        helpMenu.add_command(label = "About Project", command = self.about)
        # opens messagebox that lists our group 3 members, you can change it

        #----------------------------------------------------
        # Calculate widgets, these top widgets are placed on a frame
        frame1 = Frame(window)
        frame1.pack()
        
        budget_label = Label(frame1, text = "Budget: ")
        budget_label.grid(row = 1, column = 0, sticky = E)

        #entry input will be put in this predictedRevenueVar variable
        self.predictedRevenueVar = StringVar()
        budget_entry = Entry(frame1, width=20, textvariable = self.predictedRevenueVar)
        budget_entry.grid(row = 1, column = 1, padx = 10, sticky = W)

        cal_button = Button(frame1, text="Calculate", width=10, command = self.compute)
        cal_button.grid(row=1, column=2)

        rev_label = Label(frame1, text = "Predicted Revenue: ")
        rev_label.grid(row = 2, column = 0)

        self.cal_label = Label(frame1, text = "")
        self.cal_label.grid(row = 2, column = 1, padx = 10, sticky = W)

        # Graph Button
        bt_graph = Button(frame1, text="Draw a Graph", width=20, command = self.graph_window)
        bt_graph.grid(row=3, column=1, padx=10, pady=10, sticky=W)

        #---------------------------------------------------
        # Frame for a Treeview
        tv_frame = LabelFrame(window, text = 'Data')
        tv_frame.place(relheight=0.55, relwidth=1, rely=0.2, relx=0)#height=250, width=450,
        #I replaced height and width with relheight and relwidth, so that the labelframe would
            #expand if you change the size of the window when you drag along the window's edges

        # Treeview Widget
        self.tv1 = Treeview(tv_frame)
        self.tv1.place(relheight=1, relwidth=1)

        tv_scrolly = Scrollbar(tv_frame, orient = "vertical", command = self.tv1.yview)
        tv_scrolly.pack(side='right', fill = 'y')

        tv_scrollx = Scrollbar(tv_frame, orient = "horizontal", command = self.tv1.xview)
        tv_scrollx.pack(side='bottom', fill = 'x')
        
        self.tv1.configure(yscrollcommand = tv_scrolly.set, xscrollcommand = tv_scrollx.set)

        #---------------------------------------------------------------------
        # Select file and load widgets
        self.file_label = Label(window, text="No File Selected")
        self.file_label.place(rely=0.82, relx=0.1)

        select_button = Button(window, text="Browse a File", command = lambda: self.file_browse())
        select_button.place(rely=0.88, relx=0.1)
        
        load_button = Button(window, text="Load", command=lambda: self.load_data())
        load_button.place(rely=0.88, relx=0.3)
        
        window.mainloop()

    def compute(self):
        #since the self.predictedRevenueVar is a stringVar, I have to convert it to a number data
            #type using eval, I put the code in a try/except block in case the use could enter non-numbers
        try:
            value = float(self.predictedRevenueVar.get()) # convert stringVar to a float 
            calculation = format(mrt.get_predicted_revenue(value), '.2f') #calculation and make sure there are 2 numbers after decimal
            cal_string = "$ " + calculation #I put the float into a string to add the $ sign
            
            messagebox.showinfo(title='Revenue', message='Movie\'s estimate revenue: ' +cal_string)
        
            self.cal_label["text"] = cal_string
        except ValueError:
            self.cal_label["text"] = self.cal_label["text"]

            messagebox.showerror("Error", "Invalid Input: Must be a Number")

     
    def graph_window(self): 
        global graph
        graph = Toplevel()
        graph.geometry("500x500")
        graph.title("Graph")
        button = Button(graph, text="Close Window", command=graph.destroy)
        button.pack()
        self.plot()

    def plot(self):
        fig = Figure(figsize=(5, 5), dpi=75)
        
        plot1 = fig.add_subplot(1, 1, 1)
        mrt.model_visualization(plot = plot1)
    
        canvas = FigureCanvasTkAgg(fig, master=graph)
        canvas.draw()
        canvas.get_tk_widget().pack()
    
        toolbar = NavigationToolbar2Tk(canvas, graph)
        toolbar.update()
    
        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()

    def file_browse(self):
        filename = filedialog.askopenfilename(filetypes = (('xlsx Files', '*.xlsx')
                                                           , ('All Files', '*.*')
                                                           , ('CSV Files', '*.csv')))

        if filename == "":
            self.file_label["text"] = self.file_label["text"] #"No File Selected"
        else:
            self.file_label["text"] = filename
        #I noticed that when you don't select a file, the label will display a blank, so I used
            # an if/else to make sure that label text will display the default message when a file
            #is not selected
        #and in order for this function to change the label that is in the init function, I self
            #referenced the label by putting self. in front of it and also in the function as well

    def load_data(self):
        filepath = self.file_label["text"]
        try:
            filename = r"{}".format(filepath)

            #df means dataframe
            if filename[-4: ] == ".csv":
                df = pd.read_csv(filename)
            else:
                df = pd.read_excel(filename)
                
        except ValueError:
            messagebox.showerror("Error", "Invalid File")
            #the first string argument of this messagebox it the title, the 2nd is the message in the box
            return None
        except FileNotFoundError:
            messagebox.showerror("Error", "No such file exists")
            return None

        self.clear_data()
        self.tv1["column"] = list(df.columns)
        self.tv1["show"] = "headings"

        for column in self.tv1["columns"]:
            self.tv1.heading(column, text=column)
        
        df_rows = df.to_numpy().tolist()

        for row in df_rows:
            self.tv1.insert("", "end", values=row)
            
        return None
        
    def clear_data(self):
        self.tv1.delete(*self.tv1.get_children())
        #return None
        #needed to put self. on tv1 so the functions can access the variables in the init method

    def howToUse(self):
        instruction = "1. Click Browse a File to select a file\n" + \
                      "2. After Selecting a file, click the Load button\n" + \
                      "3. Enter the budget\n" + "4. Click Compute"
        messagebox.showinfo("How To Use", instruction)

    def about(self):
        info = "CIS 008 - Group 3 Members:\n" + "  Dang le\n" + "  Christopher Denson\n" + \
               "  Kathy Nguyen\n" + "  Arvind Vallabha"
        messagebox.showinfo("About Project", info)

DataAnalysis_Project()

