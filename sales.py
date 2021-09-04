import sqlite3
from tkinter import *

from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk, messagebox
import os


class sale_Class:
    def __init__(self, root):
        self.root = root
        self.root.title("Supermarket Management System | Develop By: Group 3 ")
        self.root.geometry("1100x500+350+180")
        self.root.config(bg="#E0FFFF")
        self.root.resizable(width=False, height=False)
        self.root.focus_force()

        # ============== Variable =============
        self.bill_list=[]
        self.var_invoice = StringVar()

        # =============Title============
        title = Label(self.root, text="View Customer Bill", font=("times new roman", 30), bd=3, bg="#184a45",
                      fg="white").pack(side=TOP, fill=X, padx=10, pady=20)

        lbl_invoice = Label(self.root, text="Invoice No.", font=("Elephant", 15), bg="#E0FFFF").place(x=150, y=100)
        txt_invoice = Entry(self.root, textvariable=self.var_invoice, font=("goudy old style", 15),
                            bg="lightyellow").place(x=270, y=100, width=180, height=28)

        btn_search = Button(self.root, text="search",command=self.seacrh,font=("times new roman", 15, "bold"), bg="#2196f3", fg="white",
                            cursor="hand2").place(x=460, y=100, width=120, height=28)
        btn_clear = Button(self.root,command=self.clear,text="Clear", font=("times new roman", 15, "bold"), bg="lightgray",
                           cursor="hand2").place(x=590, y=100, width=120, height=28)

        # =========== Bill List ===========
        sales_Frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_Frame.place(x=150, y=140, width=180, height=330)

        scrolly = Scrollbar(sales_Frame, orient=VERTICAL)
        self.sales_list = Listbox(sales_Frame, font=("goudy old style", 15), bg="white", yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.sales_list.yview)
        self.sales_list.bind("<ButtonRelease-1>", self.get_data)
        self.sales_list.pack(fill=BOTH, expand=1)

        # =========== Bill area ===========
        bill_Frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_Frame.place(x=320, y=140,  width=500, height=330)

        # =============Title============
        lbl_title2 = Label(bill_Frame, text="Customer Bill Area", font=("times new roman", 20), bd=3, bg="orange",
                           fg="white").pack(side=TOP, fill=X)

        scrolly2 = Scrollbar(bill_Frame, orient=VERTICAL)
        self.bill_eara = Text(bill_Frame, bg="lightyellow", yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_eara.yview)
        self.bill_eara.pack(fill=BOTH, expand=1)

        # ============= image==================



        self.show()

    # ============================================================
    def show(self):
        del self.bill_list[:]
        self.sales_list.delete(0, END)
        for i in os.listdir('bill'):
            if i.split('.')[-1] =='txt':
                self.sales_list.insert(END,i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self,ev):
        index_=self.sales_list.curselection()
        file_name=self.sales_list.get(index_)
        self.bill_eara.delete('1.0', END)
        fp=open(f'bill/{file_name}','r',encoding="utf-8")
        for i in fp:
            self.bill_eara.insert(END,i)
        fp.close()

    def seacrh(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice no. should be required",parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                fp = open(f'bill/{self.var_invoice.get()}.txt','r',encoding="utf-8")
                self.bill_eara.delete('1.0',END)
                for i in fp:
                    self.bill_eara.insert(END, i)
                fp.close()
            else:
                messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)

    def clear(self):
        self.show()
        self.bill_eara.delete('1.0',END)




if __name__ == "__main__":
    root = Tk()
    obj = sale_Class(root)
    root.mainloop()
