import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import time


def create_menu_table():
    with sqlite3.connect('minute_burger.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             product_name TEXT NOT NULL,
             price REAL NOT NULL,
             quantity INTEGER NOT NULL)
        ''')


def create_orders_table():
    with sqlite3.connect('minute_burger.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             customer_name TEXT NOT NULL,
             product_name TEXT NOT NULL, 
             price REAL NOT NULL,
             quantity INTEGER NOT NULL,
             total REAL NOT NULL)
        ''')


def set_background_image(window, image_path):
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    background_label = tk.Label(window, image=photo)
    background_label.image = photo  # To prevent garbage collection
    background_label.place(relwidth=1, relheight=1)

    return background_label


def authenticate_user(username, password):
    clearance_type = 'Guest'
    cleared = False
    if username == "MinuteBurger" and password == 'admin123':
        cleared = True
        clearance_type = "Admin"
    elif username == "Guest" and password == "Guest":
        cleared = True

    return cleared, clearance_type


def open_main_window():
    login_window.destroy()
    root.deiconify()


admin_type = "Guest"


def login():
    global admin_type
    username = username_entry.get()
    password = password_entry.get()

    login_result, admin_type = authenticate_user(username, password)
    print(login_result, admin_type)
    if login_result:
        open_main_window()
    else:
        messagebox.showerror("Authentication Failed", "Invalid username or password. Please try again.")

    create_main_window(admin_type)



def view_menu():
    with sqlite3.connect('minute_burger.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM menu')
        data = cursor.fetchall()
    return data


def update_treeview(menu_data=None):
    if menu_data is None:
        menu_data = view_menu()

    tree.delete(*tree.get_children())
    for row in menu_data:
        tree.insert('', 'end', values=row)


def bubble_sort_by_price():
    menu_data = view_menu()
    n = len(menu_data)

    for i in range(n):
        for j in range(0, n - i - 1):
            if menu_data[j][2] > menu_data[j + 1][2]:  # Compare based on price (assuming index 2 is the price)
                menu_data[j], menu_data[j + 1] = menu_data[j + 1], menu_data[j]
                update_treeview_with_delay(menu_data)


def gnome_sort_by_price():
    menu_data = view_menu()
    i, size = 1, len(menu_data)

    def gnome_sort_step():
        nonlocal i
        if i < size:
            i = gnome_sort_by_price_step(menu_data, i)
            root.after(100, gnome_sort_step)
        else:
            update_treeview(menu_data)

    gnome_sort_step()


def update_treeview_with_delay(menu_data):
    update_treeview(menu_data)
    root.update()
    time.sleep(0.1)  # Adjust the delay as needed


def bubble_sort_by_price_step(menu_data, i, j):
    if menu_data[j][2] > menu_data[j + 1][2]:  # Compare based on price (assuming index 2 is the price)
        menu_data[j], menu_data[j + 1] = menu_data[j + 1], menu_data[j]
        update_treeview_with_delay(menu_data)
    return i, j + 1


def gnome_sort_by_price_step(menu_data, i):
    if i == 0 or menu_data[i][2] >= menu_data[i - 1][2]:  # Compare based on price
        return i + 1
    else:
        menu_data[i], menu_data[i - 1] = menu_data[i - 1], menu_data[i]
        update_treeview_with_delay(menu_data)
        return i - 1


def open_order_window():
    order_window = tk.Toplevel(root)
    order_window.title("Place Order")
    background_label = set_background_image(order_window,
                                            "burger.jpg")

    window_width = 800
    window_height = 600
    order_window.geometry(f"{window_width}x{window_height}")

    tk.Label(order_window, text="Customer Name:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10,
                                                                               sticky="w")

    customer_name_entry = tk.Entry(order_window, font=("Helvetica", 12))
    customer_name_entry.grid(row=0, column=0, padx=5, pady=10)

    # Create a Treeview for menu display
    tree_menu = ttk.Treeview(order_window)
    tree_menu['columns'] = ('product_name', 'price')

    tree_menu.heading("#0", text="Index")
    tree_menu["show"] = "headings"
    tree_menu.heading('product_name', text='Product Name')
    tree_menu.heading('price', text='Price')

    column_widths = {'product_name': 200, 'price': 100}
    for col, width in column_widths.items():
        tree_menu.column(col, width=width, minwidth=width, anchor=tk.CENTER)

    tree_menu_height = 12
    tree_menu['height'] = tree_menu_height
    tree_menu.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    tree_menu_scrollbar = ttk.Scrollbar(order_window, orient="vertical", command=tree_menu.yview)
    tree_menu.configure(yscroll=tree_menu_scrollbar.set)
    tree_menu_scrollbar.grid(row=1, column=2, pady=10, sticky="ns")

    tree_menu.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

    # Function to populate tree_menu with menu items
    def populate_menu():
        menu_data = view_menu()
        for item in menu_data:
            tree_menu.insert('', 'end', values=(item[1], item[2]))

    # Call the populate_menu function to load menu items
    populate_menu()

    # Create a Treeview for customer orders
    tree_order = ttk.Treeview(order_window)
    tree_order['columns'] = ('product_name', 'price', 'quantity', 'total')

    tree_order.heading("#0", text="Index")
    tree_order["show"] = "headings"
    tree_order.heading('product_name', text='Product Name')
    tree_order.heading('price', text='Price')
    tree_order.heading('quantity', text='Quantity')
    tree_order.heading('total', text='Total')

    # Configure column widths
    column_widths_order = {'product_name': 200, 'price': 100, 'quantity': 100, 'total': 100}
    for col, width in column_widths_order.items():
        tree_order.column(col, width=width, minwidth=width, anchor=tk.CENTER)

    # Create a vertical scrollbar for the treeview
    tree_order_scrollbar = ttk.Scrollbar(order_window, orient="vertical", command=tree_order.yview)
    tree_order.configure(yscroll=tree_order_scrollbar.set)
    tree_order_scrollbar.grid(row=3, column=2, pady=10, sticky="ns")

    # Place the treeview widget using grid
    tree_order.grid(row=3, column=0, columnspan=2, padx=12, pady=10, sticky="nsew")

    # Configure row and column weights for expandability
    order_window.grid_rowconfigure(1, weight=1)
    order_window.grid_columnconfigure(0, weight=1)
    order_window.grid_columnconfigure(2, weight=1)

    tk.Label(order_window, text="Quantity:", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")

    quantity_entry = tk.Entry(order_window, font=("Helvetica", 12))
    quantity_entry.grid(row=2, column=0, padx=1, pady=10)

    def add_to_order():
        selected_item = tree_menu.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a menu item to add to the order.")
            return
        menu_item = tree_menu.item(selected_item, 'values')
        price = float(menu_item[1])  # Convert price to float
        quantity = int(quantity_entry.get())
        total = price * quantity
        tree_order.insert('', 'end', values=(menu_item[0], price, quantity, total))

    add_to_order_button = tk.Button(order_window, text="Add to Order", command=add_to_order, font=("Helvetica", 12))
    add_to_order_button.grid(row=2, column=1, padx=1, pady=10, sticky="w")

    order_window.columnconfigure(3, weight=1)

    def place_order():
        if tree_order.get_children():
            customer_name = customer_name_entry.get()
            conn = sqlite3.connect('minute_burger.db')
            cursor = conn.cursor()

            for item in tree_order.get_children():
                order_data = tree_order.item(item, 'values')

                # Update the quantity in the menu table
                cursor.execute('''
                    UPDATE menu
                    SET quantity = quantity - ?
                    WHERE product_name = ?
                    ''', (order_data[2], order_data[0]))

                # Insert the order into the orders table
                cursor.execute('''
                    INSERT INTO orders (customer_name, product_name, price, quantity, total)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (customer_name, order_data[0], order_data[1], order_data[2], order_data[3]))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Order placed successfully")
            order_window.destroy()
            populate_menu()  # Refresh the menu tree
            update_treeview()  # Refresh the main menu tree
        else:
            messagebox.showwarning("Warning", "Please add items to the order before placing it.")

    place_order_button = tk.Button(order_window, text="Place Order", command=place_order, font=("Helvetica", 12))
    place_order_button.grid(row=2, column=2, padx=1, pady=10, sticky="w")


def add_menu_item():
    def save_menu_item():
        try:
            with sqlite3.connect('minute_burger.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO menu (product_name, price, quantity)
                    VALUES (?, ?, ?)
                ''', (product_name_entry.get(), price_entry.get(), quantity_entry.get()))
                conn.commit()
            messagebox.showinfo("Success", "Menu item added successfully")
            add_window.destroy()
            update_treeview()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    add_window = tk.Toplevel(root)
    add_window.title("Add Menu Item")

    tk.Label(add_window, text="Product Name:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10,
                                                                            sticky="w")
    tk.Label(add_window, text="Price:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    tk.Label(add_window, text="Quantity:", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")

    product_name_entry = tk.Entry(add_window, font=("Helvetica", 12))
    product_name_entry.grid(row=0, column=1, padx=10, pady=10)
    price_entry = tk.Entry(add_window, font=("Helvetica", 12))
    price_entry.grid(row=1, column=1, padx=10, pady=10)
    quantity_entry = tk.Entry(add_window, font=("Helvetica", 12))
    quantity_entry.grid(row=2, column=1, padx=10, pady=10)

    save_button = tk.Button(add_window, text="Save", command=save_menu_item, font=("Helvetica", 12))
    save_button.grid(row=3, column=0, columnspan=2, pady=10)


def change_menu_item():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a menu item to change.")
        return

    existing_data = tree.item(selected_item, 'values')

    def update_menu_item():
        try:
            with sqlite3.connect('minute_burger.db') as conn:
                cursor = conn.cursor()

                update_query = '''
                    UPDATE menu
                    SET product_name=?, price=?, quantity=?
                    WHERE id=?
                '''
                new_data = [entry_widgets[field].get() for field in fields]
                new_data.append(existing_data[0])
                cursor.execute(update_query, tuple(new_data))

                conn.commit()
            messagebox.showinfo("Success", "Menu item updated successfully")
            change_window.destroy()
            update_treeview()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    change_window = tk.Toplevel(root)
    change_window.title("Change Menu Item")

    fields = ['product_name', 'price', 'quantity']
    entry_widgets = {}

    for i, field in enumerate(fields):
        tk.Label(change_window, text=field.replace('_', ' '), font=("Helvetica", 12)).grid(row=i, column=0, padx=10,
                                                                                           pady=10, sticky="w")
        entry_widgets[field] = tk.Entry(change_window, font=("Helvetica", 12))
        entry_widgets[field].insert(0, existing_data[i])
        entry_widgets[field].grid(row=i, column=1, padx=10, pady=10)

    update_button = tk.Button(change_window, text="Update Menu Item", command=update_menu_item, font=("Helvetica", 12))
    update_button.grid(row=len(fields), columnspan=2, pady=10)


def delete_menu_item():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a menu item to delete.")
        return

    confirmation = messagebox.askyesno("Confirm", "Are you sure you want to delete this menu item?")
    if confirmation:
        with sqlite3.connect('minute_burger.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM menu WHERE id=?', (tree.item(selected_item, 'values')[0],))
            conn.commit()
        messagebox.showinfo("Success", "Menu item deleted successfully")
        update_treeview()


def exit_app():
    root.destroy()


root = tk.Tk()
root.title("MinuteBurger Menu Management")

background_label = set_background_image(root, "burger2.jpg")

# Global variable to track login status and admin type
logged_in = False

# Login window
login_window = tk.Toplevel(root)
login_window.title("Login")

tk.Label(login_window, text="Welcome to MinuteBurger!", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2,
                                                                                     pady=10)

tk.Label(login_window, text="Username:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
tk.Label(login_window, text="Password:", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")

username_entry = tk.Entry(login_window, font=("Helvetica", 12))
username_entry.grid(row=1, column=1, padx=10, pady=10)
password_entry = tk.Entry(login_window, font=("Helvetica", 12), show="*")
password_entry.grid(row=2, column=1, padx=10, pady=10)

login_button = tk.Button(login_window, text="Login", command=login, font=("Helvetica", 12))
login_button.grid(row=3, column=0, columnspan=2, pady=10)

# Names below the username and password in the login window
tk.Label(login_window, text="Group 7:", font=("Helvetica", 8)).grid(row=4, column=0, columnspan=2, pady=2)

names = ["Miranda, Shenelyn", "Siervo, Jenelyn C.", "Punzalan, Timotie John"]

for i, name in enumerate(names):
    tk.Label(login_window, text=name, font=("Helvetica", 8)).grid(row=5 + i, column=0, columnspan=2, pady=1)

# Hide the main window until the user logs in
root.withdraw()

tree = ttk.Treeview(root)
tree['columns'] = ('id', 'product_name', 'price', 'quantity')

tree.heading("#0", text="Index")
tree["show"] = "headings"
tree.heading('id', text='ID')
tree.heading('product_name', text='Product Name')
tree.heading('price', text='Price')
tree.heading('quantity', text='Quantity')

column_widths = {'id': 50, 'product_name': 200, 'price': 100, 'quantity': 100}
for col, width in column_widths.items():
    tree.column(col, width=width, minwidth=width, anchor=tk.CENTER)

tree_height = 28
tree['height'] = tree_height

update_treeview()

tree.pack(pady=10, padx=10)
print(f"{admin_type=}")


def create_main_window(admin_type):
    if admin_type == "Admin":
        add_button = tk.Button(root, text="Add Menu Item", command=add_menu_item, font=("Helvetica", 12))
        add_button.pack(side=tk.LEFT, padx=5)

        change_button = tk.Button(root, text="Change Menu Item", command=change_menu_item, font=("Helvetica", 12))
        change_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(root, text="Delete Menu Item", command=delete_menu_item, font=("Helvetica", 12))
        delete_button.pack(side=tk.LEFT, padx=5)

    order_button = tk.Button(root, text="Place Order", command=open_order_window, font=("Helvetica", 12))
    order_button.pack(side=tk.LEFT, padx=5)

    # Create buttons for sorting menu items by price
    bubble_sort_button = tk.Button(root, text="Bubble Sort by Price", command=bubble_sort_by_price, font=("Helvetica", 12))
    bubble_sort_button.pack(side=tk.LEFT, padx=5)

    gnome_sort_button = tk.Button(root, text="Gnome Sort by Price", command=gnome_sort_by_price, font=("Helvetica", 12))
    gnome_sort_button.pack(side=tk.LEFT, padx=5)

    exit_button = tk.Button(root, text="Exit", command=exit_app, font=("Helvetica", 12))
    exit_button.pack(side=tk.LEFT, padx=5)

root.mainloop()


