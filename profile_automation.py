# import tkinter as tk
# from tkinter import messagebox
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import chromedriver_autoinstaller
# import time

# # Function for Task 1: Navigate to Portfolio site and download
# def run_task1():
#     # Automatically install and set up ChromeDriver
#     chromedriver_autoinstaller.install()
#     driver = webdriver.Chrome()

#     try:
#         # Step 1: Navigate to the Portfolio Website
#         driver.get("https://portfolio-f7afe.web.app/")
#         time.sleep(5)  # Wait for the page to load

#         # Step 2: Scroll down to make the download button visible
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
#         time.sleep(2)  # Wait for scrolling to complete

#         # Step 3: Locate and click the download button using XPath
#         download_button = driver.find_element(By.XPATH, '//*[@id="resume"]/div[2]/div/p/a')
#         download_button.click()  # Click the download button
#         time.sleep(5)  # Wait for the next page to load (Google Drive)

#         # Step 4: Handle Google Drive File Download
#         driver.get("https://drive.google.com/file/d/1pcCgOl_oHeb89riL71VyFHx2zeGIOQRd/view?usp=sharing")
#         time.sleep(5)  # Wait for the page to load

#         # Locate the download icon and click it
#         download_icon = driver.find_element(By.XPATH, '//div[@aria-label="Download"]')
#         download_icon.click()  # Click the download icon
#         time.sleep(5)  # Wait for the download to complete

#         # Show a success message
#         messagebox.showinfo("Success", "Task 1: File downloaded successfully!")

#     except Exception as e:
#         # Handle errors
#         messagebox.showerror("Error", f"Task 1 Error: {e}")

#     finally:
#         # Close the browser
#         driver.quit()

# # Create the Tkinter GUI
# root = tk.Tk()
# root.title("Task 1 Automation")

# # Add a label
# label = tk.Label(root, text="Click the button to execute Task 1:", font=("Helvetica", 12))
# label.pack(pady=10)

# # Add a Task 1 button
# task1_button = tk.Button(root, text="Task 1", command=run_task1, bg="blue", fg="white", font=("Helvetica", 12))
# task1_button.pack(pady=10)

# # Add an Exit button
# exit_button = tk.Button(root, text="Exit", command=root.destroy, bg="red", fg="white", font=("Helvetica", 12))
# exit_button.pack(pady=10)

# # Run the Tkinter event loop
# root.mainloop()
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function for Task 1: Navigate to Portfolio site and download
def run_task1():
    # Set up ChromeDriver using ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Step 1: Navigate to the Portfolio Website
        driver.get("https://portfolio-f7afe.web.app/")
        time.sleep(5)  # Wait for the page to load

        # Step 2: Scroll down to make the download button visible
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom of the page
        time.sleep(2)  # Wait for scrolling to complete

        # Step 3: Locate and click the download button using XPath
        download_button = driver.find_element(By.XPATH, '//*[@id="resume"]/div[2]/div/p/a')
        download_button.click()  # Click the download button
        time.sleep(5)  # Wait for the next page to load (Google Drive)

        # Step 4: Handle Google Drive File Download
        driver.get("https://drive.google.com/file/d/1pcCgOl_oHeb89riL71VyFHx2zeGIOQRd/view?usp=sharing")
        time.sleep(5)  # Wait for the page to load

        # Locate the download icon and click it
        download_icon = driver.find_element(By.XPATH, '//div[@aria-label="Download"]')
        download_icon.click()  # Click the download icon
        time.sleep(5)  # Wait for the download to complete

        # Show a success message
        messagebox.showinfo("Success", "Task 1: File downloaded successfully!")

    except Exception as e:
        # Handle errors
        messagebox.showerror("Error", f"Task 1 Error: {e}")

    finally:
        # Close the browser
        driver.quit()

# Create the Tkinter GUI
root = tk.Tk()
root.title("Task 1 Automation")

# Add a label
label = tk.Label(root, text="Click the button to execute Task 1:", font=("Helvetica", 12))
label.pack(pady=10)

# Add a Task 1 button
task1_button = tk.Button(root, text="Task 1", command=run_task1, bg="blue", fg="white", font=("Helvetica", 12))
task1_button.pack(pady=10)

# Add an Exit button
exit_button = tk.Button(root, text="Exit", command=root.destroy, bg="red", fg="white", font=("Helvetica", 12))
exit_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()