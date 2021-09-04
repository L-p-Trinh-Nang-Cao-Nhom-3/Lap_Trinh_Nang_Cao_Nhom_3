import sqlite3
from tkinter import *

import pyodbc
from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk, messagebox

class productClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Supermarket Management System | Develop By: Group 3 ")
        self.root.geometry("1100x500+350+180")
        self.root.config(bg="#E0FFFF")
        self.root.resizable(width=False, height=False)
        self.root.focus_force()

        #============ variablr=============
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.var_name=StringVar()
        self.var_imprices=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()

        self.category_list = []
        self.supplier_list = []
        self.fetch_cat_sup()

        product_Frame=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=10,width=450,height=480)

        # =============Title============
        title = Label(product_Frame, text="Manager Product Details", font=("goudy old style", 18), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)

        #============ column 1==========
        lbl_category = Label(product_Frame, text="Category", font=("goudy old style", 18),bg="white").place(x=30,y=60)
        lbl_supplier = Label(product_Frame, text="Supplier", font=("goudy old style", 18),bg="white").place(x=30,y=110)
        lbl_name = Label(product_Frame, text="Name", font=("goudy old style", 18),bg="white").place(x=30,y=160)
        lbl_imprices = Label(product_Frame, text="Import Prices", font=("goudy old style", 18),bg="white").place(x=30,y=210)
        lbl_price = Label(product_Frame, text="Price", font=("goudy old style", 18),bg="white").place(x=30,y=260)
        lbl_qty = Label(product_Frame, text="Quantity", font=("goudy old style", 18),bg="white").place(x=30,y=310)
        lbl_status = Label(product_Frame, text="Status", font=("goudy old style", 18),bg="white").place(x=30,y=360)



        #============= column 2 ==================
        cmb_cat = ttk.Combobox(product_Frame,textvariable=self.var_cat,values=self.category_list,state='readonly', justify=CENTER,font=("goudy old style", 15))
        cmb_cat.place(x=170,y=60,width=200)
        cmb_cat.current(0)

        # ============= column 3 ==================
        cmb_sup = ttk.Combobox(product_Frame, textvariable=self.var_sup, values=self.supplier_list,state='readonly',justify=CENTER,font=("goudy old style", 15))
        cmb_sup.place(x=170, y=110, width=200)
        cmb_sup.current(0)

        txt_name = Entry(product_Frame, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place( x=170, y=160, width=200)
        txt_imprices = Entry(product_Frame, textvariable=self.var_imprices, font=("goudy old style", 15), bg="lightyellow").place( x=170, y=210, width=200)
        txt_price = Entry(product_Frame, textvariable=self.var_price, font=("goudy old style", 15), bg="lightyellow").place( x=170, y=260, width=200)
        txt_qty = Entry(product_Frame, textvariable=self.var_qty, font=("goudy old style", 15), bg="lightyellow").place( x=170, y=310, width=200)

        cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status, values=("Active","Inactive"), state='readonly',justify=CENTER, font=("goudy old style", 15))
        cmb_status.place(x=170, y=360, width=200)
        cmb_status.current(0)

        #================= button============
        self.btn_add = Button(self.root, text="Save", font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2",command=self.add )
        self.btn_add.place(x=20, y=420, width=100, height=40)
        self.btn_update = Button(self.root, text="Update", font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2",command=self.update)
        self.btn_update.place(x=130, y=420, width=100, height=40)
        self.btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2",command=self.delete)
        self.btn_delete.place(x=240, y=420, width=100, height=40)
        self.btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white",cursor="hand2",command=self.clear)
        self.btn_clear.place(x=350, y=420, width=100, height=40)

        #=============== search=================

        SearchFrame = LabelFrame(self.root, text="Search Product", bd=2, relief=RIDGE, bg="#E0FFFF")
        SearchFrame.place(x=480, y=10, width=600, height=80)

        # ======options========
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Select", "Category", "Supplier","Name"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15),bg='lightyellow').place(x=200, y=10)
        btn_search = Button(SearchFrame, text="Search", font=("goudy old style", 15), cursor="hand2", bg='#4caf50',fg="white", command=self.search).place(x=410, y=9, width=150, height=30)

        self.product_Frame = Frame(self.root, bd=3, relief=RIDGE)
        self.product_Frame.place(x=480, y=100,width=600,height=390)

        scrollx = Scrollbar(self.product_Frame, orient=HORIZONTAL)
        scrolly = Scrollbar(self.product_Frame, orient=VERTICAL)


        self.ProductTable = ttk.Treeview(self.product_Frame,columns=("pid", "category", "supplier", "name","imprices" ,"price", "qty", "status"),xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)

        self.ProductTable.heading("pid",text="P_ID")
        self.ProductTable.heading("category",text="Category")
        self.ProductTable.heading("supplier",text="Supplier")
        self.ProductTable.heading("name",text="Name")
        self.ProductTable.heading("imprices",text="Import Prices")
        self.ProductTable.heading("price",text="Price")
        self.ProductTable.heading("qty",text="QTY")
        self.ProductTable.heading("status",text="Status")

        self.ProductTable["show"] = 'headings'

        self.ProductTable.column("pid", width=70)
        self.ProductTable.column("category", width=120)
        self.ProductTable.column("supplier", width=150)
        self.ProductTable.column("name", width=150)
        self.ProductTable.column("imprices", width=150)
        self.ProductTable.column("price", width=80)
        self.ProductTable.column("qty", width=100)
        self.ProductTable.column("status", width=100)
        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()





    #==================================================================
    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_imprices.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()


# -----------------------------------------------------------------------
        # ---------------- Show-------------------------

    def show(self):
            con = sqlite3.connect(database="suppermarket.db")
            cur = con.cursor()
            try:
                cur.execute("select * from product")
                rows = cur.fetchall()
                self.ProductTable.delete(*self.ProductTable.get_children())
                for row in rows:
                    self.ProductTable.insert("", END, values=row)
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}")

    def get_data(self,ev):
        r=self.ProductTable.focus()
        content =self.ProductTable.item(r)
        row =content["values"]
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_imprices.set(row[4])
        self.var_price.set(row[5])
        self.var_qty.set(row[6])
        self.var_status.set(row[7])
#---------------- ADD-------------------------

    def fetch_cat_sup(self):
        self.category_list.append("Empty")
        self.supplier_list.append("Empty")
        con=sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            cur.execute("select name from category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.category_list[:]
                self.category_list.append("Select")
                for i in cat:
                    self.category_list.append(i[0])
            cur.execute("select name from supplier")
            sup = cur.fetchall()
            if len(sup)>0:
                del self.supplier_list[:]
                self.supplier_list.append("Select")
                for i in sup:
                    self.supplier_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def add(self):
        con=sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get()=="Select" or self.var_sup.get()=="Empty":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute("select * from product where name=? ",(self.var_name.get(),))
                row=cur.fetchone()
                if row !=None:
                    messagebox.showerror("Error", "Product already present, try different", parent=self.root)
                else:
                    cur.execute("INSERT INTO product (category,supplier,name,imprices,price,qty,status) values (?,?,?,?,?,?,?)",
                                (self.var_cat.get(),
                                 self.var_sup.get(),
                                 self.var_name.get(),
                                 self.var_imprices.get(),
                                 self.var_price.get(),
                                 self.var_qty.get(),
                                 self.var_status.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Product Added Successfuly",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}",parent=self.root)

#------------------------- update--------------------

    def update(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please select product from list", parent=self.root)
            else:
                cur.execute("select * from product where pid=? ", (self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Product ", parent=self.root)
                else:
                    cur.execute("update product set  category=?,supplier=?,name=?,imprices=?,price=?,qty=?,status=? where pid=? ",
                                (self.var_cat.get(),
                                 self.var_sup.get(),
                                 self.var_name.get(),
                                 self.var_imprices.get(),
                                 self.var_price.get(),
                                 self.var_qty.get(),
                                 self.var_status.get(),
                                 self.var_pid.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Employee Update Successfuly", parent=self.root)
                    self.show()
        except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    # ---------------- Delete-------------------------

    def delete(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error", "P_ID. should be required", parent=self.root)
            else:
                cur.execute("select * from product where pid=? ", (self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Please select Product from the list first", parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you readlly want to delete?", parent=self.root)
                    if op== True:
                        cur.execute('delete from product where pid=? ',(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Product deleted Successfuly",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")


    # ---------------- fetch_course-------------------------

    def search(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search By option",parent=self.root)
            elif self.var_searchby.get()=="":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
              cur.execute("select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
              rows=cur.fetchall()
              if len(rows)!= 0:
                  self.ProductTable.delete(*self.ProductTable.get_children())
                  for row in rows:
                      self.ProductTable.insert("", END, values=row)
              else:
                messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

if __name__=="__main__":
    root =Tk()
    obj=productClass(root)
    root.mainloop()