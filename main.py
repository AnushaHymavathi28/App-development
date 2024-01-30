import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
from tkinter.font import Font
from PIL import Image, ImageTk
import os
import sqlite3

print("Current Working Directory:", os.getcwd())

def init_db():
    conn = sqlite3.connect('registration.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registration (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            dob TEXT,
            phone TEXT,
            address TEXT,
            category TEXT,
            sex TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()  # Call this function when your program starts


# Load images for the carousel
def load_images():
    image_folder = "images"
    target_size = (360, 200)  # Desired width and height of the images
    image_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith(".jpg")]
    images = []

    for image_file in image_files:
        # Open and resize the image
        img = Image.open(image_file)
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        # Convert to PhotoImage and add to the list
        photo_img = ImageTk.PhotoImage(img)
        images.append(photo_img)

    return images

# Change image for the carousel
def change_image():
    global current_image_index, img_label
    current_image_index = (current_image_index + 1) % len(images)
    img_label.config(image=images[current_image_index])
    root.after(3000, change_image)

def submit_form(name, dob, phone, address, category, sex):
    conn = sqlite3.connect('registration.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO registration (name, dob, phone, address, category, sex) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, dob, phone, address, category, sex))
    conn.commit()
    conn.close()

    # Show success message
    messagebox.showinfo("Success", "Registration successful")

# Open registration form
def open_registration_form():
    reg_window = tk.Toplevel(root)
    reg_window.title("Registration Form")
    reg_window.geometry("300x300")  # Adjust size as needed

    
    # Form fields
    tk.Label(reg_window, text="Name:").grid(row=0, column=0)
    name_entry = tk.Entry(reg_window)
    name_entry.grid(row=0, column=1)

    tk.Label(reg_window, text="DOB (YYYY-MM-DD):").grid(row=1, column=0)
    dob_entry = tk.Entry(reg_window)
    dob_entry.grid(row=1, column=1)

    tk.Label(reg_window, text="Phone Number:").grid(row=2, column=0)
    phone_entry = tk.Entry(reg_window)
    phone_entry.grid(row=2, column=1)

    tk.Label(reg_window, text="Address:").grid(row=3, column=0)
    address_entry = tk.Entry(reg_window)
    address_entry.grid(row=3, column=1)

    tk.Label(reg_window, text="Category:").grid(row=4, column=0)
    category_combobox = ttk.Combobox(reg_window, values=["Beginner", "Intermediate", "Advanced"])
    category_combobox.grid(row=4, column=1)

    tk.Label(reg_window, text="Sex:").grid(row=5, column=0)
    sex_combobox = ttk.Combobox(reg_window, values=["Male", "Female", "Other"])
    sex_combobox.grid(row=5, column=1)

    # Submit button in the registration form
    submit_btn = tk.Button(reg_window, text="Submit", command=lambda: submit_form(
        name_entry.get(), dob_entry.get(), phone_entry.get(), 
        address_entry.get(), category_combobox.get(), sex_combobox.get()))
    submit_btn.grid(row=6, column=1, pady=10)



# Main window
root = tk.Tk()
root.title("Martial Arts Class App")
root.geometry("360x640")  # Mobile-like interface size


# Set a theme for ttk
style = ttk.Style(root)
style.theme_use('clam')  # You can try different themes like 'alt', 'default', 'classic'

# Define custom fonts
title_font = Font(family="Arial", size=18, weight="bold")
button_font = Font(family="Arial", size=12)
text_font = Font(family="Arial", size=10)

# Define colors
bg_color = "#f0f0f0"
button_color = "#333333"
text_color = "#ffffff"
root.configure(bg=bg_color)

# Application title
title_label = tk.Label(root, text="AKASH MARTIAL ARTS CLUB", font=title_font, bg=bg_color, fg=button_color)
title_label.pack(pady=20)

# Custom styled buttons
style.configure('TButton', font=button_font, borderwidth=2, background=button_color)
style.map('TButton', foreground=[('active', text_color)], background=[('active', button_color)])

# Add a frame for buttons with a custom background color
button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(fill='x', padx=10)

# Define all your frames here, but don't pack them yet
image_frame = tk.Frame(root)
info_frame = tk.Frame(root)
about_us_frame = tk.Frame(root)
categories_frame = tk.Frame(root)

# Marquee Frame
marquee_frame = tk.Frame(root, height=30)  # Set a fixed height for the marquee frame
marquee_frame.pack(fill='x', expand=False)

# Marquee Label
marquee_text = "Karate is a martial art and way of life that trains a practitioner to be peaceful"
marquee_label = tk.Label(marquee_frame, text=marquee_text, font=('Helvetica', 10))
marquee_label.pack()

# Function to update the marquee position
def update_marquee():
    marquee_label.config(text=marquee_label.cget('text')[1:] + marquee_label.cget('text')[0])
    root.after(100, update_marquee)  # Adjust speed as necessary

update_marquee()  # Start the marquee

# Function to hide all frames
def hide_all_data_frames():
    about_us_frame.pack_forget()
    address_frame.pack_forget()
    categories_frame.pack_forget()
    instructors_frame.pack_forget()
    category_description_label.config(text="") 
# Function to show "About Us" information
def show_about_us_info():
    hide_all_data_frames()
    about_us_frame.pack(fill='both', expand=True)

# Function to show address information
def show_address_info():
    hide_all_data_frames()
    address_frame.pack(fill='both', expand=True) 

# Function to show category information
def show_category_info():
    hide_all_data_frames()
    categories_frame.pack(fill='both', expand=True)

# Function to show instructors information
def show_instructors_info():
    hide_all_data_frames()  # Hide all frames
    instructors_frame.pack(fill='both', expand=True)

# "About Us" Frame (Initially hidden)
about_us_frame = tk.Frame(root)
about_us_text = """Here at ‘AKASH MARTIAL ARTS‘ we are teaching martial arts - karate, kobudo, but more importantly, we promote character development and encourage every student to be their best. Self-defense and physical fitness have always been the focus of martial arts, and we offer a safe, structured, and fun environment to achieve this objective. Through the combination of great training and dedicated instructors.Director/Instructor – Manjunath Jain."""
tk.Label(about_us_frame, text=about_us_text, wraplength=300, justify="left").pack()
# Initially hide the "About Us" frame
about_us_frame.pack_forget()

# Address Frame (Initially hidden)
address_frame = tk.Frame(root)
address_content = """CALL US ON : 810544280
ADDRESS : Brigade Metropolis Arcade, Whitefield main road, Garudarchapalya, Mahadevapura bangalore.
WORKING HOURS: Monday, Wednesday 5pm to 6pm and Sunday 8am to 10 am"""
address_label = tk.Label(address_frame, text=address_content, wraplength=300, justify="left")
address_label.pack()

# Category descriptions
category_descriptions = {
    "Tiny Tigers": "Ages 3 to 6 years old (A fun and energetic class that focuses on balance, coordination, discipline, various tricks, footwork, sparing and self-defense.)",
    "Youth": "Ages 7 to 12 years old (Students begin to learn advanced martial arts skills with specific curriculum as a set of hand, kick and self-defense techniques).",
    "Adult": "Ages 13 and above (With traditional martial arts instructions the curriculum consists of form, hand techniques, kick techniques, weapons and sparing)"
}

# Categories tab setup
categories_tab_frame = tk.Frame(root)
categories_tab_frame.pack(fill='both', expand=True, padx=10, pady=10)


# Function to update the category description based on the selection
def update_category_description(event):
    selected_category = category_combobox.get()
    category_description_label.config(text=category_descriptions.get(selected_category, ""))

# Dropdown to select categories
category_combobox = ttk.Combobox(categories_frame, values=list(category_descriptions.keys()), state="readonly")
category_combobox.set("")  # Set initial value to empty
category_combobox.pack()
category_combobox.bind("<<ComboboxSelected>>", update_category_description)

# Label to display the category description
category_description_label = tk.Label(categories_tab_frame, text="", wraplength=300, justify="left")
category_description_label.pack(pady=10)

# Instructors Frame (Initially hidden)
instructors_frame = tk.Frame(root)
instructors_content = """
SHALINI: Kids instructor holding 2nd dan black belt
SENSEI AKASH JAIN: Youth instructor holding 3rd dan black belt, branch chief instructor, examiner, and national referee.
RENSHI MANJUNATH JAIN: Senior/adults instructor holding 7th dan black belt ruk dan kuro obi 7th dan black belt, kenpo martial arts, chief instructor and examiner, and international referee.
"""
instructors_label = tk.Label(instructors_frame, text=instructors_content, wraplength=300, justify="left")
instructors_label.pack()
# Initially hide the instructors frame
instructors_frame.pack_forget()

images = load_images()
current_image_index = 0

# Image carousel
img_label = tk.Label(root, image=images[0])
img_label.pack()

# Start cycling images
root.after(3000, change_image)

# Information sections
image_frame = tk.Frame(root)
image_frame.pack(fill='both', expand=True , padx=0, pady=0)
# Information sections
info_frame = tk.Frame(root)
info_frame.pack(fill='x')

tk.Button(info_frame, text="About Us", bg="lightgrey", command=show_about_us_info).pack(fill='x', padx=5, pady=2)
tk.Button(info_frame, text="Address", bg="lightgrey", command=show_address_info).pack(fill='x', padx=5, pady=2)
tk.Button(info_frame, text="Categories", bg="lightgrey", command=show_category_info).pack(fill='x', padx=5, pady=2)
tk.Button(info_frame, text="Instructors", bg="lightgrey",command=show_instructors_info).pack(fill='x', padx=5, pady=2)  # Add command if needed
## Add main application widgets here (e.g., a button to open the registration form)
register_btn = tk.Button(root, text="Register",bg="red" ,command=open_registration_form)
register_btn.pack(pady=10)

about_us_frame.pack(fill='both', expand=True)
about_us_frame.pack_forget()

categories_frame.pack(fill='both', expand=True)
categories_frame.pack_forget()

address_frame.pack(fill='both', expand=True)
address_frame.pack_forget()

instructors_frame.pack(fill='both', expand=True)
instructors_frame.pack_forget()

# Run the application
root.mainloop()
