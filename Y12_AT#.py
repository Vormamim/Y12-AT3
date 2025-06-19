import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt

# Set appearance and color theme
ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("green")  

global values

text_boxes = []  # Holds entry field references
name_boxes = []  # Holds name entry references
current_row = 0  # Allows ne rows to be added    


dict = {}


def add_entry_row(): # Adds a row for name and marks simulatenously on the left side of the page
    global current_row
    row_frame = ctk.CTkFrame(scrollable_frame)  # Each row has it's own frame which is placed in the master scrollable frame
    row_frame.grid(row=current_row, column=0, columnspan=2, padx=10, pady=5) #the frame is placed in whatever curront row

    nametext = ctk.CTkEntry(row_frame, width=200) # placed in the row frame and is the input for the name
    nametext.pack(side="left", padx=(0, 10)) 
    newtext = ctk.CTkEntry(row_frame, width=200) #placed in the row frame and is the input for the mark
    newtext.pack(side="left", padx=(0, 10))

    def delete_row():
        row_frame.destroy() # Deletes the frame of the row
        # Remove the entries from the lists
        if nametext in name_boxes:
            name_boxes.remove(nametext)
        if newtext in text_boxes:
            text_boxes.remove(newtext)

    del_button = ctk.CTkButton(row_frame, text="X", command=delete_row, fg_color="red", width=70) # Buttonto delete
    del_button.pack(side="left")

    name_boxes.append(nametext) # Adds the name to a list to save for future purpose
    text_boxes.append(newtext) # Adds the mark to a list to save for future puposes
    current_row += 1

def get_entries(): 
    global values
    raw_values = [entry.get() for entry in text_boxes]  # Retrieve values in the list for marks  
    values  = [int(x) for x in raw_values] # Makes them all integers to be used in the graph
    run()

def run() :   
    plt.clf() # Clears any current graph 
    global values
   
    counts, bins, patches = plt.hist(values, bins=10, color="skyblue", edgecolor="black", alpha=0.7)  # Plots histogram with an array for counts, bins and patches
    
   
    bin_centers = 0.5 * (bins[1:] + bins[:-1])  # Calculate bin centers for the polygon

    # Exclude bins with 0 frequency
    filtered_centers = [center for center, count in zip(bin_centers, counts) if count > 0]
    filtered_counts = [count for count in counts if count > 0]

    # Plot frequency polygon only for non-zero frequencies
    plt.plot(filtered_centers, filtered_counts, color="red", marker="o", linestyle="-", linewidth=2, label="Frequency Polygon")
    plt.title("Histogram with Frequency Polygon")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()     
    calculations()

def extra_graph() : 
    global values 
    global text_boxes  
    plt.clf()
    names = [entry.get() for entry in name_boxes]  # Extract names from name_boxes
    marks = [int(entry.get()) for entry in text_boxes]  # Extract marks from text_boxes
    plt.bar(names, marks, color="skyblue", edgecolor="black")  # Create bar chart
    plt.show()

def calculations() :   
    current_row_2 = 0  # Allows new rows to be added in the second scrollable frame
    global names  
    global marks 
    names = [entry.get() for entry in name_boxes]  # Extract names from name_boxes
    marks = [int(entry.get()) for entry in text_boxes]  # Extract marks from text_boxes
    data = np.array(marks) 
    mean = np.mean(data) 
    std_dev = np.std(data) 
    z_scores = [round(x, 3) for x in ((data - mean)/ std_dev)]
    row_frame_2 = ctk.CTkFrame(scrollable_frame_2)   
    row_frame_2.grid(row=current_row_2, column=0, columnspan=2, padx=10, pady=5)  # Create a new frame for the Z-scores
    for i in range(len(names)): 
        dict[names[i]] = z_scores[i] 
    for key, value in dict.items():
        item_frame = ctk.CTkFrame(row_frame_2)
        item_frame.pack(fill="x", pady=(5,2))
        label = ctk.CTkLabel(item_frame, text=f"{key}: {value}", font=("Calibri", 16))
        label.pack(side="left", padx=(0,10))
        if value > 0 and value < 1:
            sum_label = ctk.CTkLabel(item_frame, text="🟢✨ Good", font=("Segoe UI Emoji", 16), width=100) 
        elif value >= 1 and value < 2: 
            sum_label = ctk.CTkLabel(item_frame, text="🟢🌟 Excellent", font=("Segoe UI Emoji", 16), width=100)  
        elif value >= 2 and value < 3: 
            sum_label = ctk.CTkLabel(item_frame, text="🟢💎 Outstanding", font=("Segoe UI Emoji", 16), width=100) 
        elif value < 0 and value > -1: 
            sum_label = ctk.CTkLabel(item_frame, text="🟡✨ Below Average", font=("Segoe UI Emoji", 16), width=100 )
        elif value == 0:
            sum_label = ctk.CTkLabel(item_frame, text="🟡😐 Average", font=("Segoe UI Emoji", 16), width=100) 
        elif value <= -1 and value > -2: 
            sum_label = ctk.CTkLabel(item_frame, text="🔴⚠️ Needs Improvement", font=("Segoe UI Emoji", 16), width=100)
        else:
            sum_label = ctk.CTkLabel(item_frame, text="💩🔴 Poor", font=("Segoe UI Emoji", 16), width=100)
        sum_label.pack(side="left")

        current_row_2 += 1  # Increment the row counter for the next label 
    

    



### MAIN MASTER PROGRAM ###

app = ctk.CTk()
app.geometry("1000x900")
app.title("Student Marks Program")

title_label = ctk.CTkLabel(app, text="Student Marks Program 📚", font=("Calibri", 28, "bold"))
title_label.pack(pady=(20, 10))

# Button row (all buttons in one horizontal frame)
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

button_add_row = ctk.CTkButton(button_frame, text="Add name & mark", command=add_entry_row, font=("Calibri", 16))
button_add_row.pack(side="left", padx=5)

button_run = ctk.CTkButton(button_frame, text="Show frequency histogram", command=get_entries, font=("Calibri", 16))
button_run.pack(side="left", padx=5)

extra_button = ctk.CTkButton(button_frame, text="Show individual marks", command=extra_graph, font=("Calibri", 16))
extra_button.pack(side="left", padx=5)

calc_button = ctk.CTkButton(button_frame, text="Calculate Z-scores", command=calculations, font=("Calibri", 16))
calc_button.pack(side="left", padx=5)

# Scrollable frame for entry rows
scrollable_frame = ctk.CTkScrollableFrame(app)
scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Scrollable frame for results (z-scores, etc.)
scrollable_frame_2 = ctk.CTkScrollableFrame(app)
scrollable_frame_2.pack(pady=20, padx=20, fill="both", expand=True)

# If you had a dict_label or other result widgets, pack them here as well
# dict_label = ctk.CTkLabel(app, text="")
# dict_label.pack(pady=(10, 10))

app.mainloop()