import array
import sqlite3
from datetime import *
import time
from tkinter import *
from tkinter import messagebox, ttk, StringVar
import os
import tempfile

from pythonProject.QuanLySieuThi.spend_eml import spendClass_emp


class BillingClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Supermarket Management System | Develop By: Group 3 ")
        self.root.geometry("1350x700+100+50")
        self.root.config(bg="#E0FFFF")
        self.cart_list = []
        self.customer_list = []
        self.chk_print = 0
        self.root.resizable(width=False, height=False)

        # -------- title--------

        title = Label(self.root, text="Supermarket Management System", font=("times new roman", 35, "bold"),
                      bg="#800040", fg="white", anchor="w", padx=20, compound=LEFT, ).place(x=0, y=0, relwidth=1,
                                                                                            height=70)

        # ======= button==========
        btn_spend = Button(self.root, command=self.spend, text="Spend", font=("Elephant", 20, "bold"), cursor="hand2",
                           bg="yellow", fg="black").place(x=970, y=10, height=50, width=150)
        btn_logout = Button(self.root, command=self.logout, text="Logout", font=("Elephant", 20, "bold"),
                            cursor="hand2", bg="yellow", fg="black").place(x=1150, y=10, height=50, width=150)

        # ============= clock===============
        self.lbl_clock = Label(self.root,
                               text="Welcome To Supermarket Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",
                               font=("times new roman", 15, "bold"), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # ============ Product_Frame ===============

        # ========= Variablr=========
        self.var_search = StringVar()
        self.var_cname = StringVar()
        self.var_contact = StringVar()

        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()
        self.var_date = StringVar()

        self.var_name_empl = StringVar()

        self.employee_list = []
        self.fetch_employee()
        self.proname_list= []
        self.qty_list=[]
        self.price_list=[]





        ProductFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        ProductFrame1.place(x=6, y=110, width=410, height=550)

        pTitle = Label(ProductFrame1, text="All Products", font=("goudy old style", 20, "bold"), bg="#262626",
                       fg="white").pack(side=TOP, fill=X)
        # ==========Product Search Frame===========
        ProductFrame2 = Frame(ProductFrame1, bd=4, relief=RIDGE, bg="white")
        ProductFrame2.place(x=2, y=42, width=398, height=90)

        lbl_search = Label(ProductFrame2, text="Search Product | By Name", font=("times new roman", 15, "bold"),
                           bg="white", fg="green").place(x=2, y=5)
        lbl_search = Label(ProductFrame2, text="Product Name", font=("times new roman", 15, "bold"), bg="white").place(
            x=2, y=45)
        txt_search = Entry(ProductFrame2, textvariable=self.var_search, font=("times new roman", 15),
                           bg="lightyellow").place(x=128, y=47, width=150, height=22)
        btn_search = Button(ProductFrame2, command=self.search, text="Search", font=("goudy old style", 15),
                            bg="#2196f3", fg="white", cursor="hand2").place(x=285, y=45, width=100, height=25)
        btn_show_all = Button(ProductFrame2, command=self.show, text="Show All", font=("goudy old style", 15),
                              bg="#083531", fg="white", cursor="hand2").place(x=285, y=10, width=100, height=25)

        # ========== Product detail Frame===========
        ProductFrame3 = Frame(ProductFrame1, bd=3, relief=RIDGE)
        ProductFrame3.place(x=2, y=140, width=398, height=400)

        scrollx = Scrollbar(ProductFrame3, orient=HORIZONTAL)
        scrolly = Scrollbar(ProductFrame3, orient=VERTICAL)
        self.product_Table = ttk.Treeview(ProductFrame3, columns=("pid", "name", "price", "qty", "status"),
                                          xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        self.product_Table.heading("pid", text="Pro_id")
        self.product_Table.heading("name", text="Name")
        self.product_Table.heading("price", text="Price")
        self.product_Table.heading("qty", text="QTY")
        self.product_Table.heading("status", text="status")
        self.product_Table["show"] = 'headings'
        self.product_Table.column("pid", width=60)
        self.product_Table.column("name", width=100)
        self.product_Table.column("price", width=70)
        self.product_Table.column("qty", width=70)
        self.product_Table.column("status", width=70)
        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)

        # ================ Customer Frame =========

        Customer_Frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        Customer_Frame.place(x=420, y=110, width=450, height=170)

        cTitle = Label(Customer_Frame, text="Customer Details", font=("goudy old style", 15, "bold"), bg="pink").pack(
            side=TOP, fill=X)
        lbl_name = Label(Customer_Frame, text="Name", font=("Elephant", 15), bg="white").place(x=5, y=35)
        txt_name = Entry(Customer_Frame, textvariable=self.var_cname, font=("times new roman", 13),
                         bg="lightyellow").place(x=170, y=35, width=220, height=30)

        lbl_contact = Label(Customer_Frame, text="Contact No.", font=("Elephant", 15), bg="white").place(x=5, y=80)
        txt_contact = Entry(Customer_Frame, textvariable=self.var_contact, font=("times new roman", 13),
                            bg="lightyellow").place(x=170, y=80, width=220, height=30)

        lbl_name_eploy = Label(Customer_Frame, text="Name employee", font=("Elephant", 15), bg="white").place(x=5,
                                                                                                              y=125)
        cmb_name_eploy = ttk.Combobox(Customer_Frame, textvariable=self.var_name_empl, values=self.employee_list,
                                      state='readonly', justify=CENTER, font=("times new roman", 13))
        cmb_name_eploy.place(x=170, y=125, width=220, height=30)
        cmb_name_eploy.current(0)

        # ==========Cal Cart Frame===========
        Cal_Cat_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        Cal_Cat_Frame.place(x=420, y=280, width=450, height=180)

        # ========== Cart Frame===========
        cart_Frame = Frame(Cal_Cat_Frame, bd=3, relief=RIDGE, bg="white")
        cart_Frame.place(x=0, y=0, width=450, height=180)
        self.cart_Title = Label(cart_Frame, text="Cart \t Total Product: [0]", font=("goudy old style", 15, "bold"),
                                bg="pink")
        self.cart_Title.pack(side=TOP, fill=X)

        scrollx = Scrollbar(cart_Frame, orient=HORIZONTAL)
        scrolly = Scrollbar(cart_Frame, orient=VERTICAL)
        self.cart_Table = ttk.Treeview(cart_Frame, columns=("pid", "name", "price", "qty"), xscrollcommand=scrollx.set,
                                       yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.cart_Table.xview)
        scrolly.config(command=self.cart_Table.yview)

        self.cart_Table.heading("pid", text="Pro_id")
        self.cart_Table.heading("name", text="Name")
        self.cart_Table.heading("price", text="Price")
        self.cart_Table.heading("qty", text="QTY")
        self.cart_Table["show"] = 'headings'
        self.cart_Table.column("pid", width=60)
        self.cart_Table.column("name", width=100)
        self.cart_Table.column("price", width=80)
        self.cart_Table.column("qty", width=70)
        self.cart_Table.pack(fill=BOTH, expand=1)
        self.cart_Table.bind("<ButtonRelease-1>", self.get_data)

        # =============== ADD Cart Widgrts Frame===========

        Add_CartWidgetsFrame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        Add_CartWidgetsFrame.place(x=420, y=460, width=450, height=200)

        lbl_p_name = Label(Add_CartWidgetsFrame, text="Product Name", font=("times new roman", 15), bg="white").place(
            x=5, y=10)
        txt_p_name = Entry(Add_CartWidgetsFrame, textvariable=self.var_pname, font=("times new roman", 15),
                           bg="lightyellow", state='readonly').place(x=130, y=10, width=190, height=28)

        lbl_p_price = Label(Add_CartWidgetsFrame, text="Price Per Qty", font=("times new roman", 15), bg="white").place(
            x=5, y=45)
        txt_p_price = Entry(Add_CartWidgetsFrame, textvariable=self.var_price, font=("times new roman", 15),
                            bg="lightyellow", state='readonly').place(x=130, y=45, width=190, height=28)

        lbl_p_qty = Label(Add_CartWidgetsFrame, text="Quantity", font=("times new roman", 15), bg="white").place(x=5,
                                                                                                                 y=75)
        txt_p_qty = Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, font=("times new roman", 15),
                          bg="lightyellow").place(x=130, y=75, width=190, height=28)

        lbl_p_qty = Label(Add_CartWidgetsFrame, text="In Stock ", font=("times new roman", 15), bg="white").place(x=5,
                                                                                                                  y=110)
        self.lbl_inStock = Label(Add_CartWidgetsFrame, textvariable=self.var_stock, font=("times new roman", 15),
                                 bg="white")
        self.lbl_inStock.place(x=130, y=110, width=190, height=28)

        btn_clear_cart = Button(Add_CartWidgetsFrame, command=self.clear_cart, text="Clear",
                                font=("goudy old style", 15), bg="lightgray", cursor="hand2").place(x=130, y=150,
                                                                                                    width=100,
                                                                                                    height=35)
        btn_add_cart = Button(Add_CartWidgetsFrame, command=self.add_update_cart, text="Add | Update cart",
                              font=("goudy old style", 15), bg="orange", cursor="hand2").place(x=250, y=150, width=170,
                                                                                               height=35)

        # ========= billing area ============
        bill_Frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        bill_Frame.place(x=875, y=110, width=470, height=410)

        bTitle = Label(bill_Frame, text="Custumer Bill Area", font=("goudy old style", 20, "bold"), bg="#1a75ff").pack(
            side=TOP, fill=X)
        scrolly = Scrollbar(bill_Frame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(bill_Frame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        # ============ billing button ==============
        bill_menu_Frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        bill_menu_Frame.place(x=875, y=520, width=470, height=140)

        self.lbl_net_pay = Label(bill_menu_Frame, text="Total Bill \n [0]", font=("goudy old style", 20), bg="#ff704d",
                                 fg="white")
        self.lbl_net_pay.place(x=0, y=0, width=470, height=70)

        btn_print = Button(bill_menu_Frame, text="Print", command=self.print_bill, font=("goudy old style", 20),
                           bg="#e62e00", cursor="hand2")
        btn_print.place(x=2, y=75, width=130, height=60)

        btn_clear_all = Button(bill_menu_Frame, command=self.clear_all, text="Clear All", font=("goudy old style", 20),
                               bg="gray", cursor="hand2")
        btn_clear_all.place(x=140, y=75, width=140, height=60)

        btn_generate = Button(bill_menu_Frame, command=self.total, text="Save Bill", font=("goudy old style", 20),
                              bg="#e6e600", cursor="hand2")
        btn_generate.place(x=290, y=75, width=170, height=60)

        # -------- footer--------
        lbl_footer = Label(self.root, text="Supermarket Management System    Designer By: Nguyen Van Dung",
                           font=("times new roman", 20), bg="#4d636d", fg="white").pack(side=BOTTOM, fill=X)
        self.show()
        self.update_date_time()

    # ======================= All function=================

    def total(self):
        self.generate_bill()
        self.add_cus()
        self.add_bill()

    def show(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows = cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    # ===============================

    def search(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                cur.execute(
                    "select pid,name,price,qty,status from product where name LIKE '%" + self.var_search.get() + "%' and status='Active'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert("", END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def get_data(self, ev):
        r = self.product_Table.focus()
        content = self.product_Table.item(r)
        row = content["values"]
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')


    def add_update_cart(self):
        if self.var_pid.get() == "":
            messagebox.showerror("Error", "Please select product from the list", parent=self.root)
        elif self.var_qty.get() == "" or self.var_pid.get() == "":
            messagebox.showerror("Error", "Quantity is Required", parent=self.root)
        elif int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror("Error", "Invalid Quantity", parent=self.root)
        else:
            # price_cal = int(self.var_qty.get()) * float(self.var_price.get())
            # price_cal = float(price_cal)
            price_cal = self.var_price.get()
            cart_data = [self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get(), self.var_stock.get()]


            # ================ update_cart ===========
            present = 'no'
            index_ = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = "yes"
                    break
                index_ += 1
            if present == 'yes':
                op = messagebox.askyesno("Confirm", "Product already preseent\nDo you want to Update| remove from the Cart list", parent=self.root)
                if op == True:
                    if self.var_qty.get() == "0":
                        self.cart_list.pop(index_)
                    else:
                        # self.cart_list[index_][2] = price_cal  # price
                        self.cart_list[index_][3] = self.var_qty.get()  # qty

            else:
                self.cart_list.append(cart_data)


            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amnt = 0
        self.net_pay = 0
        self.discount = 0
        for row in self.cart_list:
            self.bill_amnt = self.bill_amnt + (float(row[2]) * int(row[3]))

        self.net_pay = self.bill_amnt
        self.lbl_net_pay.config(text=f'Total Bill\n{str(self.net_pay)}')
        self.cart_Title.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.cart_Table.delete(*self.cart_Table.get_children())
            for row in self.cart_list:
                self.cart_Table.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def generate_bill(self):
        if self.var_cname.get() == '' or self.var_contact.get() == '' or self.var_name_empl.get() == "Select":
            messagebox.showerror("Error", "Customer Details are required", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", "Please Add product to the Cartegory!!!", parent=self.root)
        else:
            # ============ Bill Top ============
            self.bill_top()
            # ============ Bill Middle =========
            self.bill_middle()
            # ============ Bill Bttom ==========
            self.bill_botom()
            fp = open(f"bill/{str(self.invoice)}.txt", 'w',encoding="utf-8")
            fp.write(self.txt_bill_area.get("1.0", END))
            fp.close()
            messagebox.showinfo("Saved", "Bill has been generated/Save in Backend", parent=self.root)
            self.chk_print = 1

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%y"))
        bill_top_temp = f'''
\t\tCUSTOMER PAYMENT INVOICE\n
    Phone No. 0978xxxxxxx , Address: TP_HCM
{str("=" * 55)}
 Customer Name: {self.var_cname.get()}
 Phone No. :{self.var_contact.get()}
 Employee Name: {self.var_name_empl.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%y"))}
{str("=" * 55)}  
 Product Name\t\tQTY\t\tPrice
{str("=" * 55)}  
'''
        self.txt_bill_area.delete("1.0", END)
        self.txt_bill_area.insert("1.0", bill_top_temp)

    def bill_botom(self):
        bill_bottom_temp = f'''
{str("=" * 55)}   

 Total Bill\t\t\t\t{self.net_pay}VND.  
{str("=" * 55)} \n        
{str("--------------------- Thank You ! ---------------------")}\n        
        '''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def bill_middle(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            for row in self.cart_list:
                pid = row[0]
                self.name = row[1]

                self.row3 = int(row[3])
                self.row4 = int(row[4])
                qty = self.row4 - self.row3
                if self.row3 == self.row4:
                    status = 'Inactive'
                if self.row3 != self.row4:
                    status = 'Active'
                price = float(row[2]) * self.row3
                price = str(price)
                self.txt_bill_area.insert(END, "\n " + self.name + "\t\t" + (str(self.row3)) + "\t\t" + price + "VND.")
                # ====== update qty in product table============
                self.proname_list.append(self.name)
                self.price_list.append(row[2])
                self.qty_list.append(self.row3)
                cur.execute("update product set qty=?,status=? where pid=?", (qty, status, pid))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def clear_cart(self):
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.lbl_inStock.config(text="In Stock")
        self.var_stock.set("")

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set("")
        self.var_contact.set("")
        self.txt_bill_area.delete("1.0", END)
        self.cart_Title.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set("")
        self.clear_cart()
        self.show()
        self.show_cart()

    def update_date_time(self):
        self.time_ = time.strftime('%I:%M:%S')
        self.date_ = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(
            text=f"Welcome To Supermarket Management System\t\t Date:{str(self.date_)}\t\t Time:{str(self.time_)}")
        self.lbl_clock.after(200, self.update_date_time)

    def print_bill(self):
        if self.chk_print == 1:
            messagebox.showinfo('Print', 'Please wait while printing', parent=self.root)
            new_file = tempfile.mktemp('.txt')
            open(new_file, 'w').write(self.txt_bill_area.get('1.0', END))
            os.startfile(new_file, 'print')
        else:
            messagebox.showinfo('Print', 'Please generate bill, to print the receipt', parent=self.root)

    def add_cus(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.var_name_empl.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("select * from customer where name=? ", (self.var_name_empl.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Customer already present, try different", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO customer (cid,name,date,phone,proname,number,price,total) values (?,?,?,?,?,?,?,?)",
                        (self.invoice,
                         self.var_cname.get(),
                         self.date_,
                         self.var_contact.get(),
                         str(self.proname_list),
                         str(self.qty_list),
                         str(self.price_list),
                         self.net_pay,))
                    con.commit()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def add_bill(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO bill (name,name_emp,name_cus,date) values (?,?,?,?)",
                        (self.invoice,
                         self.var_name_empl.get(),
                         self.var_cname.get(),
                         self.date_,))
            con.commit()
            self.show()
        except Exception as ex:
            pass

    def fetch_employee(self):
        self.employee_list.append("Empty")
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            cur.execute("select name from employee ")
            rows = cur.fetchall()
            if len(rows) > 0:
                del self.employee_list[:]
                self.employee_list.append("Select")
                for row in rows:
                    self.employee_list.append(row[0])

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def spend(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = spendClass_emp(self.new_win)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")


if __name__ == "__main__":
    root = Tk()
    obj = BillingClass(root)
    root.mainloop()
