import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox, filedialog
from pathlib import Path
import os
import sys
from convert import convert_to_py as to_py

def select_input():
    input_file = filedialog.askopenfilename(title="Select input file", filetypes = (('ipynb files', '*.ipynb'),('All files', '*.*')))
    if input_file != "":
        input_box.config(state='normal')
        input_box.delete(0, tk.END)
        input_box.insert(0, input_file)
        input_box.config(state='readonly')
        path = Path(input_file)
        k = path.parent.absolute()
        out_box.config(state='normal')
        out_box.delete(0, tk.END)
        out_box.insert(0, k)
        out_box.config(state='readonly')
        nm = path.name.split(".")
        nm = ".".join(nm[:-1])
        out_folder.config(state='normal')
        out_folder.delete(0, tk.END)
        out_folder.insert(0, nm)


def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected != "":
        out_box.config(state='normal')
        out_box.delete(0, tk.END)
        out_box.insert(0, folder_selected)
        out_box.config(state='readonly')

off_color = "red"
on_color = "green"
def on_check():   
    if mark_check.get() == 1:markdown_needed["fg"] = on_color     
    else:markdown_needed["fg"] = off_color

def on_check_1():   
    if mark_check_1.get() == 1:comm_needed["fg"] = on_color     
    else:comm_needed["fg"] = off_color

def convert():
    if input_box.get() == "" or out_box.get() == "" or out_folder.get() == "":
        messagebox.showerror("Error", "Please input all the fields")
        return
    if sys.platform.startswith("linux"):  
        if "/" in out_folder.get():
            messagebox.showerror("Error", "Please Enter a Valid Folder Structure")
            return
    elif sys.platform == "darwin":
        if "/" in out_folder.get() or ":" in out_folder.get():
            messagebox.showerror("Error", "Please Enter a Valid Folder Structure")
            return
    elif sys.platform == "win32":
        nac = [">","<",'\\',"/",":",'"',"|","?","*"]
        k = True
        for i in nac:
            if i in out_folder.get():
                k = False
        if k==False or out_folder.get() in ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"] or out_folder.get()[-1] == "." or out_folder.get()[-1] == " ":
            messagebox.showerror("Error", "Please Enter a Valid Folder Structure")
            return
    folder_path = out_box.get()
    markdown = False
    if mark_check.get() == 1:
        markdown = True
    py_filename = out_folder.get() + ".py"
    markdown_filename = out_folder.get() + ".md"
    py_path = os.path.join(folder_path, out_folder.get() , py_filename)
    markdown_path = os.path.join(folder_path, out_folder.get() , markdown_filename)
    folder_path = os.path.join(folder_path, out_folder.get())
    input_file = input_box.get()
    line_breaks = True
    if mark_check_1.get() == 0:
        line_breaks = False
    k = to_py(input_file, folder_path, py_path, markdown_path, markdown, line_breaks)
    if k == True:
        messagebox.showinfo("Success", "Conversion Successful")
    else:
        messagebox.showerror("Error", "Conversion Failed")


root = tk.Tk()
root.title("Ipynb to Py Converter")

if "nt" == os.name:
    root.iconbitmap("icon.ico")
root.geometry("400x400")
root.resizable(0, 0)


canvas = tk.Canvas(root, width=400, height=400, bg="#070769")
canvas.create_text(200, 30, fill="white", font="Arial 14 bold",text="Convert .ipynb to .py in few clicks!!")

canvas.create_text(75, 80, fill="white", font="Arial 12",text="Select .ipynb file")

input_box = tk.Entry(root, width=40, bg="#fff", text="", relief=tk.RAISED, font='Arial 12')
input_box.config(state='readonly')
input_box.place(x=20, y=100)


btn1 = tk.Button(canvas, text="Choose File", font='Arial 12', command=select_input, padx=2)
btn1.place(x=20, y=130)

canvas.create_text(89, 180, fill="white", font="Arial 12",text="Select Output Folder")

out_box = tk.Entry(root, width=40, bg="#fff", text="", relief=tk.RAISED, font='Arial 12')
out_box.config(state='readonly')
out_box.place(x=20, y=200)


btn2 = tk.Button(canvas, text="Choose Output Folder", font='Arial 12', command=select_folder, padx=2)
btn2.place(x=20, y=230)

canvas.create_text(102, 280, fill="white", font="Arial 12",text="Select Output File Name")

out_folder = tk.Entry(root, width=40, bg="#fff", text="", relief=tk.RAISED, font='Arial 12')
out_folder.config(state='readonly')
out_folder.place(x=20, y=300)

mark_check = tk.IntVar()
markdown_needed = tk.Checkbutton(root, text = "Include Markdown", variable=mark_check, font='Arial 14 bold',  bg='#070769', activebackground="#070769", fg=off_color, command=on_check)
markdown_needed.place(x=20, y=330)

mark_check_1 = tk.IntVar(value=1)
comm_needed = tk.Checkbutton(root, text = "Include Cell Breaks", variable=mark_check_1, font='Arial 14 bold',  bg='#070769', activebackground="#070769", fg=on_color, command=on_check_1)
comm_needed.place(x=20, y=360)

btn3 = tk.Button(canvas, text="Convert !!!", font='Arial 14 bold', command=convert, padx=2)
btn3.place(x=270, y=340)


canvas.pack(expand=True, fill=tk.BOTH)


root.mainloop()