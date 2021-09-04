import sqlite3
from tkinter import *

import pyodbc
from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk, messagebox


class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Supermarket Management System | Develop By: Group 3 ")
        self.root.geometry("1100x500+350+180")
        self.root.config(bg="#E0FFFF")
        self.root.resizable(width=False, height=False)
        self.root.focus_force()
    #=============variable==============
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
    #============= image ==========
        # self.im1=Image.open("../QuanLyHocSinh/images/cl_new.png")
        # self.im1=self.im1.resize((500,250),Image.ANTIALIAS)
        # self.im1=ImageTk.PhotoImage(self.im1)
        #
        # self.lbl_im1=Label(self.root,image=self.im1,bd=2,relief=RAISED)
        # self.lbl_im1.place(x=50,y=220)
        #
        # self.im2 = Image.open("../QuanLyHocSinh/images/cl.png")
        # self.im2 = self.im2.resize((500, 250), Image.ANTIALIAS)
        # self.im2 = ImageTk.PhotoImage(self.im2)
        # self.lbl_im2 = Label(self.root, image=self.im2, bd=2, relief=RAISED)
        # self.lbl_im2.place(x=580, y=220)

    #=============Title============
        lbl_title=Label(self.root,text="Manager Product Category",font=("goudy old style",25),bd=3, relief=RIDGE,bg="#184a45",fg="white").pack(side=TOP,fill=X,padx=10,pady=20)

        lbl_cateID = Label(self.root, text="Category ID", font=("goudy old style", 25), bg="#E0FFFF").place(x=50, y=100)
        txt_cateID = Entry(self.root ,textvariable=self.var_cat_id, font=("goudy old style", 18), bg="lightyellow").place( x=50, y=170, width=170,height=40)

        lbl_name=Label(self.root,text="Category Name",font=("goudy old style",30),bg="#E0FFFF").place(x=350,y=100)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",18),bg="lightyellow").place(x=350,y=170, width=300,height=40)

        btn_add=Button(self.root,text="ADD",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=350,y=240,width=65,height=40)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=430,y=240,width=65,height=40)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="red",fg="white",cursor="hand2").place(x=510,y=240,width=65,height=40)
        self.btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white",cursor="hand2",command=self.clear).place(x=590,y=240,width=65,height=40)


        # ========== category details========
        cat_Frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_Frame.place(x=720, y=100, width=380,height=390)

        scrollx = Scrollbar(cat_Frame, orient=HORIZONTAL)
        scrolly = Scrollbar(cat_Frame, orient=VERTICAL)
        self.category_Table = ttk.Treeview(cat_Frame, columns=("cid","name"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.category_Table.xview)
        scrolly.config(command=self.category_Table.yview)

        self.category_Table.heading("cid", text="CateID")
        self.category_Table.heading("name", text="Name")

        self.category_Table["show"] = 'headings'

        self.category_Table.column("cid", width=150)
        self.category_Table.column("name", width=200)
        self.category_Table.pack(fill=BOTH, expand=1)
        self.category_Table.bind("<ButtonRelease-1>", self.get_data)
        self.show()

        #========================================

    def get_data(self, ev):
        r = self.category_Table.focus()
        content = (self.category_Table.item(r))
        row = content["values"]
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    def add(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_cat_id.get()==""or self.var_name.get()=="":
                messagebox.showerror("Error", "Category name should be required", parent=self.root)
            else:
                cur.execute("select * from category where cid=? ",(self.var_cat_id.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Category already precent, try different", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO category (cid,name) values(?,?)",(self.var_cat_id.get(),self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Category Added Successfuly", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def update(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Please select Category from list", parent=self.root)
            else:
                cur.execute("select * from category where cid=? ", (self.var_cat_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Category ", parent=self.root)
                else:
                    cur.execute("update category set  name=?  where cid=? ",
                                (self.var_name.get(),
                                self.var_cat_id.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Category Update Successfuly", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)


    def delete(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Category ID should be required", parent=self.root)
            else:
                cur.execute("select * from category where cid=? ", (self.var_cat_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Please select Category Name from the list first", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you readlly want to delete?", parent=self.root)
                    if op == True:
                        cur.execute('delete from category where cid=? ', (self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Category Name deleted Successfuly", parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")


    def show(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            cur.execute("select * from category")
            rows = cur.fetchall()
            self.category_Table.delete(*self.category_Table.get_children())
            for row in rows:
                self.category_Table.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def clear(self):
        self.show()
        self.var_cat_id.set("")
        self.var_name.set("")
        self.show()

if __name__=="__main__":
    root =Tk()
    obj=categoryClass(root)
    root.mainloop()