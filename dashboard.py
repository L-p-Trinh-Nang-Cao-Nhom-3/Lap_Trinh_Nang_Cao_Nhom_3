import os
import sqlite3
import time
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import messagebox

from pythonProject.QuanLySieuThi.Customer import customerClass
from pythonProject.QuanLySieuThi.bill import bill_Class
from pythonProject.QuanLySieuThi.category import categoryClass
from pythonProject.QuanLySieuThi.employee import employeeClass
from pythonProject.QuanLySieuThi.position import positionClass
from pythonProject.QuanLySieuThi.product import productClass
from pythonProject.QuanLySieuThi.sales import sale_Class
from pythonProject.QuanLySieuThi.spending import spendClass
from pythonProject.QuanLySieuThi.supplier import supplierClass

#https://www.figma.com/file/OBVBb3tnPXnfbqzGJgiwBZ/Untitled?node-id=0%3A1
#225864-e5917e49-e4ac-49cc-b457-0ef392a86b80

class RMS:
    def __init__(self,root):
        self.root=root
        self.root.title("Supermarket Management System | Develop By: Group 3 ")
        self.root.geometry("1350x700+100+50")
        self.root.config(bg="#E0FFFF")
        self.root.resizable(width =False, height =False)


        # -------- title--------

        title = Label(self.root,text="Supermarket Management System",font=("times new roman",30,"bold"),bg="#800040",fg="white").place(x=0, y=0, relwidth=1, height=50)

        # ======= button==========
        btn_logout = Button(self.root,command=self.logout,text="Logout", font=("Elephant", 20, "bold"), cursor="hand2", bg="#ffff4d", fg="black").place(x=1030, y=3, height=50, width=150)
        lbl_exit = Button(self.root, text="Exit", command=self.exit, font=("Elephant", 20, "bold"), bg="#ffff4d",fg="#802000", cursor="hand2").place(x=1180, y=3, height=50, width=150)


        #============= clock===============
        self.lbl_clock=Label(self.root,text="Welcome To Supermarket Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15,"bold"),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0, y=50, relwidth=1, height=25)

        #====== left menu=========
        self.MenuLogo=Image.open("images/menu.png")
        self.MenuLogo=self.MenuLogo.resize((300,110),Image.ANTIALIAS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)

        # lbl_menulogo = Label(leftMenu, image=self.MenuLogo)

        leftMenu = LabelFrame(self.root, bd=2, relief=RIDGE, bg="#B0E0E6")
        leftMenu.place(x=0, y=75, width=300, height=600)

        lbl_menu=Label(leftMenu, text="Menu",image=self.MenuLogo,font=("times new roman", 35)).pack(side=TOP,fill=X)


        lbl_employee=Button(leftMenu,text="Employee",command=self.employee,font=("Elephant", 22,"bold"),bg="#B0E0E6",fg="#e60000",activebackground="#B0E0E6",bd=0,cursor="hand2").place(x=70,y=120)
        lbl_position=Button(leftMenu,text="Position",command=self.position,font=("Elephant", 22,"bold"),bg="#B0E0E6",fg="#e60000",activebackground="#B0E0E6",bd=0,cursor="hand2").place(x=70,y=170)
        lbl_supplier=Button(leftMenu,text="Supplier",command=self.supplier,font=("Elephant", 22,"bold"),bg="#B0E0E6",fg="#e60000",activebackground="#B0E0E6",bd=0,cursor="hand2").place(x=70,y=220)
        lbl_category=Button(leftMenu,text="Category",command=self.category,font=("Elephant", 22,"bold"),bg="#B0E0E6",fg="#e60000",activebackground="#B0E0E6",bd=0,cursor="hand2").place(x=70,y=270)
        lbl_product=Button(leftMenu,text="Product",command=self.product,font=("Elephant", 22,"bold"),bg="#B0E0E6",fg="#e60000",activebackground="#B0E0E6",bd=0,cursor="hand2").place(x=70,y=320)
        lbl_customer=Button(leftMenu,text="Customer",command=self.customer,font=("Elephant", 22,"bold"),bg="#B0E0E6",fg="#e60000",activebackground="#B0E0E6",bd=0,cursor="hand2").place(x=70,y=370)
        lbl_spend=Button(leftMenu,text="Spend",command=self.spend,font=("Elephant", 22,"bold"),bg="#B0E0E6",fg="#e60000",activebackground="#B0E0E6",bd=0,cursor="hand2").place(x=70,y=420)
        lbl_sale=Button(leftMenu,text="Sale",command=self.sales,font=("Elephant", 22,"bold"),bg="#B0E0E6",fg="#e60000",activebackground="#B0E0E6",bd=0,cursor="hand2").place(x=70,y=470)
        lbl_sale=Button(leftMenu,text="Bill",command=self.bill,font=("Elephant", 22,"bold"),bg="#B0E0E6",fg="#e60000",activebackground="#B0E0E6",bd=0,cursor="hand2").place(x=70,y=520)



        #=============== Content==============
        self.lbl_employee = Label(self.root, text="Total Employee \n[ 0 ]", font=("goudy old style", 20),bg="#ff80ff")
        self.lbl_employee.place(x=850, y=120, width=200, height=100)
        self.lbl_supplier = Label(self.root, text="Total Supplier\n[ 0 ]", font=("goudy old style", 20),bg="#ff80ff")
        self.lbl_supplier.place(x=850, y=260, width=200, height=100)
        self.lbl_category = Label(self.root, text="Total Category\n[ 0 ]", font=("goudy old style", 20),bg="#ff80ff")
        self.lbl_category.place(x=1100, y=120, width=200, height=100)
        self.lbl_product = Label(self.root, text="Total Product\n[ 0 ]", font=("goudy old style", 20), bd=5,bg="#ff80ff")
        self.lbl_product.place(x=1100, y=260, width=200, height=100)
        self.lbl_customer = Label(self.root, text="Total Customer\n[ 0 ]", font=("goudy old style", 20),bg="#ff80ff")
        self.lbl_customer.place(x=850, y=400, width=200, height=100)
        self.lbl_spend = Label(self.root, text="Total spend\n[ 0 ]", font=("goudy old style", 20), bg="#ff80ff")
        self.lbl_spend.place(x=1100, y=400, width=200, height=100)
        self.lbl_sale = Label(self.root, text="Total Sales\n[ 0 ]", font=("goudy old style", 20),bg="#ff80ff")
        self.lbl_sale.place(x=850, y=540, width=200, height=100)
        self.lbl_bill = Label(self.root, text="Total Bill\n[ 0 ]", font=("goudy old style", 20), bg="#ff80ff")
        self.lbl_bill.place(x=1100, y=540, width=200, height=100)

        # -------- footer--------
        lbl_footer=Label(self.root,text="Supermarket Management System.      Designer By: Nguyen Van Dung",font=("goudy old style", 12), bg="#4d636d", fg="white").pack(side=BOTTOM, fill=X)

        self.update_content()


    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)

    def position(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = positionClass(self.new_win)

    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = sale_Class(self.new_win)

    def customer(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = customerClass(self.new_win)

    def spend(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = spendClass(self.new_win)

    def bill(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = bill_Class(self.new_win)

    def update_content(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            cur.execute('select * from product')
            product=cur.fetchall()
            self.lbl_product.config(text=f"Total Product\n[ {str(len(product))} ]")

            cur.execute('select * from supplier')
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f"Total Supplier\n[ {str(len(supplier))} ]")

            cur.execute('select * from category')
            category = cur.fetchall()
            self.lbl_category.config(text=f"Total Category\n[ {str(len(category))} ]")

            cur.execute('select * from employee')
            employee = cur.fetchall()
            self.lbl_employee.config(text=f"Total Employee\n[ {str(len(employee))} ]")

            bill=str(len(os.listdir('bill')))
            self.lbl_sale.config(text=f"Total Sales\n[{bill}]")

            time_ = time.strftime('%I:%M:%S')
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome To Supermarket Management System\t\t Date:{str(date_)}\t\t Time:{str(time_)}")
            self.lbl_clock.after(200, self.update_content)

            cur.execute('select * from customer')
            customer = cur.fetchall()
            self.lbl_customer.config(text=f"Total Customer\n[ {str(len(customer))} ]")

            cur.execute('select * from spend')
            spend = cur.fetchall()
            self.lbl_spend.config(text=f"Total Spend\n[ {str(len(spend))} ]")

            cur.execute('select * from bill')
            bill = cur.fetchall()
            self.lbl_bill.config(text=f"Total Bill\n[ {str(len(bill))} ]")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)



    def exit(self):
        op = messagebox.askyesno("Confirm", "Do you readly want to Exit", parent=self.root)
        if op == True:
            self.root.destroy()

    def logout(self):
        self.root.destroy()
        os.system("python login.py")



if __name__=="__main__":
    root =Tk()
    obj=RMS(root)
    root.mainloop()
