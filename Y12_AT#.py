import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
import json
import os  
from scipy.stats import rankdata
import hashlib

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# Ensure data.json exists
if not os.path.exists("data.json"):
    with open("data.json", "w") as f:
        json.dump({}, f)

app = ctk.CTk()
app.geometry("1100x900")
app.title("Student Marks Program")

def clear_window():
    for widget in app.winfo_children():
        widget.destroy()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def sign_up():
    clear_window()
    username = ctk.CTkEntry(app, placeholder_text="Enter username", width=200, height=40, font=("Arial", 16))
    username.pack(pady=(20, 10))
    password = ctk.CTkEntry(app, placeholder_text="Enter password", width=200, height=40, font=("Arial", 16), show="*")
    password.pack(pady=(10, 20))

    def confirm_signup():
        saved_username = username.get()
        saved_password = password.get()
        if not saved_username or not saved_password:
            label = ctk.CTkLabel(app, text="Username and password cannot be empty.", font=("Arial", 16), text_color="red")
            label.pack(pady=(10, 20))
            return
        with open("data.json", "r") as f:
            data = json.load(f)
        if saved_username in data:
            label = ctk.CTkLabel(app, text="Username already exists. Please try again.", font=("Arial", 16), text_color="red")
            label.pack(pady=(10, 20))
        else:
            # Store the hashed password
            data[saved_username] = hash_password(saved_password)
            with open("data.json", "w") as f:
                json.dump(data, f, indent=4)
            label = ctk.CTkLabel(app, text="Sign up successful! Please log in.", font=("Arial", 16), text_color="green")
            label.pack(pady=(10, 20))

    confirm = ctk.CTkButton(app, text="Confirm", width=200, height=40, font=("Arial", 16), command=confirm_signup)
    confirm.pack(pady=(10, 20))

    back = ctk.CTkButton(app, text="Back to Login", width=200, height=40, font=("Arial", 16), command=login)
    back.pack(pady=(10, 20))

def login():
    clear_window()
    username = ctk.CTkEntry(app, placeholder_text="Enter username", width=200, height=40, font=("Arial", 16))
    username.pack(pady=(20, 10))
    password = ctk.CTkEntry(app, placeholder_text="Enter password", width=200, height=40, font=("Arial", 16), show="*")
    password.pack(pady=(10, 20))

    def confirm_login():
        login_username = username.get()
        login_password = password.get()
        if not login_username or not login_password:
            label = ctk.CTkLabel(app, text="Username and password cannot be empty.", font=("Arial", 16), text_color="red")
            label.pack(pady=(10, 20))
            return
        with open("data.json", "r") as f:
            data = json.load(f)
        # Compare the hash of the entered password with the stored hash
        if login_username in data and data[login_username] == hash_password(login_password):
            master_program()
        else:
            label = ctk.CTkLabel(app, text="Invalid username or password. Please try again.", font=("Arial", 16), text_color="red")
            label.pack(pady=(10, 20))

    confirm = ctk.CTkButton(app, text="Confirm", width=200, height=40, font=("Arial", 16), command=confirm_login)
    confirm.pack(pady=(10, 20))

    signup = ctk.CTkButton(app, text="Sign Up", width=200, height=40, font=("Arial", 16), command=sign_up)
    signup.pack(pady=(10, 20))

def master_program():
    clear_window()

    title_label = ctk.CTkLabel(app, text="Student Marks Program 📚", font=("Calibri", 28, "bold"))
    title_label.pack(pady=(20, 10))

    # Subject input
    subject_entry_frame = ctk.CTkFrame(app)
    subject_entry_frame.pack(pady=(10, 0))

    subject_entry = ctk.CTkEntry(subject_entry_frame, placeholder_text="Enter new subject")
    subject_entry.pack(side="left", padx=(0, 10))

    tabview = ctk.CTkTabview(app)
    tabview.pack(padx=10, pady=10, fill="both", expand=True)

    subject_tabs = {}

    class SubjectTab:
        def __init__(self, parent, subject_name):
            self.parent = parent
            self.subject_name = subject_name
            self.text_boxes = []
            self.name_boxes = []
            self.values = []
            self.data_dict = {}

            # Frame for entry rows
            self.scrollable_frame = ctk.CTkScrollableFrame(parent)
            self.scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True) 



            # Frame for results
            self.scrollable_frame_2 = ctk.CTkScrollableFrame(parent)
            self.scrollable_frame_2.pack(pady=10, padx=10, fill="both", expand=True)

            # Button row
            button_frame = ctk.CTkFrame(parent)
            button_frame.pack(pady=10)

            button_add_row = ctk.CTkButton(button_frame, text="Add name & mark", command=self.add_entry_row, font=("Calibri", 16))
            button_add_row.pack(side="left", padx=5)

            button_run = ctk.CTkButton(button_frame, text="Show frequency histogram", command=self.get_entries, font=("Calibri", 16))
            button_run.pack(side="left", padx=5)

            extra_button = ctk.CTkButton(button_frame, text="Show individual marks", command=self.extra_graph, font=("Calibri", 16))
            extra_button.pack(side="left", padx=5)

            calc_button = ctk.CTkButton(button_frame, text="Calculate Performance", command=self.calculations, font=("Calibri", 16))
            calc_button.pack(side="left", padx=5)

        def add_entry_row(self):
            row_frame = ctk.CTkFrame(self.scrollable_frame)
            row_frame.pack(padx=10, pady=5, fill="x")

            nametext = ctk.CTkEntry(row_frame, width=200)
            nametext.pack(side="left", padx=(0, 10))
            newtext = ctk.CTkEntry(row_frame, width=200)
            newtext.pack(side="left", padx=(0, 10))

            def delete_row():
                row_frame.destroy()
                if nametext in self.name_boxes:
                    self.name_boxes.remove(nametext)
                if newtext in self.text_boxes:
                    self.text_boxes.remove(newtext)

            del_button = ctk.CTkButton(row_frame, text="X", command=delete_row, fg_color="red", width=70)
            del_button.pack(side="left")

            self.name_boxes.append(nametext)
            self.text_boxes.append(newtext)
 

        def get_entries(self):
            self.values = []
            marks = [] 
            if not self.name_boxes or not self.text_boxes: 
                error_msg = ctk.CTkLabel(self.scrollable_frame, text="Please add at least one name and mark entry.", text_color="red", font=("Calibri", 16)) 
                error_msg.pack(pady=(10, 0))
                return    
            error_check = [entry.get() for entry in self.name_boxes + self.text_boxes] 
            for entry in error_check: 
                if not entry.strip(): 
                    error_msg = ctk.CTkLabel(self.scrollable_frame, text="All fields must be filled out.", text_color="red", font=("Calibri", 16)) 
                    error_msg.pack(pady=(10, 0))
                    return
            for entry in self.text_boxes:
                raw = entry.get()
                parts = [x for x in raw.replace(',', ' ').split() if x.strip()]
                nums = []
                for x in parts:
                    try:
                        nums.append(int(x))
                    except ValueError:
                        error_msg = ctk.CTkLabel(self.scrollable_frame, text="All marks must be numbers.", text_color="red", font=("Calibri", 16))
                        error_msg.pack(pady=(10, 0))
                        return
                if nums:
                    avg = sum(nums) / len(nums)
                    marks.append(avg)
                else:
                    marks.append(0)
            self.values = marks 
            self.run() 
            self.calculations()

        def run(self):
            plt.clf()
            counts, bins, patches = plt.hist(self.values, bins=10, color="skyblue", edgecolor="black", alpha=0.7)
            bin_centers = 0.5 * (bins[1:] + bins[:-1])
            filtered_centers = [center for center, count in zip(bin_centers, counts) if count > 0]
            filtered_counts = [count for count in counts if count > 0]
            plt.plot(filtered_centers, filtered_counts, color="red", marker="o", linestyle="-", linewidth=2, label="Frequency Polygon")
            plt.title(f"Histogram with Frequency Polygon ({self.subject_name})")
            plt.xlabel("Value")
            plt.ylabel("Frequency")
            plt.legend()
            plt.show()
            

        def extra_graph(self):
            names = [entry.get() for entry in self.name_boxes]
            marks = []
            for entry in self.text_boxes:
                raw = entry.get()
                parts = [x for x in raw.replace(',', ' ').split() if x.strip()]
                nums = [int(x) for x in parts]
                if nums:
                    avg = sum(nums) / len(nums)
                    marks.append(avg)
                else:
                    marks.append(0)
            plt.clf()
            plt.bar(names, marks, color="skyblue", edgecolor="black")
            plt.title(f"Average Marks per Student ({self.subject_name})")
            plt.xlabel("Student")
            plt.ylabel("Average Mark")
            plt.show()

        def calculations(self):
            # Clear previous results
            for widget in self.scrollable_frame_2.winfo_children():
                widget.destroy()

            names = [entry.get() for entry in self.name_boxes]
            marks = [] 
            
            for entry in self.text_boxes:
                raw = entry.get()
                parts = [x for x in raw.replace(',', ' ').split() if x.strip()]
                nums = [int(x) for x in parts]
                if nums:
                    avg = sum(nums) / len(nums)
                    marks.append(avg)
                else:
                    marks.append(0) 
            
                
            data = np.array(marks)
            mean = np.mean(data)
            std_dev = np.std(data)
            z_scores = [round(x, 3) for x in ((data - mean)/ std_dev)] if std_dev != 0 else [0 for _ in data]
            self.data_dict = {}
            for i in range(len(names)):
                self.data_dict[names[i]] = z_scores[i]
            for key, value in self.data_dict.items(): 
                for x in marks: 
                    item_frame = ctk.CTkFrame(self.scrollable_frame_2)
                item_frame.pack(fill="x", pady=(5,2))
                label = ctk.CTkLabel(item_frame, text=f"{key}: {value} (avg)", font=("Calibri", 16))
                label.pack(side="left", padx=(0,10))
                if value >= 2:
                    sum_label = ctk.CTkLabel(item_frame, text=f"🌟 Top Performer (≥ +2σ) with score {x}", font=("Segoe UI Emoji", 16), width=150)
                elif value >= 1.5:
                    sum_label = ctk.CTkLabel(item_frame, text=f"🟢 Excellent (+1.5σ to +2σ) with score {x}", font=("Segoe UI Emoji", 16), width=150)
                elif value >= 1:
                    sum_label = ctk.CTkLabel(item_frame, text=f"🟢 Very Good (+1σ to +1.5σ) with score {x}", font=("Segoe UI Emoji", 16), width=150)
                elif value >= 0.5:
                    sum_label = ctk.CTkLabel(item_frame, text=f"🟢 Above Average (+0.5σ to 1σ) with score {x}", font=("Segoe UI Emoji", 16), width=150)
                elif value >= 0:
                    sum_label = ctk.CTkLabel(item_frame, text=f"🟡 Average (0 to +0.5σ) with score {x}", font=("Segoe UI Emoji", 16), width=150)
                elif value >= -0.5:
                    sum_label = ctk.CTkLabel(item_frame, text=f"🟡 Slightly Below Average (-0.5σ to 0) with score {x}", font=("Segoe UI Emoji", 16), width=150)
                elif value >= -1:
                    sum_label = ctk.CTkLabel(item_frame, text=f"🟠 Below Average (-1σ to -0.5σ) with score {x}", font=("Segoe UI Emoji", 16), width=150)
                elif value >= -1.5:
                    sum_label = ctk.CTkLabel(item_frame, text=f"🔴 Needs Improvement (-1.5σ to -1σ) with score {x}", font=("Segoe UI Emoji", 16), width=150)
                elif value >= -2:
                    sum_label = ctk.CTkLabel(item_frame, text=f"🔴 Poor (-2σ to -1.5σ) with score {x}", font=("Segoe UI Emoji", 16), width=150)
                else:
                    sum_label = ctk.CTkLabel(item_frame, text=f"🔴 Very Poor (< -2σ) with score {x}", font=("Segoe UI Emoji", 16), width=150)
                sum_label.pack(side="left")   
            self.summary_window()
                
        
        def summary_window(self): 
            summary_window = ctk.CTkToplevel(app)
            summary_window.title(f"Summary for students in {self.subject_name}")
            summary_window.geometry("600x400")

            # Create a scrollable frame for the summary
            scrollable_frame = ctk.CTkScrollableFrame(summary_window)
            scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Add summary labels 
            names = [entry.get() for entry in self.name_boxes]
            marks = [] 
            
            for entry in self.text_boxes:
                raw = entry.get()
                parts = [x for x in raw.replace(',', ' ').split() if x.strip()]
                nums = [int(x) for x in parts]
                if nums:
                    avg = sum(nums) / len(nums)
                    marks.append(avg)
                else:
                    marks.append(0)  
            ranks = len(marks) - rankdata(marks,method='max') + 1  
            self.rank_dict = {names[i]: ranks[i] for i in range(len(names))} 
            for key, value in self.rank_dict.items():
                item_frame = ctk.CTkFrame(scrollable_frame)
                item_frame.pack(fill="x", pady=(5,2))
                label = ctk.CTkLabel(item_frame, text=f"{key}: Rank {value}", font=("Calibri", 16))
                label.pack(side="left", padx=(0,10))
                
                           
    def add_subject():
        subject = subject_entry.get().strip()
        if subject and subject not in subject_tabs:
            tabview.add(subject)
            subject_tabs[subject] = SubjectTab(tabview.tab(subject), subject)
            subject_entry.delete(0, "end")

    add_subject_button = ctk.CTkButton(subject_entry_frame, text="Add Subject", command=add_subject)
    add_subject_button.pack(side="left")

# Show login screen first
login()
app.mainloop()