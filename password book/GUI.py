import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from database import create_table, save_password, get_passwords, update_password, delete_password

def save_password_gui():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not website or not username or not password:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    save_password(website, username, password)

    clear_entries()
    messagebox.showinfo("Success", "Password saved successfully!")

def clear_entries():
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def show_passwords_gui():
    passwords = get_passwords()

    if not passwords:
        messagebox.showinfo("Info", "No passwords saved.")
        return

    # New window for displaying passwords
    show_window = tk.Toplevel(root)
    show_window.title("Saved Passwords")

    # Treeview widget for displaying passwords in a grid
    tree = ttk.Treeview(show_window)
    tree["columns"] = ("ID", "Website", "Username", "Password")
    tree.heading("#0", text="Index")
    tree.heading("ID", text="ID")
    tree.heading("Website", text="Website")
    tree.heading("Username", text="Username")
    tree.heading("Password", text="Password")

    for i, row in enumerate(passwords):
        tree.insert("", i, values=(row[0], row[1], row[2], "********"))

    tree.pack(expand=True, fill="both")

    # Search functionality
    def search_passwords():
        search_text = search_entry.get().lower()
        tree.delete(*tree.get_children())
        for i, row in enumerate(passwords):
            if search_text in row[1].lower():  # Search based on website name
                tree.insert("", i, values=(row[0], row[1], row[2], "********"))

    # Search Entry and Button
    search_label = tk.Label(show_window, text="Search:")
    search_entry = tk.Entry(show_window)
    search_button = tk.Button(show_window, text="Search", command=search_passwords)

    search_label.pack(pady=5)
    search_entry.pack(pady=5)
    search_button.pack(pady=10)

def update_password_gui():
    password_id = ask_password_id()

    if password_id is not None:
        new_password = ask_new_password()
        if new_password is not None:
            update_password(password_id, new_password)
            messagebox.showinfo("Success", "Password updated successfully!")

def delete_password_gui():
    password_id = ask_password_id()

    if password_id is not None:
        delete_password(password_id)
        messagebox.showinfo("Success", "Password deleted successfully!")

def ask_password_id():
    password_id = simpledialog.askinteger("Password ID", "Enter the ID of the password:")
    return password_id

def ask_new_password():
    new_password = simpledialog.askstring("New Password", "Enter the new password:")
    return new_password

# Main GUI
root = tk.Tk()
root.title("Password Book")

# Create the table if not exists
create_table()

# Configure grid
for i in range(3):
    root.columnconfigure(i, weight=1)

for i in range(7):
    root.rowconfigure(i, weight=1)

# Widgets
website_label = tk.Label(root, text="Website:")
username_label = tk.Label(root, text="Username:")
password_label = tk.Label(root, text="Password:")

website_entry = tk.Entry(root)
username_entry = tk.Entry(root)
password_entry = tk.Entry(root, show="*")

save_button = tk.Button(root, text="Save Password", command=save_password_gui)
show_button = tk.Button(root, text="Show Passwords", command=show_passwords_gui)
update_button = tk.Button(root, text="Update Password", command=update_password_gui)
delete_button = tk.Button(root, text="Delete Password", command=delete_password_gui)

# Grid layout
website_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
username_label.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
password_label.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

website_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
username_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
password_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

save_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
show_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")
update_button.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
delete_button.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

root.mainloop()



