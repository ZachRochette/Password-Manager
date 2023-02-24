########################## PASSWORD MANAGER ###################

from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
import os
import sys

# ----------------------- PASSWORD SETUP ------------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '@', '#', '$', '%', '&', '*', '+', '(', ')']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols

    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ----------------------- SAVE DATA ------------------------------------- #


def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {
        "email": email,
        "password": password
    }}

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showwarning(title="Missing Data",
                               message="Please fill in all fields.")
    else:
        try:
            with open("data.json", "r") as f:
                # Read old data
                data = json.load(f)
        except FileNotFoundError:
            with open("data.json", "w") as f:
                json.dump(new_data, f, indent=4)
        else:
            # Update old data
            data.update(new_data)

            with open("data.json", "w") as f:
                # Save updated data
                json.dump(data, f, indent=4)
        finally:
            website_entry.delete(0, 'end')
            # email_entry.delete(0,'end')
            password_entry.delete(0, 'end')

# --------------------- FIND PASSWORD ---------------------------------- #


def find_password():

    website = website_entry.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(
            title="File Not Found", message=f"The file you are looking for does not exist.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(
                title=website, message=f"Email: {email}\n Password: {password}")
        else:
            messagebox.showinfo(
                title="Data Not Found", message=f"No details for {website} exists.")
    # ----------------------- UI SETUP ------------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="#FFFFFF")


# Canvas

# ------------ Get Images to work with pyinstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


canvas = Canvas(width=200, height=200, bg="#FFFFFF", highlightthickness=0)
logo_img = PhotoImage(file=resource_path("logo.png"))
canvas.create_image(100, 90, image=logo_img)
canvas.grid(row=0, column=1)

# Grid

website_label = Label(text="Website: ", bg="#FFFFFF").grid(row=1, column=0)
email_label = Label(text="Email/Username: ",
                    bg="#FFFFFF").grid(row=2, column=0)
password_label = Label(text="Password: ", bg="#FFFFFF").grid(row=3, column=0)

# Entries

website_entry = Entry(width=33, highlightthickness=1)
website_entry.grid(row=1, column=1, columnspan=1, pady=5)
website_entry.focus()
website_entry.get()

email_entry = Entry(width=52, highlightthickness=1)
email_entry.grid(row=2, column=1, columnspan=2, pady=5)
email_entry.insert(0,  f"{email_entry.get()}")
email_entry.get()

password_entry = Entry(width=33, highlightthickness=1)
password_entry.grid(row=3, column=1, pady=5)
password_entry.get()

# Buttons

generate_password_button = Button(
    text="Generate Password", command=generate_password).grid(row=3, column=2, pady=5)

add_button = Button(text="Add", width=44, command=save).grid(
    row=4, column=1, columnspan=2, pady=5)

search_button = Button(text="Search", width=15,
                       command=find_password).grid(row=1, column=2)


# Keep Tkinter open

window.mainloop()
