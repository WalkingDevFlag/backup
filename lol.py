import tkinter as tk

root = tk.Tk()
root.title("Calculator App")

# Create Input Fields
num1_label = tk.Label(root, text="Enter number 1: ")
num1_entry = tk.Entry(root)
operation_label = tk.Label(root, text="Enter operation: ")
operation_entry = tk.Entry(root)
result_label = tk.Label(root, text="Result:")

# Create Button
clear_button = tk.Button(root, text="Clear", command=clear_inputs)

# Layout
num1_label.grid(row=0, column=0)
num1_entry.grid(row=0, column=1)
operation_label.grid(row=1, column=0)
operation_entry.grid(row=1, column=1)
result_label.grid(row=2, column=0)
clear_button.grid(row=3, column=1)

def clear_inputs():
    num1_entry.delete(0, tk.END)
    operation_entry.delete(0, tk.END)
    result_label.config(text="")

root.mainloop()
