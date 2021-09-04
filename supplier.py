import sqlite3
from tkinter import *

from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk, messagebox


class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Supermarket Management System | Develop By: Group 3 ")
        self.root.geometry("1100x500+350+180")
        self.root.config(bg="#E0FFFF")
        self.root.resizable(width=False, height=False)
        self.root.focus_force()

        # ========= Variable============

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_sup_invoice=StringVar()
        self.var_name=StringVar()
        self.var_contact =StringVar()
        
       


        # ======options========
        lbl_search =Label(self.root,text="Invoice No." ,font=("goudy old style", 15),bg="#E0FFFF")
        lbl_search.place(x=670, y=80)

        txt_search = Entry(self.root, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg='lightyellow').place(x=780, y=80,width=160)
        btn_search = Button(self.root, text="Search", font=("goudy old style", 15), cursor="hand2", bg='#4caf50', fg="white", command=self.search).place(x=960, y=79, width=100, height=28)


        # =============Title============
        title = Label(self.root, text="Supplier Details", font=("goudy old style", 15), bg="#0f4d7d", fg="white").place( x=50, y=10, width=1000,height=40)

        # ======== content==========
        # ---- row1-----
        lbl_supplier_invoice = Label(self.root,text="Invoice No.", font=("goudy old style", 15), bg="#E0FFFF").place(x=50, y=80)
        txt_supplier_invoice = Entry(self.root,textvariable=self.var_sup_invoice, font=("goudy old style", 15), bg="lightyellow").place(x=180, y=80, width=180)

        # ---- row2-----
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15), bg="#E0FFFF").place(x=50, y=120)
        txt_name=Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(x=180, y=120, width=180)
        # ---- row3-----
        lbl_contact = Label(self.root, text="Contract", font=("goudy old style", 15), bg="#E0FFFF").place( x=50, y=160)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow").place(x=180, y=160, width=180)
           
        # ---- row4-----
        lbl_desc = Label(self.root, text="Description", font=("goudy old style", 15), bg="#E0FFFF").place(x=50, y=200)
        self.txt_desc = Text(self.root,font=("goudy old style", 15), bg="lightyellow")
        self.txt_desc.place( x=180, y=200, width=470,height=120)

        # ============= button============
        self.btn_add = Button(self.root, text="Save", font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white",  cursor="hand2", command=self.add)                          
        self.btn_add.place(x=180, y=370, width=110, height=35)
        self.btn_update = Button(self.root, text="Update", font=("goudy old style", 15, "bold"), bg="#4caf50",fg="white", cursor="hand2", command=self.update)                               
        self.btn_update.place(x=300, y=370, width=110, height=35)
        self.btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15, "bold"), bg="#f44336",fg="white", cursor="hand2", command=self.delete)                              
        self.btn_delete.place(x=420, y=370, width=110, height=35)
        self.btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white",cursor="hand2", command=self.clear)                      
        self.btn_clear.place(x=540, y=370, width=110, height=35)

        # ==========
        self.emp_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.emp_Frame.place(x=670, y=120, width=430, height=285)

        scrollx = Scrollbar(self.emp_Frame, orient=HORIZONTAL)
        scrolly = Scrollbar(self.emp_Frame, orient=VERTICAL)
        self.supplierTable = ttk.Treeview(self.emp_Frame, columns=( "invoice", "name", "contact", "desc"),xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice", text="Invoice No")
        self.supplierTable.heading("name", text="Name")
        self.supplierTable.heading("contact", text="Contact")
        self.supplierTable.heading("desc", text="Description")
        self.supplierTable["show"] = 'headings'
        self.supplierTable.column("invoice", width=70)
        self.supplierTable.column("name", width=150)
        self.supplierTable.column("contact", width=85)
        self.supplierTable.column("desc", width=150)
    
        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

        # ======================================================================

    def clear(self):
        self.show()
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")      
        self.txt_desc.delete("1.0", END)
        self.var_searchtxt.set("")
        self.show()

        # -----------------------------------------------------------------------

    def get_data(self, ev):
        r = self.supplierTable.focus()
        content = self.supplierTable.item(r)
        row = content["values"]
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])     
        self.txt_desc.delete("1.0", END)
        self.txt_desc.insert(END, row[3])
        # ---------------- ADD-------------------------

    def add(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice must be required", parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=? ", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Invoice no. already asigned, try diferent", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO supplier (invoice, name, contact,desc) values (?,?,?,?)",
                        (self.var_sup_invoice.get(),
                         self.var_name.get(),                    
                         self.var_contact.get(),                       
                         self.txt_desc.get("1.0", END),                        
                         ))
                    if len(self.var_contact.get()) != 10:
                         messagebox.showerror("Error", "Error phone contact", parent=self.root)
                    else:
                        con.commit()
                        messagebox.showinfo("Success", "Supplier Added Successfuly", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

        # ------------------------- update--------------------

    def update(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() =="":
                messagebox.showerror("Error", "Invoice no. must be required", parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=? ", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Invoice No. ", parent=self.root)
                else:
                    cur.execute( "update supplier set  name=?,contact=?,desc=? where invoice=? ",
                                 (self.var_name.get(),
                                  self.var_contact.get(),
                                  self.txt_desc.get("1.0", END),
                                  self.var_sup_invoice.get(),))
                    if len(self.var_contact.get()) != 10:
                         messagebox.showerror("Error", "Error phone contact", parent=self.root)
                    else:
                        con.commit()
                        messagebox.showinfo("Success", "Supplier Update Successfuly", parent=self.root)
                        self.show()
        except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}")


        # ---------------- Delete-------------------------

    def delete(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. should be required", parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=? ", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Please select student from the list first", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you readlly want to delete?", parent=self.root)
                    if op == True:
                        cur.execute('delete from supplier where invoice=? ', (self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Supplier deleted Successfuly", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

        # ---------------- Show-------------------------

    def show(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            cur.execute("select * from supplier")
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

        # ---------------- fetch_course-------------------------

    def search(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Select Search By option", parent=self.root)
            else:
                cur.execute( "select * from supplier where invoice=?",(self.var_searchtxt.get(),))
                row= cur.fetchone()
                if row!=None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert("", END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")


if __name__=="__main__":
    root =Tk()
    obj=supplierClass(root)
    root.mainloop()