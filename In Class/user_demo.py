import tkinter as tk
import mysql.connector
from tkinter import messagebox

def get_users():
    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '782772',
            database = 'users'
        )

        cursor  = connection.cursor()
        cursor.execute("SELECT * FROM Users")
        users = cursor.fetchall()

        return users
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def create_gui():
    # Create the main window
    root = tk.Tk()
    root.title("MySQL User Query Application")

    # Create a Listbox to display user data
    listbox = tk.Listbox(root, width = 50, height = 10)
    listbox.pack(pady = 20)

    # Function to display data in the Listbox
    def load_data():
        users = get_users()
        listbox.delete(0, tk.END) # clear existing list box items
        for user in users:
            listbox.insert(tk.END, f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")

    # Create a button to load data
    load_button = tk.Button(root, text = "Load Users", command = load_data)
    load_button.pack()

    # start the tkinter event loop
    root.mainloop()

def main():
    create_gui()

if __name__ == "__main__":
    main()
