import customtkinter as ctk

# Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("CALCULATOR")
root.geometry("400x600")
root.resizable(True, True)

# Input/Output field
entry = ctk.CTkTextbox(root, font=("Arial", 22), fg_color="white", text_color="black")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=20, sticky="nsew")
entry.insert("1.0", "")  # start empty

# Flag to know if last input was a result
last_was_result = False

# Button click function
def on_click(btn_text):
    global last_was_result

    if last_was_result and btn_text not in ("=", "C"):
        entry.insert("end", "\n")
        last_was_result = False

    if btn_text == "=":
        try:
            lines = entry.get("1.0", "end").strip().split("\n")
            expression = lines[-1]
            result = eval(expression)
        except Exception:
            result = "Error"
        entry.insert("end", f"\n= {result}")
        entry.see("end")
        last_was_result = True
    elif btn_text == "C":
        entry.delete("1.0", "end")  # Corrected
        last_was_result = False
    else:
        entry.insert("end", btn_text)

# Buttons layout
buttons = [
    ('7',1,0),('8',1,1),('9',1,2),('C',1,3),
    ('4',2,0),('5',2,1),('6',2,2),('*',2,3),
    ('1',3,0),('2',3,1),('3',3,2),('-',3,3),
    ('0',4,0),('.',4,1),('/',4,2),('+',4,3),
    ('(',5,0),(')',5,1),('=',5,2)
]

# Create buttons
for (text, row, col) in buttons:
    action = lambda x=text: on_click(x)
    
    if text == "=":
        btn = ctk.CTkButton(root, text=text, font=("Arial", 22, "bold"),
                            fg_color="#21AC4F", corner_radius=20, command=action)
        btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=5, pady=5)
    elif text == "C":
        btn = ctk.CTkButton(root, text=text, font=("Arial", 22, "bold"),
                            fg_color="#F84C08", corner_radius=20, command=action)
        btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
    else:
        btn = ctk.CTkButton(root, text=text, font=("Arial", 22, "bold"),
                            fg_color="#31363D", corner_radius=20, command=action)
        btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

# Keyboard support
def key_event(event):
    global last_was_result
    if event.char in "0123456789+-*/.()":
        if last_was_result:
            entry.insert("end", "\n")
            last_was_result = False
        entry.insert("end", event.char)
        return "break"
    elif event.keysym == "Return":
        on_click("=")
        return "break"
    elif event.keysym == "BackSpace":
        current = entry.get("1.0", "end")
        if len(current) > 1:
            entry.delete(f"{ctk.END}-2c", "end")
        return "break"
    elif event.char.lower() == "c":
        entry.delete("1.0", "end")  # Corrected
        last_was_result = False
        return "break"

root.bind("<Key>", key_event)

# Make rows and columns expand equally
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

root.mainloop()
