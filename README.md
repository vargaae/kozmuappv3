 <div align="center">
  <img alt="Application image" src="https://cssh.northeastern.edu/informationethics/wp-content/uploads/sites/44/2020/07/ai@2x.png" width="400" />
</div>
<br>
  <div align="center">
    <img src="https://img.shields.io/badge/-Python-black?style=for-the-badge&logoColor=white&logo=python&color=61DAFB" alt="Python" />
</div>

# UTILITY ( Közmű ) APPLICATION v3

This project demonstrates a fully functional Python application with a GUI, data persistence, and robust error handling.
A robust Python program that provides a graphical user interface (GUI) using tkinter, enabling the user to manage and analyze utility values. The program offers functionality to add, edit, and delete dictation values, calculates consumption and bill amounts, and saves the data in a CSV file. It includes error handling to ensure the program can handle unexpected inputs or file errors.

## 🚀IDEA - PROMPT

- Create a working python program with error handling for displaying and analyzing utility values ​​with visual display and saving to a CSV file. Sum up the dictation values on every save and modification ​​of the utilities in m3, kWh, their sums, the difference between the two most recent dictation values, i.e. the consumption (consumption value is updating on every savings or modifyings. for consumption read the previous dictation value from the last saved dictation by the dictation date, if there is a saved dictation for the given utility, if there is none, then to 0 calculate the consumption in comparison), dictation dates (the dictation date can be selected from the calendar), the last save date (save a time stamp, but for later changes save the date of the last change), display the amount of bills arising from the consumption calculated from these dictations in HUF, for which the m3 /kWh price can be entered (initial value HUF 100/m3 - enter this as the default value, so if you do not enter another value, then calculate with this) and you can enter the new dictations and the amount of the invoices, these will be listed and the saved data can be edit, modify, delete and save. It should include MVM Gas, MVM Electricity, Vízművek Water dictation, we can select these from a menu when dictating the values. Display MVM Gas, MVM Electricity, Vízművek Water dictations in separate section rows.

- (+ use concat instead of append function)

- main.py > this version is generated with ChatGPT ( GPT 4.0 )
- kozmu-copilot.py > this version is generated with Github Copilot

## Key Features of the Program

- 🚀Error Handling: The program uses try-except blocks to catch and handle errors gracefully, ensuring the user is informed when an issue occurs.
- 🚀GUI with tkinter: A user-friendly graphical interface is provided for managing utility values.
- 🚀Date Selection: The tkcalendar library is used for selecting dictation dates via a calendar widget.
- 🚀Data Management with pandas: Data is loaded, manipulated, and saved efficiently using pandas.
- 🚀Data Persistence: Utility values are saved to a CSV file named utility_data.csv, making the data persistent between program runs.
- 🚀Modular Code: The program is organized into functions, making it easy to maintain and extend.

## Libraries Used

- 🚀pandas: For data manipulation and saving/loading CSV files.
- 🚀tkinter: For the graphical user interface.
- 🚀tkcalendar: For the date picker widget.

## Functionality

- 🚀Add Dictation: Adds a new utility dictation entry with the current date, values, and calculates consumption and the bill amount.
- 🚀Edit Dictation: Edits an existing dictation entry and updates the CSV file.
- 🚀Delete Dictation: Deletes an entry from the CSV file.
- 🚀Display Data: Shows the data in a table format using ttk.Treeview.

## Data Handling

- 🚀File Handling: The data is saved in a CSV file (utility_data.csv). The program initializes the CSV file if it does not exist and saves data after every operation.
- 🚀Default Values: The default rate is set to 100 HUF per m3 or kWh, but this can be modified by the user when adding or editing a dictation.

- 🚀Consumption Calculation: The program calculates consumption as the difference between the current and previous dictation values. Consumption and bill amounts are recalculated whenever a dictation is added or modified.

## Issues - TODO

- Now the program calculates consumption as the difference between the current and previous dictation values. It would work better, if the program would calculate consumption as the difference between the current dictation and the earlier date's dictation value.

## Debugging - Changes

Certainly! I have modified the code to use pd.concat() instead of append() for adding new data to the DataFrame. This ensures better performance and adheres to the more modern practices in pandas.

### Key Changes

- Used pd.concat(): Replaced the append() method with pd.concat() for adding new data to the DataFrame.

- Explanation: pd.concat() is more efficient and the recommended method over append(), especially for future versions of pandas where append() might be deprecated.

### Notes

- This version ensures better performance and compatibility with future updates to the pandas library.

- The rest of the functionality, such as adding, editing, and deleting dictations, and calculating consumption and bill amounts, remains unchanged.

**Requirements**
Install Dependencies:
You need to install the pandas and tkcalendar libraries if you haven't already:

```bash
pip install pandas tkcalendar

```

**How to Run the Program**
Make sure Python is installed on your system.
Install the required libraries using the command above.
Run the script in your Python environment.
Use the interface to manage utility dictation values, including adding, editing, and deleting entries.

**Running the Project**
1.Run the script in your Python environment.
2.Use the dropdown menu to select a utility.
3.Use the date picker to select a dictation date.
4.Click the "Add Dictation" button to input new readings.
5.Select a row in the table to edit or delete it.
This project serves as a good portfolio project for Python developers, demonstrating skills in GUI development, data management, and CSV file handling.

```bash
python main.py

```

**Saved data**
Example for utility_data.csv - delete, if you want to start a fully new dictation:

```bash
Utility,Date,Previous Value,Current Value,Consumption,Rate,Bill Amount,Last Modified
MVM Electricity,2024-11-07,0,100,100,100.0,10000.0,2024-11-09 02:52:52
MVM Electricity,2024-11-09,100,200,100,100.0,10000.0,2024-11-09 02:53:11
MVM Electricity,2024-11-09,200,1000,800,100.0,80000.0,2024-11-09 02:57:57

```
