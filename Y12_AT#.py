import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
import json
import os

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

def sign_up():
    clear_window()
    username = ctk.CTkEntry(app, placeholder_text="Enter username", width=200, height=40, font=("Arial", 16))
    username.pack(pady=(20, 10))
    password = ctk.CTkEntry(app, placeholder_text="Enter password", width=200, height=40, font=("Arial", 16), show="*")
    password.pack(pady=(10, 20))

    def confirm_signup():
        saved_username = username.get()
        saved_password = password.get()
        with open("data.json", "r") as f:
            data = json.load(f)
        if saved_username in data:
            label = ctk.CTkLabel(app, text="Username already exists. Please try again.", font=("Arial", 16), text_color="red")
            label.pack(pady=(10, 20))
        else:
            data[saved_username] = saved_password
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
        with open("data.json", "r") as f:
            data = json.load(f)
        if login_username in data and data[login_username] == login_password:
            launch_marks_program()
        else:
            label = ctk.CTkLabel(app, text="Invalid username or password. Please try again.", font=("Arial", 16), text_color="red")
            label.pack(pady=(10, 20))

    confirm = ctk.CTkButton(app, text="Confirm", width=200, height=40, font=("Arial", 16), command=confirm_login)
    confirm.pack(pady=(10, 20))

    signup = ctk.CTkButton(app, text="Sign Up", width=200, height=40, font=("Arial", 16), command=sign_up)
    signup.pack(pady=(10, 20))

def launch_marks_program():
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
            self.current_row = 0
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

            calc_button = ctk.CTkButton(button_frame, text="Calculate Z-scores", command=self.calculations, font=("Calibri", 16))
            calc_button.pack(side="left", padx=5)

        def add_entry_row(self):
            row_frame = ctk.CTkFrame(self.scrollable_frame)
            row_frame.grid(row=self.current_row, column=0, columnspan=2, padx=10, pady=5)

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
            self.current_row += 1

        def get_entries(self):
            self.values = []
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
            self.values = marks
            self.run()

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
            self.calculations()

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
                item_frame = ctk.CTkFrame(self.scrollable_frame_2)
                item_frame.pack(fill="x", pady=(5,2))
                label = ctk.CTkLabel(item_frame, text=f"{key}: {value} (avg)", font=("Calibri", 16))
                label.pack(side="left", padx=(0,10))
                if value > 0 and value < 1:
                    sum_label = ctk.CTkLabel(item_frame, text="🟢✨ Good", font=("Segoe UI Emoji", 16), width=100)
                elif value >= 1 and value < 2:
                    sum_label = ctk.CTkLabel(item_frame, text="🟢🌟 Excellent", font=("Segoe UI Emoji", 16), width=100)
                elif value >= 2 and value < 3:
                    sum_label = ctk.CTkLabel(item_frame, text="🟢💎 Outstanding", font=("Segoe UI Emoji", 16), width=100)
                elif value < 0 and value > -1:
                    sum_label = ctk.CTkLabel(item_frame, text="🟡✨ Below Average", font=("Segoe UI Emoji", 16), width=100)
                elif value == 0:
                    sum_label = ctk.CTkLabel(item_frame, text="🟡😐 Average", font=("Segoe UI Emoji", 16), width=100)
                elif value <= -1 and value > -2:
                    sum_label = ctk.CTkLabel(item_frame, text="🔴⚠️ Needs Improvement", font=("Segoe UI Emoji", 16), width=100)
                else:
                    sum_label = ctk.CTkLabel(item_frame, text="💩🔴 Poor", font=("Segoe UI Emoji", 16), width=100)
                sum_label.pack(side="left")

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