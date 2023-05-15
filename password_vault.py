import sqlite3, hashlib
from tkinter import *

#Database Code
with sqlite3.connect("password_vault.db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS MasterPassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);
""")

#Initiate Window
window = Tk()

window.title("Password Vault")

def hashPassword(input):
    hash = hashlib.md5(input)
    hash = hash.hexdigest()

    return hash

def firstScreen():
    window.geometry("350x150")
    lbl = Label(window, text="Create Master Password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=30, show="*")  # the width changes the size of the textbox ( txt = Entry(window, width=30, show="*") replace text with a star)
    txt.pack(pady=3)
    txt.focus()  # This code automatically puts the cursor in the textbox

    lbl1 = Label(window, text="Re-enter Password")
    lbl1.pack()

    txt1 = Entry(window, width=30, show="*")  # the width changes the size of the textbox ( txt = Entry(window, width=30, show="*") replace text with a star)
    txt1.pack(pady=3)

    lbl2 = Label(window)
    lbl2.pack()

    def savePassword():
        if txt.get() == txt1.get():
            hashedPassword = hashPassword(txt.get().encode("utf-8"))
            insert_password = """INSERT INTO MasterPassword(password)
            VALUES(?)"""
            cursor.execute(insert_password,[(hashedPassword)])
            db.commit() #Saves password entry into database

            passwordVault() #Once the password is saved, we are taken to the password vault screen
        else:
            lbl2.config(text="Passwords do not match")

    btn = Button(window, text="Save", command=savePassword)
    btn.pack(pady=10)

def loginScreen():
    window.geometry("250x100")

    lbl = Label(window, text="Enter Master Password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=30, show="*")  #the width changes the size of the textbox (#txt = Entry(window, width=30, show="*") replace text with a star)
    txt.pack(pady=3)
    txt.focus() #This code automatically puts the cursor in the textbox

    lbl1 = Label(window)
    lbl1.pack()

    def getMasterPassword():
        checkHashedPassword = hashPassword(txt.get().encode("utf-8"))
        cursor.execute("SELECT * FROM MasterPassword WHERE id = 1 AND password = ?", [(checkHashedPassword)])
        return cursor.fetchall()

    def checkPassword(): #Must place above the button otherwise it will fail (because it will be called before the button is created)
        match = getMasterPassword()

        print(match)

        if match:
            passwordVault()
        else:
            txt.delete(0,'end') #Deletes text in textbox after you hit submit
            lbl1.config(text="Wrong Password")

    btn = Button(window, text="Submit", command=checkPassword)
    btn.pack(pady=10)

def passwordVault():
    for widget in window.winfo_children(): #when we switch from log in screen to the password vault then it will destroy all the text
        widget.destroy()
    window.geometry("700x350")

    lbl = Label(window, text="Password Vault")
    lbl.config(anchor=CENTER)
    lbl.pack()


cursor.execute("SELECT * FROM MasterPassword")
if cursor.fetchall():
    loginScreen()
else:
    firstScreen()
window.mainloop()
