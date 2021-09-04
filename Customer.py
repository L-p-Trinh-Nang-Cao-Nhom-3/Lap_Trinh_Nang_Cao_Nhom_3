import sqlite3
from tkinter import *

import pyodbc
from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk, messagebox

class customerClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Supermarket Management System | Develop By: Group 3 ")
        self.root.geometry("1100x500+350+180")
        self.root.config(bg="#E0FFFF")
        self.root.resizable(width=False, height=False)
        self.root.focus_force()

        # ============ variablr=============
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_cus_id = StringVar()
        self.var_cus_name = StringVar()
        self.var_cus_date = StringVar()
        self.var_cus_contact = StringVar()
        self.var_cus_pro_name = StringVar()
        self.var_cus_number = StringVar()
        self.var_cus_price = StringVar()
        self.var_cus_total = StringVar()


        product_Frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=10, width=450, height=480)

        # =============Title============
        title = Label(product_Frame, text="Manager Customer Details", font=("goudy old style", 18), bg="#0f4d7d",fg="white").pack(side=TOP, fill=X)

        # ============ column 1==========
        lbl_cid = Label(product_Frame, text="Cus_ID", font=("goudy old style", 18), bg="white").place(x=30, y=60)
        lbl_name = Label(product_Frame, text="Name", font=("goudy old style", 18), bg="white").place(x=30,y=100)
        lbl_date = Label(product_Frame, text="Date", font=("goudy old style", 18), bg="white").place(x=30,y=140)
        lbl_phone = Label(product_Frame, text="Phone", font=("goudy old style", 18), bg="white").place(x=30, y=180)
        lbl_pro_name = Label(product_Frame, text="Product name", font=("goudy old style", 18), bg="white").place(x=30, y=220)
        lbl_number = Label(product_Frame, text="Number", font=("goudy old style", 18), bg="white").place(x=30, y=260)
        lbl_price = Label(product_Frame, text="Price", font=("goudy old style", 18), bg="white").place(x=30, y=300)
        lbl_total = Label(product_Frame, text="Total", font=("goudy old style", 18), bg="white").place(x=30, y=340)

        txt_cid=Entry(product_Frame, textvariable=self.var_cus_id,font=("goudy old style", 15),bg="lightyellow") .place(x=200, y=60, width=200)
        txt_name=Entry(product_Frame, textvariable=self.var_cus_name,font=("goudy old style", 15),bg="lightyellow").place(x=200, y=100, width=200)
        txt_date=Entry(product_Frame, textvariable=self.var_cus_date,font=("goudy old style", 15),bg="lightyellow").place(x=200, y=140, width=200)
        txt_phone=Entry(product_Frame, textvariable=self.var_cus_contact, font=("goudy old style", 15), bg="lightyellow").place(x=200, y=180, width=200)
        txt_pro_name=Entry(product_Frame, textvariable=self.var_cus_pro_name, font=("goudy old style", 15), bg="lightyellow").place(x=200, y=220, width=200)
        txt_number=Entry(product_Frame, textvariable=self.var_cus_number,font=("goudy old style", 15),bg="lightyellow").place( x=200, y=260, width=200)
        txt_price=Entry(product_Frame, textvariable=self.var_cus_price,font=("goudy old style", 15),bg="lightyellow").place(x=200, y=300, width=200)
        txt_total=Entry(product_Frame, textvariable=self.var_cus_total,font=("goudy old style", 15),bg="lightyellow").place(x=200, y=340, width=200)


        # ================= button============
        self.btn_add = Button(self.root, text="Save", font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=self.add)
        self.btn_add.place(x=20, y=420, width=100, height=40)
        self.btn_update = Button(self.root, text="Update", font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2", command=self.update)
        self.btn_update.place(x=130, y=420, width=100, height=40)
        self.btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2", command=self.delete)
        self.btn_delete.place(x=240, y=420, width=100, height=40)
        self.btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white",  cursor="hand2", command=self.clear)
        self.btn_clear.place(x=350, y=420, width=100, height=40)

        # =============== search=================

        SearchFrame = LabelFrame(self.root, text="Search Product", bd=2, relief=RIDGE, bg="#E0FFFF")
        SearchFrame.place(x=480, y=10, width=600, height=80)

        # ======options========
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby,values=("Select", "Name","Date"), state='readonly', justify=CENTER,font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg='lightyellow').place(x=200, y=10)
        btn_search = Button(SearchFrame, text="Search", font=("goudy old style", 15), cursor="hand2", bg='#4caf50',fg="white", command=self.search).place(x=410, y=9, width=150, height=30)

        self.customer_Frame = Frame(self.root, bd=3, relief=RIDGE)
        self.customer_Frame.place(x=480, y=100, width=600, height=390)
        scrollx = Scrollbar(self.customer_Frame, orient=HORIZONTAL)
        scrolly = Scrollbar(self.customer_Frame, orient=VERTICAL)

        self.CustomerTable = ttk.Treeview(self.customer_Frame,
                                         columns=("cid", "name","date", "phone","proname", "number", "price","total"),
                                         xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx.config(command=self.CustomerTable.xview)
        scrolly.config(command=self.CustomerTable.yview)

        self.CustomerTable.heading("cid", text="Cus_ID")
        self.CustomerTable.heading("name", text="Name")
        self.CustomerTable.heading("date", text="Date")
        self.CustomerTable.heading("phone", text="Phone")
        self.CustomerTable.heading("proname", text="Product name")
        self.CustomerTable.heading("number", text="Number")
        self.CustomerTable.heading("price", text="Price")
        self.CustomerTable.heading("total", text="Total")

        self.CustomerTable["show"] = 'headings'

        self.CustomerTable.column("cid", width=70)
        self.CustomerTable.column("name", width=120)
        self.CustomerTable.column("date", width=80)
        self.CustomerTable.column("phone", width=80)
        self.CustomerTable.column("proname", width=170)
        self.CustomerTable.column("number", width=80)
        self.CustomerTable.column("price", width=100)
        self.CustomerTable.column("total", width=100)
        self.CustomerTable.pack(fill=BOTH, expand=1)
        self.CustomerTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

        # ==================================================================

    def clear(self):
        self.var_cus_id.set("")
        self.var_cus_name.set("")
        self.var_cus_date.set("")
        self.var_cus_contact.set("")
        self.var_cus_pro_name.set("")
        self.var_cus_number.set("")
        self.var_cus_price.set("")
        self.var_cus_total.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

        # -----------------------------------------------------------------------
        # ---------------- Show-------------------------

    def show(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            cur.execute("select * from customer")
            rows = cur.fetchall()
            self.CustomerTable.delete(*self.CustomerTable.get_children())
            for row in rows:
                self.CustomerTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def get_data(self, ev):
        r = self.CustomerTable.focus()
        content = self.CustomerTable.item(r)
        row = content["values"]
        self.var_cus_id.set(row[0])
        self.var_cus_name.set(row[1])
        self.var_cus_date.set(row[2])
        self.var_cus_contact.set(row[3])
        self.var_cus_pro_name.set(row[4])
        self.var_cus_number.set(row[5])
        self.var_cus_price.set(row[6])
        self.var_cus_total.set(row[7])
        # ---------------- ADD-------------------------


    def add(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_cus_id.get()=="":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("select * from customer where name=? ", (self.var_cus_name.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Customer already present, try different", parent=self.root)
                else:
                    cur.execute("INSERT INTO customer (cid,name,date,phone,proname,number,price,total) values (?,?,?,?,?,?,?,?)",
                                (self.var_cus_id.get(),
                                 self.var_cus_name.get(),
                                 self.var_cus_date.get(),
                                 self.var_cus_contact.get(),
                                 self.var_cus_pro_name.get(),
                                 self.var_cus_number.get(),
                                 self.var_cus_price.get(),
                                 self.var_cus_total.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Customer Added Successfuly", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

        # ------------------------- update--------------------

    def update(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_cus_id.get() == "":
                messagebox.showerror("Error", "Please select Customer from list", parent=self.root)
            else:
                cur.execute("select * from customer where cid=? ", (self.var_cus_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Customer ", parent=self.root)
                else:
                    cur.execute("update customer set  name=?,date=?,phone=?,proname=?,number=?,price=?,total=?  where cid=? ",
                                (
                                 self.var_cus_name.get(),
                                 self.var_cus_date.get(),
                                 self.var_cus_contact.get(),
                                 self.var_cus_pro_name.get(),
                                 self.var_cus_number.get(),
                                 self.var_cus_price.get(),
                                 self.var_cus_total.get(),
                                 self.var_cus_id.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Customer Update Successfuly", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

        # ---------------- Delete-------------------------

    def delete(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_cus_id.get() == "":
                messagebox.showerror("Error", "P_ID. should be required", parent=self.root)
            else:
                cur.execute("select * from customer where cid=? ", (self.var_cus_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Please select Customer from the list first", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you readlly want to delete?", parent=self.root)
                    if op == True:
                        cur.execute('delete from customer where cid=? ', (self.var_cus_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Customer deleted Successfuly", parent=self.root)
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
                    "select * from customer where " + self.var_searchby.get() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.CustomerTable.delete(*self.CustomerTable.get_children())
                    for row in rows:
                        self.CustomerTable.insert("", END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")


if __name__=="__main__":
    root =Tk()
    obj=customerClass(root)
    root.mainloop()