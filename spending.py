import sqlite3
from tkinter import *

from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk, messagebox

class spendClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Supermarket Management System | Develop By: Group 3 ")
        self.root.geometry("1100x500+350+180")
        self.root.config(bg="#E0FFFF")
        self.root.resizable(width=False, height=False)
        self.root.focus_force()

        #====== Variable=============
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_sid = StringVar()
        self.var_name = StringVar()
        self.var_date = StringVar()
        self.var_spreason = StringVar()
        self.var_spprice = StringVar()
        self.var_desc = StringVar()

        self.employee_list =[]
        self.fetch_employee()


        # =============Title============
        title = Label(self.root, text="Spending Details", font=("goudy old style", 20), bg="#0f4d7d", fg="white").place(
            x=0, y=10, width=1100)

        lbl_sib=Label(self.root,text="Spend ID",font=("goudy old style", 20),bg="#E0FFFF").place(x=20,y=80)
        txt_sib=Entry(self.root,textvariable=self.var_sid,font=("goudy old style", 15),bg="lightyellow").place(x=200,y=80,width=200,height=30)

        lbl_spperson = Label(self.root, text="Person Spend", font=("goudy old style", 20), bg="#E0FFFF").place(x=20, y=140)
        cmb_spperson = ttk.Combobox(self.root, textvariable=self.var_spreason, values=self.employee_list,state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_spperson.place(x=200, y=140, width=200, height=30)
        cmb_spperson.set("select")

        lbl_date = Label(self.root, text="Date", font=("goudy old style", 20), bg="#E0FFFF").place(x=20, y=200)
        txt_date = Entry(self.root, textvariable=self.var_date, font=("goudy old style", 15), bg="lightyellow").place(
            x=200, y=200, width=200, height=30)

        lbl_price = Label(self.root, text="Price", font=("goudy old style", 20), bg="#E0FFFF").place(x=20, y=260)
        txt_price = Entry(self.root, textvariable=self.var_spprice, font=("goudy old style", 15),bg="lightyellow").place(x=200, y=260, width=200, height=30)

        lbl_spname = Label(self.root, text="Spending Name", font=("goudy old style", 20), bg="#E0FFFF").place(x=450, y=80)
        txt_spname = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place( x=640, y=80, width=350, height=30)

        lbl_desc = Label(self.root, text="Description", font=("goudy old style", 20), bg="#E0FFFF").place(x=450, y=140)
        self.txt_desc = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_desc.place(x=640, y=140, width=350, height=70)

        self.btn_add = Button(self.root, text="Add", font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white",cursor="hand2",command=self.add)
        self.btn_add.place(x=600, y=220, width=110, height=35)
        self.btn_update = Button(self.root, text="Update", font=("goudy old style", 15, "bold"), bg="#4caf50",  fg="white", cursor="hand2",command=self.update)
        self.btn_update.place(x=720, y=220, width=110, height=35)
        self.btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2",command=self.delete)
        self.btn_delete.place(x=840, y=220, width=110, height=35)
        self.btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2",command=self.clear)
        self.btn_clear.place(x=960, y=220, width=110, height=35)


        SearchFrame = LabelFrame(self.root, text="Search Spending Bill", bd=2, relief=RIDGE, bg="#E0FFFF")
        SearchFrame.place(x=600, y=270, width=470, height=60)


        # ======options========
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Select","sid", "person", "Date"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=5, width=150)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg='lightyellow').place(x=170, y=5,width=170)
        btn_search = Button(SearchFrame, text="Search", font=("goudy old style", 15), cursor="hand2", bg='#4caf50',fg="white",command=self.search).place(x=350, y=4, width=100, height=30)

        #=============================== Table =====================
        self.spend_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.spend_Frame.place(x=0, y=345, relwidth=1, height=150)

        scrollx = Scrollbar(self.spend_Frame, orient=HORIZONTAL)
        scrolly = Scrollbar(self.spend_Frame, orient=VERTICAL)
        self.Spend_Table = ttk.Treeview(self.spend_Frame, columns=("sid", "person", "date", "name", "price", "desc" ), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)



        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.Spend_Table.xview)
        scrolly.config(command=self.Spend_Table.yview)

        self.Spend_Table.heading("sid", text="Spend ID")
        self.Spend_Table.heading("person", text="Person Spend")
        self.Spend_Table.heading("date", text="Date")
        self.Spend_Table.heading("name", text="Spending Name")
        self.Spend_Table.heading("price", text="Price")
        self.Spend_Table.heading("desc", text="Description")

        self.Spend_Table["show"] = 'headings'
        self.Spend_Table.column("sid", width=70)
        self.Spend_Table.column("person", width=120)
        self.Spend_Table.column("date", width=80)
        self.Spend_Table.column("name", width=120)
        self.Spend_Table.column("price", width=85)
        self.Spend_Table.column("desc", width=150)

        self.Spend_Table.pack(fill=BOTH, expand=1)
        self.Spend_Table.bind("<ButtonRelease-1>", self.get_data)
        self.show()
# ==================================================================
    def clear(self):
        self.show()
        self.var_sid.set("")
        self.var_spreason.set("")
        self.var_date.set("")
        self.var_name.set("")
        self.var_spprice.set("")
        self.txt_desc.delete("1.0", END)
        self.var_searchtxt.set("")
        self.show()

    # -----------------------------------------------------------------------
    # ---------------- Show-------------------------


    def show(self):
            con = sqlite3.connect(database="suppermarket.db")
            cur = con.cursor()
            try:
                cur.execute("select * from spend")
                rows = cur.fetchall()
                self.Spend_Table.delete(*self.Spend_Table.get_children())
                for row in rows:
                    self.Spend_Table.insert("", END, values=row)
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}")

    def get_data(self,ev):
        r=self.Spend_Table.focus()
        content =self.Spend_Table.item(r)
        row =content["values"]
        self.var_sid.set(row[0])
        self.var_spreason.set(row[1])
        self.var_date.set(row[2])
        self.var_name.set(row[3])
        self.var_spprice.set(row[4])
        self.txt_desc.delete("1.0", END)
        self.txt_desc.insert(END, row[5])
#---------------- ADD-------------------------

    def fetch_employee(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            cur.execute("select name from employee ")
            rows = cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    self.employee_list.append(row[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
    def add(self):
        con=sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_sid.get()=="" :
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute("select * from spend where sid=? ", (self.var_sid.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Thi Position ID already asigned, try diferent", parent=self.root)
                else:
                    cur.execute("INSERT INTO spend (sid,person,date,name,price, desc) values (?,?,?,?,?,?)",
                                (self.var_sid.get(),
                                 self.var_spreason.get(),
                                 self.var_date.get(),
                                 self.var_name.get(),
                                 self.var_spprice.get(),
                                 self.txt_desc.get("1.0", END),))
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
            if self.var_sid.get() == "":
                messagebox.showerror("Error", "Please select product from list", parent=self.root)
            else:
                cur.execute("select * from spend where sid=? ", (self.var_sid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Product ", parent=self.root)
                else:
                    cur.execute("update spend set person=?,date=?,name=?,price=?, desc=? where sid=? ",
                                (
                                 self.var_spreason.get(),
                                 self.var_date.get(),
                                 self.var_name.get(),
                                 self.var_spprice.get(),
                                 self.txt_desc.get("1.0", END),
                                 self.var_sid.get(),))
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
            if self.var_sid.get()=="":
                messagebox.showerror("Error", "P_ID. should be required", parent=self.root)
            else:
                cur.execute("select * from spend where sid=? ", (self.var_sid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Please select Product from the list first", parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you readlly want to delete?", parent=self.root)
                    if op== True:
                        cur.execute('delete from spend where sid=? ',(self.var_sid.get(),))
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
              cur.execute("select * from spend where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
              rows=cur.fetchall()
              if len(rows)!= 0:
                  self.Spend_Table.delete(*self.Spend_Table.get_children())
                  for row in rows:
                      self.Spend_Table.insert("", END, values=row)
              else:
                messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")



if __name__=="__main__":
    root =Tk()
    obj=spendClass(root)
    root.mainloop()
