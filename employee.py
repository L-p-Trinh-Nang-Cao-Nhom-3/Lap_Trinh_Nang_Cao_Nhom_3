import sqlite3
from tkinter import *
import re
from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk, messagebox

class employeeClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Supermarket Management System | Develop By: Group 3 ")
        self.root.geometry("1100x500+350+180")
        self.root.config(bg="#E0FFFF")
        self.root.resizable(width=False, height=False)
        self.root.focus_force()

        #=======================
        #========= Variable============

        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()
        self.var_position=StringVar()
        self.var_salary=StringVar()

        self.position_list=[]
        self.fetch_pos()

        #=====SeachFrame========
        SearchFrame=LabelFrame(self.root,text="Search Employee",bd=2,relief=RIDGE,bg="#E0FFFF")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        #======options========
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Name","Email","Contact"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg='lightyellow').place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Search",font=("goudy old style",15),cursor="hand2",bg='#4caf50',fg="white",command=self.search).place(x=410,y=9,width=150,height=30)

        #=============Title============
        title=Label(self.root,text="Employee Details",font=("goudy old style",15),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1000)

        #======== content==========
        #---- row1-----
        lbl_empid = Label(self.root, text="Emp ID", font=("goudy old style", 15), bg="#E0FFFF").place( x=50, y=150)
        lbl_gender = Label(self.root, text="Gender", font=("goudy old style", 15), bg="#E0FFFF").place( x=350, y=150)
        lbl_contact = Label(self.root, text="Contract", font=("goudy old style", 15), bg="#E0FFFF").place( x=750, y=150)



        txt_empid = Entry(self.root, textvariable=self.var_emp_id, font=("goudy old style", 15), bg="lightyellow")
        txt_empid.place(x=150, y=150,width=180)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female","Other"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_gender.place(x=500, y=150,width=180)
        cmb_gender.current(0)
        txt_contact = Entry(self.root,textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow").place(x=850, y=150,width=180)
        # ---- row2-----
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15), bg="#E0FFFF").place(x=50, y=190)
        lbl_dob = Label(self.root, text="D.O.B", font=("goudy old style", 15), bg="#E0FFFF").place(x=350, y=190)
        lbl_doj = Label(self.root, text="D.O.J", font=("goudy old style", 15), bg="#E0FFFF").place(x=750, y=190)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15),bg="lightyellow").place(x=150, y=190, width=180)
        txt_dob =Entry(self.root, textvariable=self.var_dob,font=("goudy old style", 15),bg="lightyellow").place(x=500, y=190, width=180)
        txt_doj = Entry(self.root, textvariable=self.var_doj, font=("goudy old style", 15), bg="lightyellow").place(x=850, y=190, width=180)

        # ---- row3-----
        lbl_email = Label(self.root, text="Email", font=("goudy old style", 15), bg="#E0FFFF").place(x=50, y=230)
        lbl_pass = Label(self.root, text="Password", font=("goudy old style", 15), bg="#E0FFFF").place(x=350, y=230)
        lbl_utype = Label(self.root, text="User Type", font=("goudy old style", 15), bg="#E0FFFF").place(x=750, y=230)

        txt_email = Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15),bg="lightyellow").place(x=150, y=230, width=180)
        txt_pass = Entry(self.root, textvariable=self.var_pass, font=("goudy old style",15),bg="lightyellow").place(x=500,y=230,width=180)
        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_utype, values=("Admin", "Employee"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_utype.place(x=850, y=230, width=180)
        cmb_utype.current(0)

        lbl_position = Label(self.root, text="Position", font=("goudy old style", 15), bg="#E0FFFF").place(x=750, y=270)
        cmb_position = ttk.Combobox(self.root, textvariable=self.var_position, values=self.position_list, state='readonly',justify=CENTER, font=("goudy old style", 15))
        cmb_position.place(x=850, y=270, width=180)
        cmb_position.set("select")


        # ---- row4-----
        lbl_address = Label(self.root, text="Address", font=("goudy old style", 15), bg="#E0FFFF").place(x=50, y=270)
        lbl_salary = Label(self.root, text="Salary", font=("goudy old style", 15), bg="#E0FFFF").place(x=350, y=270)

        self.txt_address = Text(self.root,font=("goudy old style", 15), bg="lightyellow")
        self.txt_address.place( x=150, y=270, width=180,height=60)
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=("goudy old style", 15), bg="lightyellow").place(x=500,y=270, width=180)

        #============= button============
        self.btn_add = Button(self.root, text="Save", font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white",cursor="hand2",command=self.add)
        self.btn_add.place(x=500, y=305, width=110, height=28)
        self.btn_update = Button(self.root, text="Update", font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2",command=self.update)
        self.btn_update.place(x=620, y=305, width=110, height=28)
        self.btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15, "bold"), bg="#f44336",fg="white", cursor="hand2",command=self.delete)
        self.btn_delete.place(x=740, y=305, width=110, height=28)
        self.btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white",cursor="hand2",command=self.clear)
        self.btn_clear.place(x=860, y=305, width=110, height=28)

        #==========
        self.emp_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.emp_Frame.place(x=0, y=345,relwidth=1,height=150)

        scrollx = Scrollbar(self.emp_Frame, orient=HORIZONTAL)
        scrolly = Scrollbar(self.emp_Frame, orient=VERTICAL)
        self.EmployeeTable = ttk.Treeview(self.emp_Frame, columns=(
        "eid", "name", "email", "gender","contact", "dob", "doj", "password", "utype",'position', "address", "salary"),xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)


        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("eid", text="Emp No")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("dob", text="D.O.B")
        self.EmployeeTable.heading("doj", text="D.O.J")
        self.EmployeeTable.heading("password", text="password")
        self.EmployeeTable.heading("utype", text="User Type")
        self.EmployeeTable.heading("position", text="Position")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="salary")
        self.EmployeeTable["show"] = 'headings'
        self.EmployeeTable.column("eid", width=70)
        self.EmployeeTable.column("name", width=120)
        self.EmployeeTable.column("email", width=150)
        self.EmployeeTable.column("gender", width=70)
        self.EmployeeTable.column("contact", width=85)
        self.EmployeeTable.column("dob", width=90)
        self.EmployeeTable.column("doj", width=90)
        self.EmployeeTable.column("password", width=85)
        self.EmployeeTable.column("utype", width=80)
        self.EmployeeTable.column("position", width=80)
        self.EmployeeTable.column("address", width=100)
        self.EmployeeTable.column("salary", width=80)
        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()




#======================================================================

    def clear(self):
        self.show()
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.var_position.set("Select")
        self.txt_address.delete("1.0", END)
        self.var_salary.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

# -----------------------------------------------------------------------

    def get_data(self,ev):
        r=self.EmployeeTable.focus()
        content =self.EmployeeTable.item(r)
        row =content["values"]
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.var_position.set(row[9])
        self.txt_address.delete("1.0",END)
        self.txt_address.insert(END,row[10])
        self.var_salary.set(row[11])
 #=========== fetch =========
    def fetch_pos(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            cur.execute("select name from position ")
            rows = cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    self.position_list.append(row[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}",parent=self.root)
#---------------- ADD-------------------------


    def add(self):
        con=sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Emp No Number should be required",parent=self.root)
            else:
                cur.execute("select * from employee where eid=? ",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row !=None:
                    messagebox.showerror("Error", "Thi employee ID already asigned, try diferent", parent=self.root)
                else:
                    cur.execute("INSERT INTO employee (eid, name, email,gender,contact,dob,doj,password,utype,position,address,salary) values (?,?,?,?,?,?,?,?,?,?,?,?)",
                                (self.var_emp_id.get(),
                                 self.var_name.get(),
                                 self.var_email.get(),
                                 self.var_gender.get(),
                                 self.var_contact.get(),
                                 self.var_dob.get(),
                                 self.var_doj.get(),
                                 self.var_pass.get(),
                                 self.var_utype.get(),
                                 self.var_position.get(),
                                 self.txt_address.get("1.0",END),
                                 self.var_salary.get(),
                                ))
                    if  self.var_email.get().find("@")==-1 :
                        messagebox.showerror("Error", "Email does not exist", parent=self.root)
                    elif self.var_pass.get().find("@")==-1 and self.var_pass.get().find("$")==-1 and self.var_pass.get().find("%")==-1 and self.var_pass.get().find("#")==-1:
                            passwd=self.var_pass.get()
                            if len(passwd) < 6:
                                messagebox.showerror("Error", "Please enter password with at least one special character and more than 6 characters", parent=self.root)
                            elif len(passwd) > 20:
                                messagebox.showerror("Error", "Please enter a password with at least one special character and less than 20 characters", parent=self.root)
                    elif len(self.var_contact.get()) !=10 :
                        messagebox.showerror("Error", "Error phone contact", parent=self.root)
                    else:
                        con.commit()
                        messagebox.showinfo("Success", "Employee Added Successfuly", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

#------------------------- update--------------------

    def update(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("select * from employee where eid=? ", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Emplyee ID ", parent=self.root)
                else:
                    cur.execute("update employee set  name=?, email=?,gender=?,contact=?,dob=?,doj=?,password=?,utype=?,position=?,address=?,salary=? where eid=? ",
                                (
                                 self.var_name.get(),
                                 self.var_email.get(),
                                 self.var_gender.get(),
                                 self.var_contact.get(),
                                 self.var_dob.get(),
                                 self.var_doj.get(),
                                 self.var_pass.get(),
                                 self.var_utype.get(),
                                 self.var_position.get(),
                                 self.txt_address.get("1.0", END),
                                 self.var_salary.get(),
                                 self.var_emp_id.get()
                                 ))
                    if  self.var_email.get().find("@")==-1 :
                        messagebox.showerror("Error", "Email does not exist", parent=self.root)
                    elif self.var_pass.get().find("@")==-1 and self.var_pass.get().find("$")==-1 and self.var_pass.get().find("%")==-1 and self.var_pass.get().find("#")==-1:
                            passwd=self.var_pass.get()
                            if len(passwd) < 6:
                                messagebox.showerror("Error", "Please enter password with at least one special character and more than 6 characters", parent=self.root)
                            elif len(passwd) > 20:
                                messagebox.showerror("Error", "Please enter a password with at least one special character and less than 20 characters", parent=self.root)
                    elif len(self.var_contact.get()) !=10 :
                        messagebox.showerror("Error", "Error phone contact", parent=self.root)
                    else:
                        con.commit()
                        messagebox.showinfo("Success", "Employee Update Successfuly", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

# ---------------- Delete-------------------------

    def delete(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Roll No. should be required", parent=self.root)
            else:
                cur.execute("select * from employee where eid=? ", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Please select student from the list first", parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you readlly want to delete?", parent=self.root)
                    if op== True:
                        cur.execute('delete from employee where eid=? ',(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Employee deleted Successfuly",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

# ---------------- Show-------------------------


    def show(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            cur.execute("select * from employee")
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert("",END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

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
              cur.execute("select * from employee where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
              rows=cur.fetchall()
              if len(rows)!= 0:
                  self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                  for row in rows:
                      self.EmployeeTable.insert("", END, values=row)
              else:
                messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")






if __name__=="__main__":
    root =Tk()
    obj=employeeClass(root)
    root.mainloop()
