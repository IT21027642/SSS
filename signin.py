from tkinter import *
from tkinter import messagebox, simpledialog
from PIL import ImageTk
import pymysql
import pyotp
import io
import mysql.connector
import qrcode
import re
import cryptography



def login_user():
    username = usernameEntry.get().strip()
    password = passwordEntry.get().strip()

    if username == '' or password == '':
        messagebox.showerror('Error', 'All Fields Are Required')
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='1234', database='userdata')
            mycursor = con.cursor()

            # Fetch the user's secret key from the database
            query = 'SELECT * FROM data WHERE username=%s AND password=%s'
            mycursor.execute(query, (username, password))
            row = mycursor.fetchone()

            if row is None:
                messagebox.showerror('Error', 'Invalid Username or Password')
            else:
                # Generate QR code using user's secret key
                totp = pyotp.TOTP(row[3])
                otp_url = totp.provisioning_uri(name=username, issuer_name='MyApp')

                # Create a QR code image
                qr = qrcode.QRCode()
                qr.add_data(otp_url)
                qr_image = qr.make_image(fill="black", back_color="white")

                # Display the QR code image
                qr_image.show()

                # Prompt user to enter the code from the Google Authenticator app
                code = simpledialog.askstring('Verification', 'Enter the verification code')

                # Verify the code entered by the user
                if totp.verify(code):
                    messagebox.showinfo('Welcome', 'Login is Successful')
                else:
                    messagebox.showerror('Error', 'Invalid verification code')


        except pymysql.Error as e:
            messagebox.showerror('Error', 'Error connecting to the database: ' + str(e))

        finally:

            if 'con' in locals():
                con.close()


def signup_page():
    login_window.destroy()
    import signup

def hide():
    openeye.config(file='closeeye.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)

def show():
    openeye.config(file='openeye.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)

def user_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)

def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)


def forget_pass():
    def change_password():
        if user_entry.get() == '' or newpass_entry.get() == '' or confirmpass_entry.get() == '':
            messagebox.showerror('Error', 'All Fields are Required', parent=window)
        elif newpass_entry.get() != confirmpass_entry.get():
            messagebox.showerror('Error', 'Password and Confirm Password do not match', parent=window)
        else:
            try:
                con = pymysql.connect(host='localhost', user='root', password='1234', database='userdata')
                mycursor = con.cursor()
                query = 'SELECT * FROM data WHERE username=%s'
                mycursor.execute(query, (user_entry.get(),))
                row = mycursor.fetchone()
                if row is None:
                    messagebox.showerror('Error', 'Incorrect Username', parent=window)
                else:
                    query = 'UPDATE data SET password=%s WHERE username=%s'
                    mycursor.execute(query, (newpass_entry.get(), user_entry.get()))
                    con.commit()
                    messagebox.showinfo('Success', 'Password has been reset. Please login with the new password',
                                        parent=window)
                    window.destroy()
            except:
                messagebox.showerror('Error', 'Connection is not established. Try Again', parent=window)
            finally:
                if con:
                    con.close()

    window = Toplevel()
    window.title('Change Password')

    bgPic = ImageTk.PhotoImage(file='background.jpg')
    bglabel = Label(window, image=bgPic)
    bglabel.grid()

    heading_label = Label(window, text='RESET PASSWORD', font=('arial', '18', 'bold'), bg='white', fg='magenta2')
    heading_label.place(x=480, y=60)

    userLabel = Label(window, text='Username', font=('arial', 12, 'bold'), bg='white', fg='orchid1')
    userLabel.place(x=470, y=130)

    user_entry = Entry(window, width=25, fg='magenta2', font=('arial', 11, 'bold'), bd=0)
    user_entry.place(x=470, y=160)

    Frame(window, width=250, height=2, bg='orchid1').place(x=470, y=180)

    passwordLabel = Label(window, text='New Password', font=('arial', 12, 'bold'), bg='white', fg='orchid1')
    passwordLabel.place(x=470, y=210)

    newpass_entry = Entry(window, width=25, fg='magenta2', font=('arial', 11, 'bold'), bd=0)
    newpass_entry.place(x=470, y=240)

    Frame(window, width=250, height=2, bg='orchid1').place(x=470, y=260)

    submitButton = Button(window, text='Submit', bd=0, bg='magenta2', fg='white', font=('Open Sans', '16', 'bold'),
                          width=19, cursor='hand2', activebackground='magenta2', activeforeground='white',
                          command=change_password)
    submitButton.place(x=470, y=390)

    window.mainloop()


# GUI Part
login_window = Tk()
login_window.geometry('990x660+50+50')
login_window.resizable(0, 0)
login_window.title('Login Page')

bgImage = ImageTk.PhotoImage(file='bg.jpg')
bgLabel = Label(login_window, image=bgImage)
bgLabel.place(x=0, y=0)

heading = Label(login_window, text='USER LOGIN', font=('Microsoft Yahei UI Light', 23, 'bold'), bg='white',
                fg='firebrick1')
heading.place(x=605, y=120)

usernameEntry = Entry(login_window, width=25, font=('Microsoft Yeahei UI Light', 11, 'bold'), bd=0, fg='firebrick1')
usernameEntry.place(x=580, y=200)
usernameEntry.insert(0, 'Username')
usernameEntry.bind('<FocusIn>', user_enter)

frame1 = Frame(login_window, width=250, height=2)
frame1.place(x=580, y=222)

passwordEntry = Entry(login_window, width=25, font=('Microsoft Yeahei UI Light', 11, 'bold'), bd=0, fg='firebrick1')
passwordEntry.place(x=580, y=260)
passwordEntry.insert(0, 'Password')
passwordEntry.bind('<FocusIn>', password_enter)

frame2 = Frame(login_window, width=250, height=2)
frame2.place(x=580, y=282)

openeye = PhotoImage(file='openeye.png')
eyeButton = Button(login_window, image=openeye, bd=0, bg='white', activebackground='white', cursor='hand2',
                   command=hide)
eyeButton.place(x=800, y=255)

forgetButton = Button(login_window, text='Forgot Password?', bd=0, bg='white', activebackground='white', cursor='hand2',
                      font=('Microsoft Yeahei UI Light', 9, 'bold'), fg='firebrick1', activeforeground='firebrick1',
                      command=forget_pass)
forgetButton.place(x=715, y=295)

loginButton = Button(login_window, text='Login', font=('Open Sans', 16, 'bold'), fg='white', bg='firebrick1',
                     activeforeground='white', activebackground='firebrick1', cursor='hand2', bd=0, width=19,
                     command=login_user)
loginButton.place(x=578, y=350)

orLabel = Label(login_window, text='  --------------OR-------------', font=('Open Sans', 16), fg='firebrick1',
                bg='white')
orLabel.place(x=583, y=400)

facebook_logo = PhotoImage(file='facebook.png')
fbLabel = Label(login_window, image=facebook_logo, bg='white')
fbLabel.place(x=640, y=440)

google_logo = PhotoImage(file='google.png')
googleLabel = Label(login_window, image=google_logo, bg='white')
googleLabel.place(x=698, y=440)

twitter_logo = PhotoImage(file='twitter.png')
twitterLabel = Label(login_window, image=twitter_logo, bg='white')
twitterLabel.place(x=755, y=440)

signupLabel = Label(login_window, text="Don't have an account?", font=('Open Sans', 9), fg='firebrick1', bg='white')
signupLabel.place(x=590, y=500)

newaccountButton = Button(login_window, text='Create New One', font=('Open Sans', 9, 'bold underline'), fg='blue',
                          bg='white', activeforeground='blue', activebackground='white', cursor='hand2', bd=0,
                          command=signup_page)
newaccountButton.place(x=727, y=500)

login_window.mainloop()