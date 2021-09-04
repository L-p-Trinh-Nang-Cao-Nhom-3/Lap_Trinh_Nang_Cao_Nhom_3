import sqlite3
from tkinter import *

from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk, messagebox
import os


class bill_Class:
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
        title = Label(self.root, text="View Bill", font=("times new roman", 30), bd=3, bg="#184a45", fg="white").pack(side=TOP, fill=X, padx=10, pady=20)


        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_bill_id = StringVar()
        self.var_name = StringVar()
        self.var_name_emp = StringVar()
        self.var_name_cus = StringVar()
        self.var_date = StringVar()


        lbl_name = Label(self.root, text="Name", font=("goudy old style", 20), bg="#E0FFFF").place(x=20, y=120)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place( x=200, y=120, width=310, height=30)

        lbl_name_emp = Label(self.root, text="Name employee", font=("goudy old style", 20), bg="#E0FFFF").place(x=20, y=180)
        txt_name_emp = Entry(self.root, textvariable=self.var_name_emp, font=("goudy old style", 15), bg="lightyellow").place(x=200, y=180, width=310, height=30)

        lbl_name_cus = Label(self.root, text="Name customer", font=("goudy old style", 20), bg="#E0FFFF").place(x=20, y=240)
        lbl_name_cus = Entry(self.root, textvariable=self.var_name_cus, font=("goudy old style", 15), bg="lightyellow").place(x=200, y=240, width=310, height=30)

        lbl_date = Label(self.root, text="Date", font=("goudy old style", 20), bg="#E0FFFF").place(x=20, y=300)
        txt_date = Entry(self.root, textvariable=self.var_date, font=("goudy old style", 15), bg="lightyellow").place(x=200, y=300, width=310, height=30)

        self.btn_add = Button(self.root, text="Add", font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2",command=self.add)
        self.btn_add.place(x=200, y=360, width=70, height=35)
        self.btn_update = Button(self.root, text="Update", font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2",command=self.update)
        self.btn_update.place(x=280, y=360, width=70, height=35)
        self.btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2",command=self.delete)
        self.btn_delete.place(x=360, y=360, width=70, height=35)
        self.btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2",command=self.clear)
        self.btn_clear.place(x=440, y=360, width=70, height=35)

        SearchFrame = LabelFrame(self.root, text="Search Spending Bill", bd=2, relief=RIDGE, bg="#E0FFFF")
        SearchFrame.place(x=552, y=80, width=470, height=60)

        # ======options========
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby,values=("Select", "bill_id", "Date"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=5, width=150)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg='lightyellow').place(x=170, y=5, width=170)
        btn_search = Button(SearchFrame, text="Search", font=("goudy old style", 15), cursor="hand2", bg='#4caf50',fg="white",command=self.search).place(x=350, y=4, width=100, height=30)

        bill_Frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        bill_Frame.place(x=550, y=140, width=530, height=350)

        scrollx = Scrollbar(bill_Frame, orient=HORIZONTAL)
        scrolly = Scrollbar(bill_Frame, orient=VERTICAL)
        self.Bill_Table = ttk.Treeview(bill_Frame, columns=("bill_id", "name", "name_emp", "name_cus","date"), xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)


        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.Bill_Table.xview)
        scrolly.config(command=self.Bill_Table.yview)

        self.Bill_Table.heading("bill_id", text="Bill_id")
        self.Bill_Table.heading("name", text="Name")
        self.Bill_Table.heading("name_emp", text="Name_emp")
        self.Bill_Table.heading("name_cus", text="Name_cus")
        self.Bill_Table.heading("date", text="Date")
        self.Bill_Table["show"] = 'headings'
        self.Bill_Table.column("bill_id", width=50)
        self.Bill_Table.column("name", width=100)
        self.Bill_Table.column("name_emp", width=100)
        self.Bill_Table.column("name_cus", width=100)
        self.Bill_Table.column("date", width=70)
        self.Bill_Table.pack(fill=BOTH, expand=1)
        self.Bill_Table.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    # ==================================================================
    def clear(self):
            self.show()
            self.var_bill_id.set("")
            self.var_name.set("")
            self.var_name_emp.set("")
            self.var_name_cus.set("")
            self.var_date.set("")
            self.show()

    # -----------------------------------------------------------------------
    # ---------------- Show-------------------------

    def show(self):
            con = sqlite3.connect(database="suppermarket.db")
            cur = con.cursor()
            try:
                cur.execute("select * from bill")
                rows = cur.fetchall()
                self.Bill_Table.delete(*self.Bill_Table.get_children())
                for row in rows:
                    self.Bill_Table.insert("", END, values=row)
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}")

    def get_data(self, ev):
            r = self.Bill_Table.focus()
            content = self.Bill_Table.item(r)
            row = content["values"]
            self.var_bill_id.set(row[0])
            self.var_name.set(row[1])
            self.var_name_emp.set(row[2])
            self.var_name_cus.set(row[3])
            self.var_date.set(row[4])


    # ---------------- ADD-------------------------


    def add(self):
            con = sqlite3.connect(database="suppermarket.db")
            cur = con.cursor()
            try:
                if self.var_name.get() == "":
                    messagebox.showerror("Error", "All fields are required", parent=self.root)
                else:
                    cur.execute("select * from bill where name=? ", (self.var_name.get(),))
                    row = cur.fetchone()
                    if row != None:
                        messagebox.showerror("Error", "Thi Bill name already asigned, try diferent", parent=self.root)
                    else:
                        cur.execute("INSERT INTO bill (name,name_emp,name_cus,date) values (?,?,?,?)",
                                    (self.var_name.get(),
                                     self.var_name_emp.get(),
                                     self.var_name_cus.get(),
                                     self.var_date.get(),))

                        con.commit()
                    messagebox.showinfo("Success", "Bill Added Successfuly", parent=self.root)
                    self.show()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

        # ------------------------- update--------------------

    def update(self):
            con = sqlite3.connect(database="suppermarket.db")
            cur = con.cursor()
            try:
                if self.var_name.get() == "":
                    messagebox.showerror("Error", "Please select Bill from list", parent=self.root)
                else:
                    cur.execute("select * from bill where name =? ", (self.var_name.get(),))
                    row = cur.fetchone()
                    if row == None:
                        messagebox.showerror("Error", "Invalid Bill ", parent=self.root)
                    else:
                        cur.execute("update bill set name_emp=?,name_cus=?,date=? where name=? ",
                                    (
                                     self.var_name_emp.get(),
                                     self.var_name_cus.get(),
                                     self.var_date.get(),
                                     self.var_name.get(),))
                        con.commit()
                        messagebox.showinfo("Success", "Bill Update Successfuly", parent=self.root)
                        self.show()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

        # ---------------- Delete-------------------------

    def delete(self):
            con = sqlite3.connect(database="suppermarket.db")
            cur = con.cursor()
            try:
                if self.var_name.get() == "":
                    messagebox.showerror("Error", "Name should be required", parent=self.root)
                else:
                    cur.execute("select * from bill where name=? ", (self.var_name.get(),))
                    row = cur.fetchone()
                    if row == None:
                        messagebox.showerror("Error", "Please select Bill from the list first", parent=self.root)
                    else:
                        op = messagebox.askyesno("Confirm", "Do you readlly want to delete?", parent=self.root)
                        if op == True:
                            cur.execute('delete from bill where name=? ', (self.var_name.get(),))
                            con.commit()
                            messagebox.showinfo("Delete", "Bill deleted Successfuly", parent=self.root)
                            self.clear()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}")

        # ---------------- fetch_course-------------------------

    def search(self):
            con = sqlite3.connect(database="suppermarket.db")
            cur = con.cursor()
            try:
                if self.var_searchby.get() == "Select":
                    messagebox.showerror("Error", "Select Search By option", parent=self.root)
                elif self.var_searchby.get() == "":
                    messagebox.showerror("Error", "Search input should be required", parent=self.root)
                else:
                    cur.execute(
                        "select * from bill where " + self.var_searchby.get() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                    rows = cur.fetchall()
                    if len(rows) != 0:
                        self.Bill_Table.delete(*self.Bill_Table.get_children())
                        for row in rows:
                            self.Bill_Table.insert("", END, values=row)
                    else:
                        messagebox.showerror("Error", "No record found", parent=self.root)
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}")


if __name__ == "__main__":
    root = Tk()
    obj = bill_Class(root)
    root.mainloop()

