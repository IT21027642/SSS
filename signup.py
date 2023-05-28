from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import re

import pymysql


def clear():
    emailEntry.delete(0, END)
    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)
    confirmEntry.delete(0, END)
    check.set(0)


def clear():
    emailEntry.delete(0, END)
    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)
    confirmEntry.delete(0, END)
    check.set(0)

def validate_email(email):
    # Email validation using regular expression
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def login_page():
    signup_window.destroy()
    import signin

def connect_database():
    email = emailEntry.get().strip()
    username = usernameEntry.get().strip()
    password = passwordEntry.get().strip()
    confirm_password = confirmEntry.get().strip()

    if email == '' or username == '' or password == '' or confirm_password == '':
        messagebox.showerror('Error', 'All Fields Are Required')
    elif not validate_email(email):
        messagebox.showerror('Error', 'Invalid Email Address')
    elif password != confirm_password:
        messagebox.showerror('Error', 'Password Mismatch')
    elif check.get() == 0:
        messagebox.showerror('Error', 'Please Accept Terms & Conditions')
    else:
        try:
            with pymysql.connect(host='localhost', user='root', password='1234', database='userdata') as con:
                mycursor = con.cursor()
                mycursor.execute('CREATE DATABASE IF NOT EXISTS userdata')
                mycursor.execute('USE userdata')
                mycursor.execute('''CREATE TABLE IF NOT EXISTS data(
                        id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                        email VARCHAR(50),
                        username VARCHAR(100),
                        password VARCHAR(20)
                    )''')
                query = 'SELECT * FROM data WHERE username=%s'
                mycursor.execute(query, (username,))
                row = mycursor.fetchone()
                if row is not None:
                    messagebox.showinfo('Error', 'Username Already Exists')
                else:
                    query = 'INSERT INTO data(email, username, password) VALUES (%s, %s, %s)'
                    mycursor.execute(query, (email, username, password))
                    con.commit()
                    messagebox.showinfo('Success', 'Registration is successful')
                    clear()
                    signup_window.destroy()
                    import signin
        except pymysql.Error as e:
            messagebox.showerror('Error', 'Database Connectivity Issue: ' + str(e))



signup_window = Tk()
signup_window.title('Signup Page')
signup_window.resizable(False, False)
background = ImageTk.PhotoImage(file='bg.jpg')

bgLabel = Label(signup_window, image=background)
bgLabel.grid()

frame = Frame(signup_window, bg='white')
frame.place(x=554, y=100)

heading = Label(frame, text='CREATE AN ACCOUNT', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white',
                fg='firebrick1')

heading.grid(row=0, column=0, padx=10, pady=10)

emailLabel = Label(frame, text='Email', font=('Microsoft Yahei UI Light', 10, 'bold'))
emailLabel.grid(row=1, column=0, sticky='w', padx=25, pady=(10, 0))

emailEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 10, 'bold'), fg='white', bg='firebrick1')
emailEntry.grid(row=2, column=0, sticky='w', padx=25)

usernameLabel = Label(frame, text='Username', font=('Microsoft Yahei UI Light', 10, 'bold'))
usernameLabel.grid(row=3, column=0, sticky='w', padx=25, pady=(10, 0))

usernameEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 10, 'bold'), fg='white', bg='firebrick1')
usernameEntry.grid(row=4, column=0, sticky='w', padx=25)

passwordLabel = Label(frame, text='Password', font=('Microsoft Yahei UI Light', 10, 'bold'))
passwordLabel.grid(row=5, column=0, sticky='w', padx=25, pady=(10, 0))

passwordEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 10, 'bold'), fg='white', bg='firebrick1')
passwordEntry.grid(row=6, column=0, sticky='w', padx=25)

confirmLabel = Label(frame, text='Confirm Password', font=('Microsoft Yahei UI Light', 10, 'bold'))
confirmLabel.grid(row=7, column=0, sticky='w', padx=25, pady=(10, 0))

confirmEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 10, 'bold'), fg='white', bg='firebrick1')
confirmEntry.grid(row=8, column=0, sticky='w', padx=25)

check = IntVar()
termsandconditions = Checkbutton(frame, text='I agree to the Terms & Conditions',
                                 font=('Microsoft Yahei UI Light', 9, 'bold'), fg='firebrick1', bg='white',
                                 activebackground='white', activeforeground='firebrick1', cursor='hand2',
                                 variable=check)
termsandconditions.grid(row=9, column=0, pady=10, padx=15)

signupButton = Button(frame, text='Signup', font=('Open Sans', 16, 'bold'), bd=0, bg='firebrick1', fg='white',
                      activebackground='firebrick1', activeforeground='white', width=17, command=connect_database)
signupButton.grid(row=10, column=0, pady=10)

alreadyaccount = Label(frame, text="Don't have an account..?", font=('Open Sans', 9, 'bold'), bg='white',
                       fg='firebrick1')
alreadyaccount.grid(row=11, column=0, sticky='w', padx=25, pady=10)

LoginButton = Button(frame, text='Log in', font=('Open Sans', 9, 'bold underline'), bg='white', fg='blue', bd='0',
                     cursor='hand2', activebackground='white', activeforeground='blue', command=login_page)
LoginButton.place(x=170, y=391)

signup_window.mainloop()