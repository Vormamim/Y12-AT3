import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
import json
import os  
import hashlib

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# creates user.json 
if not os.path.exists("user.json"):
    with open("user.json", "w") as f:
        json.dump({}, f)

app = ctk.CTk()
app.geometry("1100x900")
app.title("Student Marks Program")

def clear_window(): # clears window when switching between login, singup or the master program 
    """clears all widgets from the current window."""
    for widget in app.winfo_children():
        widget.destroy()

def hash_password(password):# hashes the password  
    '''takes in the password and hashes it'''
    return hashlib.sha256(password.encode()).hexdigest()

def sign_up(): #sign up function
    clear_window() 
    '''text boxes for username and passoword'''
    username = ctk.CTkEntry(app, placeholder_text="Enter username", width=200, height=40, font=("Arial", 16))
    username.pack(pady=(20, 10))
    password = ctk.CTkEntry(app, placeholder_text="Enter password", width=200, height=40, font=("Arial", 16), show="*")
    password.pack(pady=(10, 20))

    def confirm_signup(): # checks if the username and password are valid 
        '''gets the username and passowrd entered'''
        saved_username = username.get()
        saved_password = password.get()
        if not saved_username or not saved_password: 
            '''if both username and passoword are false/donnt exsist'''
            label = ctk.CTkLabel(app, text="Username and password cannot be empty.", font=("Arial", 16), text_color="red") # error message
            label.pack(pady=(10, 20))
            return
        with open("user.json", "r") as f:  # loads json file as a python dictionary
            data = json.load(f)
        if saved_username in data: 
            '''checks if the username already exists in the json file'''
            label = ctk.CTkLabel(app, text="Username already exists. Please try again.", font=("Arial", 16), text_color="red")
            label.pack(pady=(10, 20))
        else:
            '''passes criteria and saves to json'''
            data[saved_username] = hash_password(saved_password) # puts the username and the hashed version of password
            with open("user.json", "w") as f: #opens json and puts data in it
                json.dump(data, f, indent=4)
            label = ctk.CTkLabel(app, text="Sign up successful! Please log in.", font=("Arial", 16), text_color="green") # confirmation message
            label.pack(pady=(10, 20))

    confirm = ctk.CTkButton(app, text="Confirm", width=200, height=40, font=("Arial", 16), command=confirm_signup)
    confirm.pack(pady=(10, 20))

    back = ctk.CTkButton(app, text="Back to Login", width=200, height=40, font=("Arial", 16), command=login)
    back.pack(pady=(10, 20))

def login(): 
    '''first page that appears that allows users to login to the system'''
    clear_window()
    username = ctk.CTkEntry(app, placeholder_text="Enter username", width=200, height=40, font=("Arial", 16))
    username.pack(pady=(20, 10))
    password = ctk.CTkEntry(app, placeholder_text="Enter password", width=200, height=40, font=("Arial", 16), show="*")
    password.pack(pady=(10, 20))

    def confirm_login(): 
        '''Checks if the inputted username and password are valid'''
        login_username = username.get() #retrieves username and password from textboxes
        login_password = password.get()
        if not login_username or not login_password: 
            '''if the values from the input boxes comes back as false'''
            label = ctk.CTkLabel(app, text="Username and password cannot be empty.", font=("Arial", 16), text_color="red") # flagged as being empty
            label.pack(pady=(10, 20))
            return
        with open("user.json", "r") as f: 
            '''opens json file to use for validation'''
            data = json.load(f)
        if login_username in data and data[login_username] == hash_password(login_password): 
            '''checks if the username exsists in the database and if the inputted username and password match with the username and hashed password in the json file'''
            master_program() #runs main program
        else:
            label = ctk.CTkLabel(app, text="Invalid username or password. Please try again.", font=("Arial", 16), text_color="red") # error message
            label.pack(pady=(10, 20))

    confirm = ctk.CTkButton(app, text="Confirm", width=200, height=40, font=("Arial", 16), command=confirm_login)
    confirm.pack(pady=(10, 20))

    signup = ctk.CTkButton(app, text="Sign Up", width=200, height=40, font=("Arial", 16), command=sign_up)
    signup.pack(pady=(10, 20))

def master_program(): 
    '''Main function that houses everything'''
    clear_window() # clears singup and login

    title_label = ctk.CTkLabel(app, text="Student Dashboard Manager 📚", font=("Calibri", 28, "bold"))
    title_label.pack(pady=(20, 10))

    # Subject input
    subject_entry_frame = ctk.CTkFrame(app) # creates a frame at the top to input subjects
    subject_entry_frame.pack(pady=(10, 0))

    subject_entry = ctk.CTkEntry(subject_entry_frame, placeholder_text="Enter new subject")
    subject_entry.pack(side="left", padx=(0, 10))

    tabview = ctk.CTkTabview(app) # creates tabs at the top of the screen
    tabview.pack(padx=10, pady=10, fill="both", expand=True)

    subject_tabs = {} # adds the name of subjects 

    class SubjectTab:  
        '''Class for the blueprint of each subject'''
        def __init__(self, parent, subject_name): # parent is the tab which widgets are put into and subject_name is the name of subject typed in
            '''creates all the attributes for the class'''
            self.parent = parent 
            self.subject_name = subject_name
            self.text_boxes = [] # marks for each student
            self.name_boxes = [] # names for each student 
            self.values = [] # list to house the averages for each subjects
            self.data_dict = {} # dict for each person name to their z score

            
            self.scrollable_frame = ctk.CTkScrollableFrame(parent) # frame for adding rows for entering marks
            self.scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True) 



        
            self.scrollable_frame_2 = ctk.CTkScrollableFrame(parent) # frame for performance results aka z scores
            self.scrollable_frame_2.pack(pady=10, padx=10, fill="both", expand=True)

          
            button_frame = ctk.CTkFrame(parent) # frame for buttons at the bottom of the page
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
            '''function to add a new entry (name and mark) as a row'''
            row_frame = ctk.CTkFrame(self.scrollable_frame) # new frame for each row placed in the scrollable frame 
            row_frame.pack(padx=10, pady=5, fill="x")

            nametext = ctk.CTkEntry(row_frame, width=200, placeholder_text="Name") # text box to add name
            nametext.pack(side="left", padx=(0, 10))
            marktext = ctk.CTkEntry(row_frame, width=200, placeholder_text= "Mark") # textbox to add mark
            marktext.pack(side="left", padx=(0, 10))

            def delete_row(): 
                '''when x is pressed, this function runs'''
                row_frame.destroy() # deletes the frame for that specific row
                if nametext in self.name_boxes:
                    self.name_boxes.remove(nametext) # removes appeneded names from the name_box list
                if marktext in self.text_boxes:
                    self.text_boxes.remove(marktext) # removes appened marks from the text_box list

            del_button = ctk.CTkButton(row_frame, text="X", command=delete_row, fg_color="red", width=70)
            del_button.pack(side="left")

            self.name_boxes.append(nametext) # if delete not pressed, adds name and marks to list
            self.text_boxes.append(marktext)
 

        def get_entries(self): 
            '''retrieves values from the entry boxes and prepares them for graphing'''
            self.values = [] # list for the averages (same as one in _innit_)
            marks = [] # initial list for averages which is then placed into self.values
            if not self.name_boxes or not self.text_boxes:  
                '''if no name boxes or text boxes made (appears as false) and is flagged'''
                error_msg = ctk.CTkLabel(self.scrollable_frame, text="Please add at least one name and mark entry.", text_color="red", font=("Calibri", 16)) # error message
                error_msg.pack(pady=(10, 0))
                return    
            error_check = [entry.get() for entry in self.name_boxes + self.text_boxes] # clreats a list combinign both names and marks
            for entry in error_check:  
                '''for each name and mark it checks if the box is filled'''
                if not entry.strip(): 
                    '''if by removing spaces at the end, there are no contents in the text box, it is flagged'''
                    error_msg = ctk.CTkLabel(self.scrollable_frame, text="All fields must be filled out.", text_color="red", font=("Calibri", 16)) 
                    error_msg.pack(pady=(10, 0))
                    return
            for entry in self.text_boxes: 
                '''function to formulate an average in the values inputted in each mark text box'''
                raw = entry.get() # extracts the values as a string
                parts = [x for x in raw.replace(',', ' ').split() if x.strip()] # replaces commas with spaces and breaks them down at each space 
                nums = [] # list for integer value of each part (integer version of parts)
                for x in parts: 
                    '''error handling for each value in the entry box to check if they are numbers and are seperated correctly'''
                    try: # trys to make the string into a number
                        nums.append(int(x))
                    except ValueError: # if it can't, it's flagged as a letter not a number or are seperated incorrectly
                        error_msg = ctk.CTkLabel(self.scrollable_frame, text="All marks must be numbers with commmas or spaces seperating them.", text_color="red", font=("Calibri", 16))
                        error_msg.pack(pady=(10, 0))
                        return
                if nums:
                    avg = sum(nums) / len(nums) # formulates average of marks in each entry box
                    marks.append(avg) # adds them to the marks list
                else:
                    marks.append(0) # adds 0 to mark list if no valid numbers
            self.values = marks # adds these processed and averages marks to the origninal self.values list
            self.run() # executes graphing
            self.calculations() # executes calculations

        def run(self): 
            '''function for graphing '''
            plt.clf()
            counts, bins, patches = plt.hist(self.values, bins=10, color="skyblue", edgecolor="black", alpha=0.7) # counts is a list of frequency of values per bin (heigh of bar) and patches is the actual bar. Bins is the edges of the bins
            bin_centers = 0.5 * (bins[1:] + bins[:-1]) # finds center of each bin/bar by finding average from the edges of each bar
            filtered_centers = [center for center, count in zip(bin_centers, counts) if count > 0] # has the centers of bins that arent empty
            filtered_counts = [count for count in counts if count > 0] # contains the counts for non empty bins
            plt.plot(filtered_centers, filtered_counts, color="red", marker="o", linestyle="-", linewidth=2, label="Frequency Polygon") # plots polygon
            plt.title(f"Histogram with Frequency Polygon ({self.subject_name})")
            plt.xlabel("Value")
            plt.ylabel("Frequency")
            plt.legend()
            plt.show()
            

        def extra_graph(self):
            names = [entry.get() for entry in self.name_boxes] # creats a list for names
            marks = [] # list for marks for the bar graph (seperate from frequency histogram) 
            ## SAME STRIPPING AND AVERAGING FORMULA AS BEFFORE ##
            for entry in self.text_boxes:
                raw = entry.get()
                parts = [x for x in raw.replace(',', ' ').split() if x.strip()]
                nums = [int(x) for x in parts]
                if nums:
                    avg = sum(nums) / len(nums)
                    marks.append(avg)
                else:
                    marks.append(0)
            plt.clf() # clears any previous graphs in the matplot lib graph
            plt.bar(names, marks, color="skyblue", edgecolor="black")
            plt.title(f"Average Marks per Student ({self.subject_name})")
            plt.xlabel("Student")
            plt.ylabel("Average Mark")
            plt.show()

        def calculations(self):
        ## Calculates the z scores and therefore the performance for each student. Activated when the calculate performance button is pressed or once the frequency histogram is made ##
            for widget in self.scrollable_frame_2.winfo_children():
                widget.destroy() ## removes any previous performance calculations
            ## SAME STRIPPING AND AVERAGING FORMULA AS BEFFORE ##
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
            
               
            data = np.array(marks) # converts the list of marks to an array to be used to find mean and stnd dev
            mean = np.mean(data) # calculates average of marks
            std_dev = np.std(data) # calculates standard deviation of marks
            z_scores = [round(x, 3) for x in ((data - mean)/ std_dev)] if std_dev != 0 else [0 for _ in data] # calculates z scores for each function using the mathematical formula and rounds to 3 decimals. If the stnd deviation of the scores is 0, it's excluded
            self.data_dict = {} # dict for name and z scores as established earlier
            for i in range(len(names)): 
                # for the ammount of names inputted
                self.data_dict[names[i]] = z_scores[i] # add that name and it's z score to the dictionary 
            for key, value in self.data_dict.items(): # for each name and mark in the dictionary
                for x in marks: ## creates a new frame for each students performance
                    item_frame = ctk.CTkFrame(self.scrollable_frame_2)
                item_frame.pack(fill="x", pady=(5,2))
                label = ctk.CTkLabel(item_frame, text=f"{key}: {value} (avg)", font=("Calibri", 16))
                label.pack(side="left", padx=(0,10)) 
                ## Classifies a students performance based on z scores. Z scores that are more negative are mor below the mean and z scores that are more positive values
                if value >= 2: 
                    sum_label = ctk.CTkLabel(item_frame, text=f"🌟 Top Performer (≥ +2σ)", font=("Segoe UI Emoji", 16), width=150)
                elif value >= 1.5:
                    sum_label = ctk.CTkLabel(item_frame, text=f"🟢 Excellent (+1.5σ to +2σ)", font=("Segoe UI Emoji", 16), width=150)
                elif value >= 1:
                    sum_label = ctk.CTkLabel(item_frame, text=f"🟢 Very Good (+1σ to +1.5σ)", font=("Segoe UI Emoji", 16), width=150)
                elif value >= 0.5:
                    sum_label = ctk.CTkLabel(item_frame, text=f"🟢 Above Average (+0.5σ to 1σ)", font=("Segoe UI Emoji", 16), width=150)
                    sum_label = ctk.CTkLabel(item_frame, text=f"🟡 Average (0 to +0.5σ)", font=("Segoe UI Emoji", 16), width=150)
                elif value >= -0.5:
                    sum_label = ctk.CTkLabel(item_frame, text=f"🟡 Slightly Below Average (-0.5σ)", font=("Segoe UI Emoji", 16), width=150)
                elif value >= -1:
                    sum_label = ctk.CTkLabel(item_frame, text=f"🟠 Below Average (-1σ to -0.5σ)", font=("Segoe UI Emoji", 16), width=150)
                elif value >= -1.5:
                    sum_label = ctk.CTkLabel(item_frame, text=f"🔴 Needs Improvement (-1.5σ to -1σ) ", font=("Segoe UI Emoji", 16), width=150)
                elif value >= -2:
                    sum_label = ctk.CTkLabel(item_frame, text=f"🔴 Poor (-2σ to -1.5σ) ", font=("Segoe UI Emoji", 16), width=150)
                else:
                    sum_label = ctk.CTkLabel(item_frame, text=f"🔴 Very Poor (< -2σ)", font=("Segoe UI Emoji", 16), width=150)
                sum_label.pack(side="left")   
           
                           
    def add_subject(): 
        ## Function to add new subjects to a list ##
        subject = subject_entry.get().strip() # Gets the str of each subject
        if subject and subject not in subject_tabs: # Adds to list if doesnt already exsisted
            tabview.add(subject) # Adds to the top of the tabs
            subject_tabs[subject] = SubjectTab(tabview.tab(subject), subject) # creates a new instance of the class with the subject
            subject_entry.delete(0, "end")  # empties the entry box after adding the subject

    add_subject_button = ctk.CTkButton(subject_entry_frame, text="Add Subject", command=add_subject)
    add_subject_button.pack(side="left")

# Show login screen first
login()
app.mainloop()