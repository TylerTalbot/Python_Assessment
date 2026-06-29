#------------------------------------------------------------------------------------------------------------------------------------------------------
# This is place for all my imports


import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


#------------------------------------------------------------------------------------------------------------------------------------------------------


root = tk.Tk()
root.geometry("450x650") # Expanded slightly to fit the table layout comfortably
root.grid_columnconfigure(2, weight=1)
root.title("Party Hire Shop")
root.configure(bg='grey')
customers = []


#------------------------------------------------------------------------------------------------------------------------------------------------------
# This is my space for all of my lists, constants, and dictionaries
# I have categorized each of the products into dictionaries for a more organized approach


PRICING = {
    #Furniture
    "Chairs": 2, "Tables": 5,
    #Tableware
    "Plates": 3, "Cups": 1, "Napkins": 1,
    #Cutlery
    "Forks": 1, "Knives": 1, "Spoons": 1,
    #Audio/Visual
    "Speakers": 10, "Projectors": 10, "Microphones": 10,
    #Entertainment
    "Bouncy Castles": 20, "Clowns": 15, "Magicians": 15
}


MAX_STOCK_FOR_EACH_PRODUCT_AVAILABLE = 500


#------------------------------------------------------------------------------------------------------------------------------------------------------
# This is my name input for the program


title_label = tk.Label(root, text="Please enter your information: ", font=("sans-serif", 14, "bold"), bg="grey")
title_label.grid(row=0, column=0, columnspan=4, pady=10)


#------------------------------------------------------------------------------------------------------------------------------------------------------
# This is a title describing the product amounts for each product


stock_label = tk.Label(root, text="There are 500 items for each product", font=("sans-serif", 14, "bold"), bg="grey")
stock_label.grid(row=1, column=0, columnspan=4, pady=10)


#------------------------------------------------------------------------------------------------------------------------------------------------------
# First Name


tk.Label(root, text="Name: ", fg="black", bg="grey", font=("sans-serif", 14, "bold")).grid(row=2, column=1, padx=10, pady=5)
name_entry = tk.Entry(root, bg="darkgrey", width=15)
name_entry.grid(row=3, column=1, padx=10, pady=5)


#------------------------------------------------------------------------------------------------------------------------------------------------------
# This is the input for the user to input their last Name


tk.Label(root, text="Last Name: ", fg="black", bg="grey", font=("sans-serif", 14, "bold")).grid(row=2, column=2, padx=10, pady=5)
last_name_entry = tk.Entry(root, bg="darkgrey", width=15)
last_name_entry.grid(row=3, column=2, padx=10, pady=5)


#------------------------------------------------------------------------------------------------------------------------------------------------------
# This is my input for the user to input how much of an item they want


tk.Label(root, text="Item Amount:", fg="black", bg="grey", font=("sans-serif", 14, "bold")).grid(row=4, column=1, padx=10, pady=5)
item_entry = tk.Entry(root, bg="darkgrey", width=15)
item_entry.grid(row=5, column=1, padx=10, pady=5)


#------------------------------------------------------------------------------------------------------------------------------------------------------
# This is my drop down menu for the user to select what products they want to purchase


tk.Label(root, text="Select Item: ", fg="black", bg="grey", font=("sans-serif", 14, "bold")).grid(row=4, column=2, padx=10, pady=5)
item_dropdown = ttk.Combobox(root, values=list(PRICING.keys()), state="readonly", width=15)
item_dropdown.grid(row=5, column=2, padx=10, pady=5)
item_dropdown.current(0)


#-------------------------------------------------------------------------------------------------------------------------------------------------------
# Treeview UI table to visually list out our hired items (Meets list printing standard)


what = ttk.Treeview(root, columns=("First Name", "Last Name", "Item", "Amount"), show="headings", height=6)
what.heading("First Name", text="First Name")
what.heading("Last Name", text="Last Name")
what.heading("Item", text="Item")
what.heading("Amount", text="Amount")


# Sizing table columns to keep them inside our window frame
what.column("First Name", width=100)
what.column("Last Name", width=100)
what.column("Item", width=100)
what.column("Amount", width=60)
what.grid(row=7, column=1, columnspan=2, pady=10, padx=10)


#-------------------------------------------------------------------------------------------------------------------------------------------------------
# This is the part of my code that handles the user's entries and tracks it locally!


def submit_order():
    first_name = name_entry.get().strip().title()
    last_name = last_name_entry.get().strip().title()
    selected_item = item_dropdown.get()
    quantity_raw = item_entry.get().strip()
   
    # Validation boundary logic
    if not first_name or not last_name or not quantity_raw:
        messagebox.showerror("Input Error", "All fields must be filled out before submitting.")
        return


    try:
        quantity = int(quantity_raw)
        if quantity <= 0:
            messagebox.showerror("Input Error", "Item Amount must be greater than 0.")
            return
        elif quantity > MAX_STOCK_FOR_EACH_PRODUCT_AVAILABLE:
            messagebox.showerror("Input Error", f"We only have {MAX_STOCK_FOR_EACH_PRODUCT_AVAILABLE} items available.")
            return
    except ValueError:
        messagebox.showerror("Input Error", "Item Amount must be a valid whole number.")
        return


    # Add transaction details to our visible table grid
    what.insert("", "end", values=(first_name, last_name, selected_item, quantity))
    messagebox.showinfo("Success", "Order added to the track list successfully!")


#-------------------------------------------------------------------------------------------------------------------------------------------------------
# Function to fulfill the specific standard task of deleting an active record item


def delete_item():
    selected_row = what.selection() # Find out which row the user highlighted
    if not selected_row:
        messagebox.showwarning("Selection Error", "Please click on an item in the list below to select and delete it.")
        return
   
    for item in selected_row:
        what.delete(item) # Safely drop item entry row from track list
    messagebox.showinfo("Deleted", "Selected item entry removed successfully.")


#-------------------------------------------------------------------------------------------------------------------------------------------------------
# Function to output final summary file from current tracking table entries (Data Privacy handling)


def download_receipts():
    all_records = what.get_children()
    if not all_records:
        messagebox.showwarning("File Error", "There are no entries in your active list to save.")
        return
       
    with open("receipt.txt", "w") as file:
        file.write("..... CURRENT PARTY SUPPLIES HIRE LOG ..... \n\n")
        for record_id in all_records:
            row_values = what.item(record_id)['values']
            file.write(f"Customer Name: {row_values[0]} {row_values[1]}\n")
            file.write(f"Item Selected: {row_values[2]}\n")
            file.write(f"Item Quantity: {row_values[3]}\n")
            file.write("-" * 40 + "\n")
           
    messagebox.showinfo("Saved", "All active list receipts downloaded successfully to receipt.txt!")


#------------------------------------------------------------------------------------------------------------------------------------------------------
# Action Buttons configurations layout row mounts


submit_button = tk.Button(root, text="Add Order Entry", bg="darkgrey", font=("sans-serif", 11, "bold"), command=submit_order)
submit_button.grid(row=6, column=1, padx=5, pady=5)


delete_button = tk.Button(root, text="Delete Selected", bg="darkgrey", font=("sans-serif", 11, "bold"), command=delete_item)
delete_button.grid(row=6, column=2, padx=5, pady=5)


download_button = tk.Button(root, text="Download All Receipts File", bg="darkgrey", font=("sans-serif", 12, "bold"), command=download_receipts)
download_button.grid(row=8, column=1, columnspan=2, pady=10)


#------------------------------------------------------------------------------------------------------------------------------------------------------
# this is the end of the code, where I place my root.mainloop to conclude the code!


root.mainloop()


#------------------------------------------------------------------------------------------------------------------------------------------------------
