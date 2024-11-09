import csv
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar

class UtilityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Utility Values Analyzer")
        
        self.utilities = {
            "MVM Gas": {"unit": "m3", "price": 100, "dictations": []},
            "MVM Electricity": {"unit": "kWh", "price": 100, "dictations": []},
            "Vízművek Water": {"unit": "m3", "price": 100, "dictations": []}
        }
        
        self.create_widgets()
        
    def create_widgets(self):
        self.utility_var = tk.StringVar(value="MVM Gas")
        self.price_var = tk.DoubleVar(value=100)
        self.value_var = tk.DoubleVar()
        self.date_var = tk.StringVar()
        
        utility_frame = ttk.LabelFrame(self.root, text="Select Utility")
        utility_frame.pack(fill="x", padx=10, pady=5)
        
        for utility in self.utilities.keys():
            ttk.Radiobutton(utility_frame, text=utility, variable=self.utility_var, value=utility).pack(side="left", padx=5, pady=5)
        
        entry_frame = ttk.LabelFrame(self.root, text="Enter Dictation")
        entry_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(entry_frame, text="Value:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(entry_frame, textvariable=self.value_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(entry_frame, text="Date:").grid(row=1, column=0, padx=5, pady=5)
        self.calendar = Calendar(entry_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(entry_frame, text="Save Dictation", command=self.save_dictation).grid(row=2, column=0, columnspan=2, pady=10)
        
        self.tree = ttk.Treeview(self.root, columns=("Utility", "Value", "Date", "Consumption", "Bill"), show="headings")
        self.tree.heading("Utility", text="Utility")
        self.tree.heading("Value", text="Value")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Consumption", text="Consumption")
        self.tree.heading("Bill", text="Bill (HUF)")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.create_csv_if_not_exists()
        self.load_data()
        self.value_var.set(0)
        self.calendar.selection_set(datetime.now().strftime("%Y-%m-%d"))
        
    def save_dictation(self):
        utility = self.utility_var.get()
        value = self.value_var.get()
        date = self.calendar.get_date()
        
        if value <= 0 or not date:
            messagebox.showerror("Error", "Please enter all fields")
            return
        
        dictation = {"value": value, "date": date, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        if self.utilities[utility]["dictations"]:
            last_dictation = self.utilities[utility]["dictations"][-1]
            consumption = value - last_dictation["value"]
        else:
            consumption = value
        
        bill = consumption * self.utilities[utility]["price"]
        
        dictation["consumption"] = consumption
        dictation["bill"] = bill
        
        self.utilities[utility]["dictations"].append(dictation)
        self.save_to_csv()
        self.load_data()
        
    def save_to_csv(self):
        with open("utility_data.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Utility", "Value", "Date", "Consumption", "Bill", "Timestamp"])
            for utility, data in self.utilities.items():
                for dictation in data["dictations"]:
                    writer.writerow([utility, dictation["value"], dictation["date"], dictation["consumption"], dictation["bill"], dictation["timestamp"]])
                    
    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        try:
            with open("utility_data.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if all(key in row and row[key] for key in ["Utility", "Value", "Date", "Consumption", "Bill"]):
                        self.tree.insert("", "end", values=(row["Utility"], float(row["Value"]), row["Date"], float(row["Consumption"]), float(row["Bill"])))
        except FileNotFoundError:
            pass
    def create_csv_if_not_exists(self):
        try:
            with open("utility_data.csv", "x", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Utility", "Value", "Date", "Consumption", "Bill", "Timestamp"])
        except FileExistsError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = UtilityApp(root)
    root.mainloop()