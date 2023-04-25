import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 9)
    nr_symbols = random.randint(2, 3)
    nr_numbers = random.randint(2, 3)

    password_list = []

    password_list += [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)

    pass_in.delete(0, END)
    pass_in.insert(0, f"{password}")
    pyperclip.copy(password)


def retrieve():
    web_data = web_in.get()
    user_data = user_in.get()
    pass_data = pass_in.get()

    new_data = {
        web_data: {
            "Username": user_data,
            "Password": pass_data
        }
    }

    user_confirm = False

    if len(web_data) == 0 or len(user_data) == 0 or len(pass_data) == 0:
        messagebox.showwarning(title="Field Empty", message="Don't leave any empty fields")
    else:
        user_confirm = messagebox.askyesno(title=f"{web_data}", message=f"Your Data: \nEmail: {user_data} \nPassword: "
                                                                        f"{pass_data} \nDo you want to save it?")
    if user_confirm:

        try:
            with open("Data.json", "r") as file:
                data = json.load(file)
                data.update(new_data)

            with open("Data.json", "w") as file:
                json.dump(data, file, indent=4)

        except FileNotFoundError:
            with open("Data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        finally:
            web_in.delete(0, END)
            user_in.delete(0, END)
            pass_in.delete(0, END)


def search():

    web_data = web_in.get()

    try:
        with open("Data.json", "r") as file:
            data = json.load(file)
            req_data = data[web_data]
            messagebox.showinfo(title=web_data, message=f"Username: {req_data['Username']}"
                                                        f"\nPassword: {req_data['Password']}")
    except KeyError:
        messagebox.showwarning(message="No data found.")
    except FileNotFoundError:
        messagebox.showwarning(message="No data found.")


window = Tk()
window.title("Password Manager")
window.config(padx=100, pady=100, bg="white")

logo = Canvas(width=200, height=200, background="white", highlightthickness=0)
icon = PhotoImage(file="logo.png")
logo.create_image(100, 100, image=icon)
logo.grid(row=0, column=0, columnspan=3)

website = Label(text="Website: ", font=(None, 10, "normal"), bg="white")
website.grid(row=1, column=0)

web_in = Entry(width=20)
web_in.focus()
web_in.grid(row=1, column=1)

search_button = Button(text="Search", command=search)
search_button.grid(row=1, column=2)

username = Label(text="Email/Username: ", font=(None, 10, "normal"), bg="white")
username.grid(row=2, column=0)

user_in = Entry(width=30)
user_in.grid(row=2, column=1, columnspan=2)

Password = Label(text="Password: ", font=(None, 10, "normal"), bg="white")
Password.grid(row=3, column=0)

pass_in = Entry(width=20)
pass_in.grid(row=3, column=1)

pass_generator = Button(text="Generate", command=generate_password)
pass_generator.grid(row=3, column=2)

add_button = Button(text="Add", width=25, command=retrieve)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
