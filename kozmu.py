import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkcalendar import DateEntry
import os
from datetime import datetime

# Constants
CSV_FILE = "utility_data.csv"
DEFAULT_RATE = 100  # Default price in HUF per m3 or kWh

# Initialize CSV file if not present
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Utility", "Date", "Previous Value", "Current Value", "Consumption", "Rate", "Bill Amount", "Last Modified"])
    df.to_csv(CSV_FILE, index=False)

# Load data from CSV
def load_data():
    try:
        return pd.read_csv(CSV_FILE)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")
        return pd.DataFrame(columns=["Utility", "Date", "Previous Value", "Current Value", "Consumption", "Rate", "Bill Amount", "Last Modified"])

# Save data to CSV
def save_data(df):
    try:
        df.to_csv(CSV_FILE, index=False)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")

# Calculate consumption and bill amount
def calculate_consumption_and_bill(utility, current_value, rate):
    df = load_data()
    previous_value = 0

    # Check the latest previous value for the selected utility
    utility_data = df[df["Utility"] == utility].sort_values(by="Date", ascending=False)
    if not utility_data.empty:
        previous_value = pd.to_numeric(utility_data.iloc[0]["Current Value"], errors='coerce')
        if pd.isna(previous_value):
            previous_value = 0

    consumption = current_value - previous_value
    bill_amount = consumption * rate
    return previous_value, consumption, bill_amount

# Add a new dictation
def add_dictation():
    try:
        utility = utility_menu.get()
        if utility == "Select Utility":
            raise ValueError("Please select a utility.")

        date = calendar.get_date()
        current_value = simpledialog.askinteger("Current Value", "Enter the current dictation value:")
        if current_value is None or current_value < 0:
            raise ValueError("Invalid current value.")

        rate = simpledialog.askfloat("Rate", f"Enter the price per unit (default: {DEFAULT_RATE} HUF):", initialvalue=DEFAULT_RATE)
        if rate is None or rate <= 0:
            raise ValueError("Invalid rate value.")

        # Calculate consumption and bill amount
        previous_value, consumption, bill_amount = calculate_consumption_and_bill(utility, current_value, rate)
        last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create a new DataFrame for the new entry
        new_data = pd.DataFrame({
            "Utility": [utility],
            "Date": [date],
            "Previous Value": [previous_value],
            "Current Value": [current_value],
            "Consumption": [consumption],
            "Rate": [rate],
            "Bill Amount": [bill_amount],
            "Last Modified": [last_modified]
        })

        # Concatenate the new data and save
        df = load_data()
        df = pd.concat([df, new_data], ignore_index=True)
        save_data(df)
        messagebox.showinfo("Success", "Dictation added successfully!")
        display_data()

    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add dictation: {e}")

# Display data in the table
def display_data():
    try:
        for row in tree.get_children():
            tree.delete(row)

        df = load_data()
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to display data: {e}")

# Edit an existing dictation
def edit_dictation():
    try:
        selected_item = tree.selection()[0]
        values = tree.item(selected_item, "values")
        index = tree.index(selected_item)

        # Ask for new values
        date = simpledialog.askstring("Date", "Enter the date (YYYY-MM-DD):", initialvalue=values[1])
        current_value = simpledialog.askinteger("Current Value", "Enter the current dictation value:", initialvalue=int(values[3]))
        rate = simpledialog.askfloat("Rate", "Enter the price per unit:", initialvalue=float(values[5]))

        if current_value is None or current_value < 0 or rate is None or rate <= 0:
            raise ValueError("Invalid input values.")

        # Load data and update
        df = load_data()
        df.at[index, "Date"] = date
        df.at[index, "Current Value"] = current_value
        df.at[index, "Rate"] = rate

        # Recalculate consumption and bill amount
        previous_value, consumption, bill_amount = calculate_consumption_and_bill(df.at[index, "Utility"], current_value, rate)
        df.at[index, "Previous Value"] = previous_value
        df.at[index, "Consumption"] = consumption
        df.at[index, "Bill Amount"] = bill_amount
        df.at[index, "Last Modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        save_data(df)
        messagebox.showinfo("Success", "Dictation edited successfully!")
        display_data()

    except IndexError:
        messagebox.showerror("Error", "Please select a dictation to edit!")
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to edit dictation: {e}")

# Delete a dictation
def delete_dictation():
    try:
        selected_item = tree.selection()[0]
        index = tree.index(selected_item)

        # Load data and delete
        df = load_data()
        df = df.drop(index)
        save_data(df)
        messagebox.showinfo("Success", "Dictation deleted successfully!")
        display_data()

    except IndexError:
        messagebox.showerror("Error", "Please select a dictation to delete!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete dictation: {e}")

# GUI setup
root = tk.Tk()
root.title("Utility Dictation Management")

# Utility selection menu
utility_menu = ttk.Combobox(root, values=["MVM Gas", "MVM Electricity", "Vízművek Water"])
utility_menu.set("Select Utility")
utility_menu.pack(pady=10)

# Calendar widget for date selection
calendar = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2)
calendar.pack(pady=10)

# Table setup
tree = ttk.Treeview(root, columns=["Utility", "Date", "Previous Value", "Current Value", "Consumption", "Rate", "Bill Amount", "Last Modified"], show="headings")
for col in tree["columns"]:
    tree.heading(col, text=col)
tree.pack(pady=20)

# Buttons for operations
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Dictation", command=add_dictation)
add_button.grid(row=0, column=0, padx=5)

edit_button = tk.Button(button_frame, text="Edit Dictation", command=edit_dictation)
edit_button.grid(row=0, column=1, padx=5)

delete_button = tk.Button(button_frame, text="Delete Dictation", command=delete_dictation)
delete_button.grid(row=0, column=2, padx=5)

# Display initial data
display_data()

root.mainloop()
