# Description: This script is a simple GUI application that allows users to login, select a process category and process, and execute the process. The process involves searching for an image based on a user input query, saving the image to a specified output path, and sending the image as an email attachment. The process categories and processes are predefined in the script. The user login information is stored in a text file for verification. The GUI is created using Tkinter.
import os
import tkinter as tk
from tkinter import messagebox, ttk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import win32com.client

# Constants
USER_FILE = "user.txt"
OUTPUT_PATH = r"D:\New folder (2)\working python projects\outlook\process\Manufacturing\Assembly\output"
EMAIL_RECEIVER = "bvhss2024@outlook.com"
WINDOW_SIZE = "800x600"
BG_COLOR = "#2C3E50"
FG_COLOR = "#ECF0F1"
BUTTON_COLOR = "#3498DB"
CATEGORY_PROCESSES = {
    "Manufacturing": ["Assembly", "Testing"],
    "Quality": ["Inspection", "Certification"]
}

# Function to check or create user
def check_or_create_user(user_id, password):
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            f.write(f"{user_id},{password}\n")
        return True
    
    with open(USER_FILE, "r") as f:
        users = f.readlines()
    
    for user in users:
        stored_id, stored_pass = user.strip().split(",")
        if stored_id == user_id and stored_pass == password:
            return True
    return False

# Function to save the image directly
def save_image(search_query):
    try:
        os.makedirs(OUTPUT_PATH, exist_ok=True)  # Ensure output path exists
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(f"https://www.google.com/search?q={search_query}&tbm=isch")
        time.sleep(2)

        # Locate and download the first image
        images = driver.find_elements(By.CSS_SELECTOR, "img")
        for img in images:
            src = img.get_attribute("src")
            if not src:  # If `src` is None, try `data-src`
                src = img.get_attribute("data-src")
            if src and src.startswith("http"):  # Ensure the URL is valid
                response = requests.get(src)
                output_file = os.path.join(OUTPUT_PATH, "image.jpg")
                with open(output_file, "wb") as f:
                    f.write(response.content)
                print(f"Image saved at {output_file}")
                break
        else:
            print("No valid image source found.")
            return False

        driver.quit()
        return True
    except Exception as e:
        print(f"Error saving image: {e}")
        return False

# Function to send email
def send_email():
    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)
        mail.To = EMAIL_RECEIVER
        mail.Subject = "Downloaded Image"
        mail.Body = "Please find the downloaded image attached."

        # Attach the downloaded image
        for file in os.listdir(OUTPUT_PATH):
            file_path = os.path.join(OUTPUT_PATH, file)
            mail.Attachments.Add(file_path)

        mail.Send()
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# GUI Functions
def login_gui():
    def attempt_login():
        user_id = user_entry.get()
        password = pass_entry.get()
        if check_or_create_user(user_id, password):
            root.destroy()
            process_gui()
        else:
            messagebox.showerror("Login Failed", "Incorrect User ID or Password kindly check with txt file")

    root = tk.Tk()
    root.geometry(WINDOW_SIZE)
    root.title("User Login")
    root.configure(bg=BG_COLOR)
    
    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(pady=150)
    
    tk.Label(frame, text="User ID", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=10)
    user_entry = tk.Entry(frame, font=("Arial", 12))
    user_entry.grid(row=0, column=1)
    
    tk.Label(frame, text="Password", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=10)
    pass_entry = tk.Entry(frame, show="*", font=("Arial", 12))
    pass_entry.grid(row=1, column=1)
    
    login_btn = tk.Button(frame, text="Login", command=attempt_login, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold"), width=15)
    login_btn.grid(row=2, column=0, columnspan=2, pady=20)
    
    root.mainloop()

def process_gui():
    def update_process_dropdown(event):
        selected_category = category_var.get()
        process_dropdown["values"] = CATEGORY_PROCESSES.get(selected_category, [])
        process_var.set("")
    
    def start_process():
        category = category_var.get()
        process = process_var.get()
        if process == "Assembly":
            root.destroy()
            assembly_gui(category, process)
        else:
            messagebox.showinfo("Information", f"You selected: {process}")

    def exit_process():
        root.destroy()
        login_gui()

    root = tk.Tk()
    root.geometry(WINDOW_SIZE)
    root.title("Process Selection")
    root.configure(bg=BG_COLOR)
    
    category_var = tk.StringVar()
    process_var = tk.StringVar()
    
    tk.Label(root, text="Category", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14, "bold")).pack(pady=10)
    category_dropdown = ttk.Combobox(root, textvariable=category_var, values=list(CATEGORY_PROCESSES.keys()), font=("Arial", 12))
    category_dropdown.pack()
    category_dropdown.bind("<<ComboboxSelected>>", update_process_dropdown)
    
    tk.Label(root, text="Process", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14, "bold")).pack(pady=10)
    process_dropdown = ttk.Combobox(root, textvariable=process_var, font=("Arial", 12))
    process_dropdown.pack()
    
    start_btn = tk.Button(root, text="Start", command=start_process, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold"), width=15)
    start_btn.pack(pady=20)

    exit_btn = tk.Button(root, text="Exit", command=exit_process, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold"), width=15)
    exit_btn.pack(pady=10)
    
    root.mainloop()

def assembly_gui(category, process):
    def execute_process():
        search_query = search_entry.get()
        status_label.config(text="Processing...", fg="orange")
        if save_image(search_query) and send_email():
            status_label.config(text="Process Completed", fg="green")
        else:
            status_label.config(text="Process Failed", fg="red")

    def exit_to_process_gui():
        root.destroy()
        process_gui()

    root = tk.Tk()
    root.geometry(WINDOW_SIZE)
    root.title("Assembly Process Execution")
    root.configure(bg=BG_COLOR)

    tk.Label(root, text=f"Output Path: {OUTPUT_PATH}", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(root, text=f"Category: {category} | Process: {process}", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold")).pack(pady=10)
    tk.Label(root, text="Enter Search Query:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14, "bold")).pack(pady=10)

    search_entry = tk.Entry(root, font=("Arial", 12))
    search_entry.pack(pady=5)

    run_btn = tk.Button(root, text="Run", command=execute_process, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold"), width=15)
    run_btn.pack(pady=20)

    exit_btn = tk.Button(root, text="Exit", command=exit_to_process_gui, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold"), width=15)
    exit_btn.pack(pady=10)

    status_label = tk.Label(root, text="Awaiting Input", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold"))
    status_label.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    login_gui()

# import os
# import tkinter as tk
# from tkinter import messagebox, ttk
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# import requests
# import win32com.client

# # Constants
# USER_FILE = "user.txt"
# OUTPUT_PATH = r"D:\New folder (2)\working python projects\outlook\process\Manufacturing\Assembly\output"
# EMAIL_RECEIVER = "bvhss2024@outlook.com"
# WINDOW_SIZE = "800x600"
# BG_COLOR = "#2C3E50"
# FG_COLOR = "#ECF0F1"
# BUTTON_COLOR = "#3498DB"
# CATEGORY_PROCESSES = {
#     "Manufacturing": ["Assembly", "Testing"],
#     "Quality": ["Inspection", "Certification"]
# }

# # Function to check or create user
# def check_or_create_user(user_id, password):
#     if not os.path.exists(USER_FILE):
#         with open(USER_FILE, "w") as f:
#             f.write(f"{user_id},{password}\n")
#         return True
    
#     with open(USER_FILE, "r") as f:
#         users = f.readlines()
    
#     for user in users:
#         stored_id, stored_pass = user.strip().split(",")
#         if stored_id == user_id and stored_pass == password:
#             return True
#     return False

# # Function to save the image directly
# def save_image(search_query):
#     try:
#         os.makedirs(OUTPUT_PATH, exist_ok=True)  # Ensure output path exists
#         service = Service(ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service)
#         driver.get(f"https://www.google.com/search?q={search_query}&tbm=isch")
#         time.sleep(2)

#         # Locate and download the first image
#         images = driver.find_elements(By.CSS_SELECTOR, "img")
#         for img in images:
#             src = img.get_attribute("src")
#             if not src:  # If `src` is None, try `data-src`
#                 src = img.get_attribute("data-src")
#             if src and src.startswith("http"):  # Ensure the URL is valid
#                 response = requests.get(src)
#                 output_file = os.path.join(OUTPUT_PATH, "image.jpg")
#                 with open(output_file, "wb") as f:
#                     f.write(response.content)
#                 print(f"Image saved at {output_file}")
#                 break
#         else:
#             print("No valid image source found.")
#             return False

#         driver.quit()
#         return True
#     except Exception as e:
#         print(f"Error saving image: {e}")
#         return False

# # Function to send email
# def send_email():
#     try:
#         outlook = win32com.client.Dispatch("Outlook.Application")
#         mail = outlook.CreateItem(0)
#         mail.To = EMAIL_RECEIVER
#         mail.Subject = "Downloaded Image"
#         mail.Body = "Please find the downloaded image attached."

#         # Attach the downloaded image
#         for file in os.listdir(OUTPUT_PATH):
#             file_path = os.path.join(OUTPUT_PATH, file)
#             mail.Attachments.Add(file_path)

#         mail.Send()
#         print("Email sent successfully!")
#         return True
#     except Exception as e:
#         print(f"Error sending email: {e}")
#         return False

# # GUI Functions
# def login_gui():
#     def attempt_login():
#         user_id = user_entry.get()
#         password = pass_entry.get()
#         if check_or_create_user(user_id, password):
#             root.destroy()
#             process_gui()
#         else:
#             messagebox.showerror("Login Failed", "Incorrect User ID or Password")

#     root = tk.Tk()
#     root.geometry(WINDOW_SIZE)
#     root.title("User Login")
#     root.configure(bg=BG_COLOR)
    
#     frame = tk.Frame(root, bg=BG_COLOR)
#     frame.pack(pady=150)
    
#     tk.Label(frame, text="User ID", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=10)
#     user_entry = tk.Entry(frame, font=("Arial", 12))
#     user_entry.grid(row=0, column=1)
    
#     tk.Label(frame, text="Password", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=10)
#     pass_entry = tk.Entry(frame, show="*", font=("Arial", 12))
#     pass_entry.grid(row=1, column=1)
    
#     login_btn = tk.Button(frame, text="Login", command=attempt_login, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold"), width=15)
#     login_btn.grid(row=2, column=0, columnspan=2, pady=20)
    
#     root.mainloop()

# def process_gui():
#     def update_process_dropdown(event):
#         selected_category = category_var.get()
#         process_dropdown["values"] = CATEGORY_PROCESSES.get(selected_category, [])
#         process_var.set("")
    
#     def start_process():
#         category = category_var.get()
#         process = process_var.get()
#         if process == "Assembly":
#             root.destroy()
#             assembly_gui(category, process)
#         else:
#             messagebox.showinfo("Information", f"You selected: {process}")

#     def exit_process():
#         root.destroy()
#         login_gui()

#     root = tk.Tk()
#     root.geometry(WINDOW_SIZE)
#     root.title("Process Selection")
#     root.configure(bg=BG_COLOR)
    
#     category_var = tk.StringVar()
#     process_var = tk.StringVar()
    
#     tk.Label(root, text="Category", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14, "bold")).pack(pady=10)
#     category_dropdown = ttk.Combobox(root, textvariable=category_var, values=list(CATEGORY_PROCESSES.keys()), font=("Arial", 12))
#     category_dropdown.pack()
#     category_dropdown.bind("<<ComboboxSelected>>", update_process_dropdown)
    
#     tk.Label(root, text="Process", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14, "bold")).pack(pady=10)
#     process_dropdown = ttk.Combobox(root, textvariable=process_var, font=("Arial", 12))
#     process_dropdown.pack()
    
#     start_btn = tk.Button(root, text="Start", command=start_process, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold"), width=15)
#     start_btn.pack(pady=20)

#     exit_btn = tk.Button(root, text="Exit", command=exit_process, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold"), width=15)
#     exit_btn.pack(pady=10)
    
#     root.mainloop()

# def assembly_gui(category, process):
#     def execute_process():
#         search_query = search_entry.get()
#         status_label.config(text="Processing...", fg="orange")
#         if save_image(search_query) and send_email():
#             status_label.config(text="Process Completed", fg="green")
#         else:
#             status_label.config(text="Process Failed", fg="red")

#     def exit_to_process_gui():
#         root.destroy()
#         process_gui()

#     root = tk.Tk()
#     root.geometry(WINDOW_SIZE)
#     root.title("Assembly Process Execution")
#     root.configure(bg=BG_COLOR)

#     tk.Label(root, text=f"Output Path: {OUTPUT_PATH}", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold")).pack(pady=5)
#     tk.Label(root, text=f"Category: {category} | Process: {process}", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold")).pack(pady=10)
#     tk.Label(root, text="Enter Search Query:", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 14, "bold")).pack(pady=10)

#     search_entry = tk.Entry(root, font=("Arial", 12))
#     search_entry.pack(pady=5)

#     run_btn = tk.Button(root, text="Run", command=execute_process, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold"), width=15)
#     run_btn.pack(pady=20)

#     exit_btn = tk.Button(root, text="Exit", command=exit_to_process_gui, bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold"), width=15)
#     exit_btn.pack(pady=10)

#     status_label = tk.Label(root, text="Awaiting Input", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold"))
#     status_label.pack(pady=5)

#     root.mainloop()

# if __name__ == "__main__":
#     login_gui()
