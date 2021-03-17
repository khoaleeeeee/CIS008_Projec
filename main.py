from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Treeview
import pandas as pd

from matplotlib.figure import Figure
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

window = Tk()
window.title("Final Project")
window.geometry("450x500")
window.config(pady=20)

def graph_window():
    global graph
    graph = Toplevel(window)
    graph.geometry("500x500")
    graph.title("Graph")
    button = Button(graph, text="Close Window", command=graph.destroy)
    button.pack()
    plot()

def plot():
    fig = Figure(figsize=(5, 5), dpi=75)
    x = np.linspace(1, 5, 100)
    y = [i ** 2 for i in x]
    plot1 = fig.add_subplot(111)
    plot1.plot(x, y)

    canvas = FigureCanvasTkAgg(fig, master=graph)
    canvas.draw()
    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas, graph)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()



# Calculate
cal_label = Label(text="Predicted Revenue: ")
cal_label.grid(row=1, column=0)
cal_entry = Entry(width=15)
cal_entry.grid(row=1, column=1)
cal_button = Button(text="Calculate", width=7)
cal_button.grid(row=1, column=2)

# Graph button
graph_button = Button(text="Draw A Graph", width=20, command=graph_window)
graph_button.grid(row=2, column=1, padx=10, pady=10)

frame = LabelFrame(text="Data")
frame.place(height=250, width=450, rely=0.2, relx=0)

upload_file_label = Label(text="No file selected")
upload_file_label.place(rely=0.82, relx=0.1)
upload_file_button = Button(text="Load", command=lambda: Load_excel_data())
upload_file_button.place(rely=0.9, relx=0.1)
browse_button = Button(text="Browse a file", command=lambda: File_dialog())
browse_button.place(rely=0.9, relx=0.2)


## Treeview Widget
tv1 = Treeview(frame)
tv1.place(relheight=1, relwidth=1)

treescrolly = Scrollbar(frame, orient="vertical", command=tv1.yview)
treescrollx = Scrollbar(frame, orient="horizontal", command=tv1.xview)
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
treescrollx.pack(side="bottom", fill="x")
treescrolly.pack(side="right", fill="y")

## Browse Function
def File_dialog():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetypes=(("xlsx files", "*.xlsx"), ("All Files", "*.*"), ("CSV Files","*.csv")))
    upload_file_label["text"] = filename


## Upload to data field function
def Load_excel_data():
    file_path = upload_file_label["text"]
    try:
        excel_filename = r"{}".format(file_path)
        if excel_filename[-4:] == ".csv":
            df = pd.read_csv(excel_filename)
        else:
            df = pd.read_excel(excel_filename)

    except ValueError:
        messagebox.showerror("Alert", "Invalid file chosen")
        return None
    except FileNotFoundError:
        messagebox.showerror("Alert", f"No such file as {file_path}")
        return None

    clear_data()
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
    return None

def clear_data():
    tv1.delete(*tv1.get_children())
    return None

window.mainloop()