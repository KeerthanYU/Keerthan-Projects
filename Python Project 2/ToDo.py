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

def create_task_row(index, task):
    # Create frame for task row with hover effect
    task_frame = ctk.CTkFrame(scrollable_frame, fg_color="#2E2E2E", corner_radius=10)
    task_frame.pack(fill="x", padx=8, pady=4)
    
    # Configure grid columns - give more space to task text
    task_frame.grid_columnconfigure(1, weight=3)  # Task text gets more space
    task_frame.grid_columnconfigure(2, weight=0)  # Fixed width for status
    task_frame.grid_columnconfigure(3, weight=0)  # Fixed width for buttons
    task_frame.grid_columnconfigure(4, weight=0)  # Fixed width for buttons

    # Bind hover events for visual feedback
    def on_enter(e):
        task_frame.configure(fg_color="#363636")
    def on_leave(e):
        task_frame.configure(fg_color="#2E2E2E")
    
    task_frame.bind("<Enter>", on_enter)
    task_frame.bind("<Leave>", on_leave)

    # Task number with custom styling
    number_label = ctk.CTkLabel(
        task_frame, 
        text=f"{index}.", 
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#4CAF50" if task["done"] else "white"
    )
    number_label.grid(row=0, column=0, padx=(15,10), pady=10)

    # Task text with wrapping for long tasks
    task_text = f"{task['task']}"
    text_color = "#A0A0A0" if task["done"] else "white"
    
    # Create a text widget for better text wrapping
    task_label = ctk.CTkTextbox(
        task_frame,
        height=40,  # Adjust height dynamically based on content
        font=ctk.CTkFont(size=16, weight="normal"),
        fg_color="transparent",
        text_color=text_color,
        activate_scrollbars=False,
        wrap="word"  # Enable word wrapping
    )
    task_label.grid(row=0, column=1, padx=10, pady=(5,5), sticky="ew")
    
    # Insert the task text and make it read-only
    task_label.insert("1.0", task_text)
    task_label.configure(state="disabled")
    
    # Adjust height based on content
    line_count = task_label.get("1.0", "end-1c").count('\n') + 1
    task_label.configure(height=max(40, min(line_count * 25, 100)))

    # Status indicator
    status_label = ctk.CTkLabel(
        task_frame,
        text="✓" if task["done"] else "○",
        font=ctk.CTkFont(size=20),
        text_color="#4CAF50" if task["done"] else "#808080",
        width=30
    )
    status_label.grid(row=0, column=2, padx=(5,10), pady=10)

    # Mark done button with improved styling
    mark_btn = ctk.CTkButton(
        task_frame, 
        text="Done",
        width=70,
        height=32,
        corner_radius=8,
        fg_color="#4CAF50" if not task["done"] else "#45464F",
        hover_color="#45A049" if not task["done"] else "#363636",
        text_color="white",
        font=ctk.CTkFont(size=14, weight="bold"),
        command=lambda t=index-1: mark_done(t)
    )
    mark_btn.grid(row=0, column=3, padx=5, pady=10)

    # Delete button with improved styling
    delete_btn = ctk.CTkButton(
        task_frame, 
        text="🗑",
        width=40,
        height=32,
        corner_radius=8,
        fg_color="#F44336",
        hover_color="#D32F2F",
        font=ctk.CTkFont(size=16),
        command=lambda t=index-1: delete_task(t)
    )
    delete_btn.grid(row=0, column=4, padx=(5,15), pady=10)

    return task_frame

def delete_task(index=None):
    if index is not None:
        tasks.pop(index)
        update_listbox()
        save_tasks()

def mark_done(index=None):
    if index is not None:
        tasks[index]["done"] = not tasks[index]["done"]
        update_listbox()
        save_tasks()

def update_listbox():
    # Clear all existing task widgets
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    
    # Create new task rows
    for index, task in enumerate(tasks, 1):
        create_task_row(index, task)

# -------------------- GUI --------------------
root = ctk.CTk()
root.title(" To-Do App")
root.geometry("600x650")  # Increased window size for better task visibility
root.resizable(True, True)  # Allow window resizing to see long tasks
root.minsize(500, 500)  # Set minimum window size

# Glassy Frame
main_frame = ctk.CTkFrame(root, corner_radius=20, fg_color="#454242")
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Title
title = ctk.CTkLabel(main_frame, text="📝 My To-Do List", font=ctk.CTkFont(size=24, weight="bold"))
title.pack(pady=(20,10))

# Entry with improved styling
entry = ctk.CTkEntry(
    main_frame, 
    placeholder_text="Add a new task...", 
    width=350, 
    height=45, 
    corner_radius=12,
    border_width=2,
    font=ctk.CTkFont(size=16),
    placeholder_text_color="#808080"
)
entry.pack(pady=(0,15))

# Buttons Frame
btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
btn_frame.pack(pady=(0,20))

# Add button with enhanced style
add_btn = ctk.CTkButton(
    btn_frame, 
    text="Add Task", 
    command=add_task, 
    width=120, 
    height=40, 
    corner_radius=10, 
    fg_color="#4CAF50", 
    hover_color="#45A049",
    font=ctk.CTkFont(size=15, weight="bold")
)
add_btn.grid(row=0, column=0, padx=8)

# Clear all button
delete_btn = ctk.CTkButton(
    btn_frame, 
    text="Clear All", 
    command=lambda: [tasks.clear(), update_listbox(), save_tasks()], 
    width=100, 
    height=40, 
    corner_radius=10, 
    fg_color="#F44336", 
    hover_color="#D32F2F",
    font=ctk.CTkFont(size=15, weight="bold")
)
delete_btn.grid(row=0, column=1, padx=8)

# Task list with scroll
list_frame = ctk.CTkFrame(main_frame, fg_color="#262626", corner_radius=15)
list_frame.pack(padx=15, pady=(0,20), fill="both", expand=True)

# Create scrollable frame for tasks
scrollable_frame = ctk.CTkScrollableFrame(
    list_frame, 
    fg_color="transparent",
    corner_radius=10,
    scrollbar_button_hover_color="#404040",
    scrollbar_button_color="#333333"
)
scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Dictionary to store task frames and buttons
task_widgets = {}

# Load tasks at start
tasks = load_tasks()
update_listbox()

root.mainloop()