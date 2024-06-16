import tkinter as tk

def on_click(event):
    text = event.widget.cget("text")
    if text == "=":
        try:
            result = eval(entry.get())
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception as e:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    elif text == "C":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, text)

# Create the main window
root = tk.Tk()
root.title("Simple Calculator")

# Create an entry widget to display input and results
entry = tk.Entry(root, width=20, borderwidth=5)
entry.grid(row=0, column=0, columnspan=4)

# Define the buttons
buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "C", "0", "=", "+"
]

# Add buttons to the calculator
row = 1
col = 0
for button_text in buttons:
    button = tk.Button(root, text=button_text, padx=20, pady=10)
    button.grid(row=row, column=col)
    button.bind("<Button-1>", on_click)
    col += 1
    if col > 3:
        col = 0
        row += 1

root.mainloop()
