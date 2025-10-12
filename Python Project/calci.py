import customtkinter as ctk

# Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("CALCULATOR")
root.geometry("360x500")
root.resizable(False, False)

# Input field
entry = ctk.CTkEntry(root, font=("Arial", 28), justify="right",fg_color="white",text_color="black")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=20, ipady=10, sticky="nsew")

# Button click function
def on_click(btn_text):
    current = entry.get()
    if btn_text == "=":
        try:
            result = eval(current)
        except Exception:
            result = "Error"
        entry.delete(0, ctk.END)
        entry.insert(ctk.END, result)
    elif btn_text == "C":
        entry.delete(0, ctk.END)
    else:
        entry.insert(ctk.END, btn_text)

# Buttons layout
buttons = [
    ('7',1,0),('8',1,1),('9',1,2),('C',1,3),
    ('4',2,0),('5',2,1),('6',2,2),('*',2,3),
    ('1',3,0),('2',3,1),('3',3,2),('-',3,3),
    ('0',4,0),('.',4,1),('/',4,2),('+',4,3),
    ('=',5,0)
]

# Create buttons
for (text, row, col) in buttons:
    action = lambda x=text: on_click(x)
    
    if text == "=":
        # Bigger = button spanning 2 columns
        btn = ctk.CTkButton(root, text=text, font=("Arial", 22, "bold"),
                            fg_color="#21AC4F", corner_radius=20, command=action)
        btn.grid(row=row, column=col, columnspan=3, sticky="nsew", padx=5, pady=5)
    elif text == "C":
        btn = ctk.CTkButton(root, text=text, font=("Arial", 22, "bold"),
                            fg_color="#F84C08", corner_radius=20, command=action)
        btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
    elif text == "+":
        btn = ctk.CTkButton(root, text=text, font=("Arial", 22, "bold"),
                            fg_color="#31363D", corner_radius=20, command=action)
        btn.grid(row=row, column=col, rowspan=2, sticky="nsew", padx=5, pady=5)
    else:
        btn = ctk.CTkButton(root, text=text, font=("Arial", 22, "bold"),
                            fg_color="#31363D", corner_radius=20, command=action)
        btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

# Keyboard support
def key_event(event):
    key = event.char
    if key in "0123456789+-/*.": 
        entry.insert(ctk.END, key)
    elif key == "\r": 
        on_click("=")
    elif key == "\x08": 
        entry.delete(len(entry.get())-1)
    elif key.lower() == "c": 
        entry.delete(0, ctk.END)

root.bind("<Key>", key_event)

# Make rows and columns expand equally
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# Run the app
root.mainloop()
