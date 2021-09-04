import os
import sqlite3
import time
from tkinter import  *

from PIL import ImageTk
from tkinter import messagebox
import email_pass
import smtplib


class Login_system:
    def __init__(self,root):
        self.root = root
        self.root.title("Supermarket Management System | Develop By: Group 3 ")
        self.root.geometry("1350x700+100+50")
        self.root.config(bg="#E0FFFF")
        self.root.resizable(width=False, height=False)

        self.otp=''
        #=========== variable ============
        self.employee_id=StringVar()
        self.password=StringVar()
        title = Label(self.root, text="Welcome to the supermarket management program",font=("times new roman", 25, "bold"), bg="#ac7339", fg="white").place(x=0, y=0, relwidth=1, height=50)
        title = Label(self.root, text="Designer By: Dragon King (Group: 3)",font=("times new roman", 13, "bold"), bg="#cc9966", fg="white").pack(side=BOTTOM,fill=X)



        #======== Logn frame ===
        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=150,y=100,width=450,height=500)

        title=Label(login_frame,text='Login System',font=('Elephant',28,"bold"),bg="white").place(x=0,y=10,relwidth=1)

        lbl_user=Label(login_frame,text="Employee Id",font=("Elephant",20),bg="white",fg="#ff0040").place(x=40,y=100)
        txt_username=Entry(login_frame,textvariable=self.employee_id,font=("times new roman",25),bg="#ECECEC").place(x=40,y=145,width=350,height=40)

        lbl_pass = Label(login_frame, text="Password", font=("Elephant", 20), bg="white", fg="#ff0040").place(x=40, y=200)
        txt_pass= Entry(login_frame,textvariable=self.password,show='*',font=("times new roman", 25), bg="#ECECEC").place(x=40, y=245, width=350,height=40)

        btn_login=Button(login_frame,command=self.login,text="Login",font=("Arial Rounded MT Bold",15),bg="#00B0F0",activebackground="#00B0F0",fg="white",activeforeground="white",cursor="hand2").place(x=90,y=310,width=250,height=40)

        hr=Label(login_frame,bg="lightgray").place(x=40,y=385,width=350,height=2)
        or_=Label(login_frame,text="OR",font=("times new roman",15,"bold"),bg="white",fg="red").place(x=200,y=370)

        btn_forget =Button(login_frame,command=self.forget_window,text="Forget Password?",font=("times new roman",13),bd=0,bg="white",activebackground="white",fg="#00759E",activeforeground="#00759E").place(x=160,y=420)




#================ all funtion ==============
        self.im1 = ImageTk.PhotoImage(file="images/ima1.png")
        self.im2 = ImageTk.PhotoImage(file="images/ima2.png")
        self.im3 = ImageTk.PhotoImage(file="images/ima3.png")

        self.lbl_change_image = Label(self.root, bg='white')
        self.lbl_change_image.place(x=601, y=101,width=720,height=498)

        self.animate()

    # ================ all funtion ==============


    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000, self.animate)

    def login(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror("Error","All Fields are required", parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? and password=?",(self.employee_id.get(),self.password.get(),))
                user = cur.fetchone()
                if user==None:
                    messagebox.showerror("Error", "Invalid Employee ID or Password", parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system('python dashboard.py')
                    else:
                        self.root.destroy()
                        os.system('python billing.py')

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def forget_window(self):
        con = sqlite3.connect(database="suppermarket.db")
        cur = con.cursor()
        try:
            if self.employee_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("select email from employee where eid=?",(self.employee_id.get(),))
                email = cur.fetchone()
                if email== None:
                    messagebox.showerror("Error", "Invalid Employee ID, Try again!", parent=self.root)
                else:
                    #== Forget pass====
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()
                    #== call sent email function
                    chk=self.sen_email(email[0])
                    if chk =='f':
                        messagebox.showerror("Error","Connection Error, try again",parent=self.root)
                    else:
                        self.forget_win=Toplevel(self.root)
                        self.forget_win.title("RESET PASSWORD")
                        self.forget_win.geometry('400x360+270+220')
                        self.forget_win.config(bg="white")
                        self.forget_win.focus_force()

                        title = Label(self.forget_win, text="Reset Password", font=("goudy old style", 15, "bold"), bg="#5cd65c", fg="white").pack(side=TOP, fill=X)
                        lbl_reset = Label(self.forget_win, text="Enter OTP Sent on Resgistered Email", font=("times new roman", 15),fg="red",bg="white").place(x=20,y=60)
                        txt_rese=Entry(self.forget_win,textvariable=self.var_otp, font=("times new roman", 15),bg="lightyellow").place(x=20,y=100,width=250,height=30)
                        self.btn_reset=Button(self.forget_win,command=self.validate_otp,text="SUBMIT", font=("times new roman", 15),bg="lightblue")
                        self.btn_reset.place(x=280, y=100, width=100, height=30)

                        new_pass= Label(self.forget_win,text="New Password",font=("goudy old style", 15, "bold"),bg="white").place(x=20, y=160)
                        txt_pass= Entry(self.forget_win,textvariable=self.var_new_pass, font=("times new roman", 15), bg="lightyellow").place(x=20,y=190,width=250,height=30)

                        conf_pass = Label(self.forget_win, text="Confirm Password", font=("goudy old style", 15, "bold"),bg="white").place(x=20, y=225)
                        txt_conf_pass = Entry(self.forget_win,textvariable=self.var_conf_pass,font=("times new roman", 15), bg="lightyellow").place(x=20,y=255,width=250,height=30)

                        self.btn_update = Button(self.forget_win,command=self.update_password,text="Update",state=DISABLED,font=("times new roman", 15), bg="lightblue")
                        self.btn_update.place(x=20, y=300, width=100, height=40)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("Error","Password is required",parent=self.forget_win)
        elif self.var_new_pass.get() != self.var_conf_pass.get():
            messagebox.showerror("Error", "New Password & Confirm Password should be same", parent=self.forget_win)
        else:
            con = sqlite3.connect(database="suppermarket.db")
            cur = con.cursor()

            try:
                cur.execute("update employee set password=? where eid=?",(self.var_new_pass.get(),self.employee_id.get(),))
                con.commit()
                messagebox.showinfo("Success", "Change Password success", parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Erroe","Invalid OTP, Try again",paretn=self.forget_win)


    def sen_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_

        s.login(email_,pass_)
        self.otp=int(time.strftime("%H%S%M")) +int(time.strftime("%S"))
        subj='Supermarket Management System: Reset Password OTP'
        msg=f'Hello!,\n\nYou Reset OTP is {str(self.otp)}.\n\n By:Nguyen Van Dung\nThank You!'
        msg='Subject: {}\n\n{}'.format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return  's'
        else:
            return  'f'


if __name__=="__main__":
    root =Tk()
    obj=Login_system(root)
    root.mainloop()
