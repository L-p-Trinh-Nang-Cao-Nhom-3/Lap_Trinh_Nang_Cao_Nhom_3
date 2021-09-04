import sqlite3
from tkinter import *

import pyodbc
from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk, messagebox

class positionClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Supermarket Management System | Develop By: Group 3 ")
        self.root.geometry("1100x500+350+180")
        self.root.config(bg="#E0FFFF")
        self.root.resizable(width=False, height=False)
        self.root.focus_force()
        #============ Variable ==========
        self.var_pos_id =StringVar()
        self.var_pos_name =StringVar()

        title = Label(self.root, text="Position Managment System",font=("times new roman", 40, "bold"), bg="#996600", fg="white",).place(x=0, y=0, relwidth=1, height=70)

        lbl_pos_id=Label(self.root,text="Position_ID",font=("goudy old style",25),bg="#E0FFFF").place(x=30,y=150)
        txt_pos_id=Entry(self.root,textvariable=self.var_pos_id,font=("times new roman",20,"bold"),bg="lightyellow").place(x=200,y=150,width=310,height=40)

        lbl_pos_name=Label(self.root,text="Name",font=("goudy old style",25),bg="#E0FFFF").place(x=30,y=250)
        txt_pos_name=Entry(self.root,textvariable=self.var_pos_name,font=("times new roman",20,"bold"),bg="lightyellow").place(x=200,y=250,width=310,height=40)

        self.btn_add = Button(self.root, text="Save", font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white",cursor="hand2", command=self.add)
        self.btn_add.place(x=200, y=315, width=70, height=35)
        self.btn_update = Button(self.root, text="Update", font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2", command=self.update)
        self.btn_update.place(x=280, y=315, width=70, height=35)
        self.btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15, "bold"), bg="#f44336",  fg="white", cursor="hand2", command=self.delete)
        self.btn_delete.place(x=360, y=315, width=70, height=35)
        self.btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2", command=self.clear)
        self.btn_clear.place(x=440, y=315, width=70, height=35)

        self.pos_Frame = Frame(self.root, bd=3, relief=RIDGE)
        self.pos_Frame.place(x=550, y=100, width=550, height=400)

        scrollx = Scrollbar(self.pos_Frame, orient=HORIZONTAL)
        scrolly = Scrollbar(self.pos_Frame, orient=VERTICAL)

        self.Position_Table = ttk.Treeview(self.pos_Frame,columns=("pid", "name"),xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx.config(command=self.Position_Table.xview)
        scrolly.config(command=self.Position_Table.yview)

        self.Position_Table.heading("pid", text="Position_ID")
        self.Position_Table.heading("name", text="Name")
        self.Position_Table["show"] = 'headings'
        self.Position_Table.column("pid", width=100)
        self.Position_Table.column("name", width=200)
        self.Position_Table.pack(fill=BOTH,expand=1)
        self.Position_Table.bind("<ButtonRelease-1>", self.get_data)
        self.show()

#============== function ==============
    def get_data(self, ev):
        r = self.Position_Table.focus()
        content = self.Position_Table.item(r)
        row = content["values"]
        self.var_pos_id.set(row[0])
        self.var_pos_name.set(row[1])

    def add(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_pos_id.get() == "":
                messagebox.showerror("Error", "Emp No Number should be required", parent=self.root)
            else:
                cur.execute("select * from position where pid=? ", (self.var_pos_id.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Thi Position ID already asigned, try diferent", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO position (pid, name) values (?,?)",
                        (self.var_pos_id.get(),
                         self.var_pos_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Position Added Successfuly", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

        # ------------------------- update--------------------

    def update(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_pos_id.get() == "":
                messagebox.showerror("Error", " Position ID must be required", parent=self.root)
            else:
                cur.execute("select * from position where pid=? ", (self.var_pos_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Position ID ", parent=self.root)
                else:
                    cur.execute("update position set  name=? where pid=? ",(self.var_pos_name.get(),self.var_pos_id.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Position Update Successfuly", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

        # ---------------- Delete-------------------------

    def delete(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_pos_id.get() == "":
                messagebox.showerror("Error", "Roll No. should be required", parent=self.root)
            else:
                cur.execute("select * from position where pid=? ", (self.var_pos_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Please select Position from the list first", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you readlly want to delete?", parent=self.root)
                    if op == True:
                        cur.execute('delete from position where pid=? ', (self.var_pos_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Position deleted Successfuly", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

        # ---------------- Show-------------------------

    def show(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            cur.execute("select * from position")
            rows = cur.fetchall()
            self.Position_Table.delete(*self.Position_Table.get_children())
            for row in rows:
                self.Position_Table.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def clear(self):
        self.var_pos_id.set("")
        self.var_pos_name.set("")
        self.show()






if __name__=="__main__":
    root =Tk()
    obj=positionClass(root)
    root.mainloop()