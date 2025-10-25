# My ToDo Application
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import json
import os

# -------------------- Setup --------------------
ctk.set_appearance_mode("System")  # Options: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

TASK_FILE = "tasks.json"

# -------------------- Functions --------------------
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_tasks():
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f)

def add_task():
    task_text = entry.get()
    if task_text.strip() == "":
        messagebox.showwarning("Warning", "Task cannot be empty!")
        return
    tasks.append({"task": task_text, "done": False})
    update_listbox()
    entry.delete(0, tk.END)
    save_tasks()

def delete_task():
    try:
        selected_index = listbox.curselection()[0]
        tasks.pop(selected_index)
        update_listbox()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to delete")

def mark_done():
    try:
        selected_index = listbox.curselection()[0]
        tasks[selected_index]["done"] = not tasks[selected_index]["done"]
        update_listbox()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to mark done")

def update_listbox():
    listbox.delete(0, tk.END)
    for task in tasks:
        display_text = task["task"]
        if task["done"]:
            display_text += " ✅"
        listbox.insert(tk.END, display_text)

# -------------------- GUI --------------------
root = ctk.CTk()
root.title("Glassy To-Do App")
root.geometry("450x550")
root.resizable(False, False)

# Glassy Frame
main_frame = ctk.CTkFrame(root, corner_radius=20, fg_color="#1E1E1E")
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Title
title = ctk.CTkLabel(main_frame, text="📝 My To-Do List", font=ctk.CTkFont(size=24, weight="bold"))
title.pack(pady=(20,10))

# Entry
entry = ctk.CTkEntry(main_frame, placeholder_text="Add a new task...", width=350, height=40, corner_radius=15, border_width=1)
entry.pack(pady=(0,15))

# Buttons Frame
btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
btn_frame.pack(pady=(0,20))

add_btn = ctk.CTkButton(btn_frame, text="➕ Add", command=add_task, width=100, height=35, corner_radius=10, fg_color="#4CAF50", hover_color="#45A049")
add_btn.grid(row=0, column=0, padx=5)

delete_btn = ctk.CTkButton(btn_frame, text="🗑 Delete", command=delete_task, width=100, height=35, corner_radius=10, fg_color="#F44336", hover_color="#D32F2F")
delete_btn.grid(row=0, column=1, padx=5)

done_btn = ctk.CTkButton(btn_frame, text="✅ Done", command=mark_done, width=100, height=35, corner_radius=10, fg_color="#2196F3", hover_color="#1976D2")
done_btn.grid(row=0, column=2, padx=5)

# Listbox with scroll
list_frame = ctk.CTkFrame(main_frame, fg_color="#2E2E2E", corner_radius=15)
list_frame.pack(padx=10, pady=(0,20), fill="both", expand=True)

scrollbar = tk.Scrollbar(list_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

# Use a standard tkinter Listbox (customtkinter does not provide a CTkListbox)
listbox = tk.Listbox(list_frame, width=50, height=15, font=("Segoe UI", 12), bg="#2E2E2E", fg="white", selectbackground="#444444", activestyle="none", yscrollcommand=scrollbar.set)
listbox.pack(padx=10, pady=10, fill="both", expand=True)
scrollbar.configure(command=listbox.yview)

# Load tasks at start
tasks = load_tasks()
update_listbox()

root.mainloop()