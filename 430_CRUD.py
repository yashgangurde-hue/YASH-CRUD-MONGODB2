import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["bike_db"]
collection = db["bikes"]

# Insert Function
def insert_bike():
    try:
        data = {
            "_id": entry_id.get(),
            "model": entry_model.get(),
            "brand": entry_brand.get(),
            "price": float(entry_price.get())
        }
        collection.insert_one(data)
        messagebox.showinfo("Success", "Bike inserted successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Insert failed:\n{e}")

# Read Function
def read_bike():
    bike_id = entry_id.get()
    data = collection.find_one({"_id": bike_id})
    if data:
        entry_model.delete(0, tk.END)
        entry_model.insert(0, data['model'])
        entry_brand.delete(0, tk.END)
        entry_brand.insert(0, data['brand'])
        entry_price.delete(0, tk.END)
        entry_price.insert(0, str(data['price']))
    else:
        messagebox.showwarning("Not Found", "Bike not found")

# Update Function
def update_bike():
    bike_id = entry_id.get()
    new_data = {
        "model": entry_model.get(),
        "brand": entry_brand.get(),
        "price": float(entry_price.get())
    }
    result = collection.update_one({"_id": bike_id}, {"$set": new_data})
    if result.modified_count > 0:
        messagebox.showinfo("Success", "Bike updated successfully")
    else:
        messagebox.showwarning("Not Found", "Bike not found or no changes made")

# Delete Function
def delete_bike():
    bike_id = entry_id.get()
    result = collection.delete_one({"_id": bike_id})
    if result.deleted_count > 0:
        messagebox.showinfo("Deleted", "Bike deleted successfully")
    else:
        messagebox.showwarning("Not Found", "Bike not found")

# GUI Setup
root = tk.Tk()
root.title("Bike Management System")
root.geometry("400x300")

# Labels and Entries
tk.Label(root, text="Bike ID").grid(row=0, column=0, padx=10, pady=5)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1)

tk.Label(root, text="Model").grid(row=1, column=0, padx=10, pady=5)
entry_model = tk.Entry(root)
entry_model.grid(row=1, column=1)

tk.Label(root, text="Brand").grid(row=2, column=0, padx=10, pady=5)
entry_brand = tk.Entry(root)
entry_brand.grid(row=2, column=1)

tk.Label(root, text="Price").grid(row=3, column=0, padx=10, pady=5)
entry_price = tk.Entry(root)
entry_price.grid(row=3, column=1)

# Buttons
tk.Button(root, text="Insert", command=insert_bike).grid(row=4, column=0, pady=10)
tk.Button(root, text="Read", command=read_bike).grid(row=4, column=1)
tk.Button(root, text="Update", command=update_bike).grid(row=5, column=0)
tk.Button(root, text="Delete", command=delete_bike).grid(row=5, column=1)

root.mainloop()
