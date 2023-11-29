import customtkinter
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess
from geometricshapecounter import GeometricShapeCounter
fileName = "shapes.png"

# CustomTkinter configuration
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")

# Create the main window
root = customtkinter.CTk()
root.title("Geometric Shape Counter")
root.geometry("900x500")  # Adjusted the window width

# Create a frame for widgets
frame = customtkinter.CTkFrame(master=root)
frame.pack(fill="both", expand=True)

# Load the background image (if available)
try:
    filename = PhotoImage(file="aybu_eee.PNG")
    background_label = customtkinter.CTkLabel(master=frame, text="", image=filename)
    background_label.grid(row=0, column=0, columnspan=2)
except:
    pass

# Create widgets for the login screen
label1 = customtkinter.CTkLabel(master=frame, text="Geometric Shape Counter", font=("Century", 36))
label1.grid(row=0, column=0, columnspan=2, pady=12, sticky="n")

label2 = customtkinter.CTkLabel(master=frame, text="EE409 DIGITAL IMAGE PROCESSING", font=("Verdana", 25))
label2.grid(row=1, column=0, columnspan=2, pady=12)

# Create a label to display the selected image on the left side
selected_image_label = customtkinter.CTkLabel(master=frame, text="")
selected_image_label.grid(row=4, column=0, columnspan=2, pady=12)

# Create a button to open the image file selection dialog
def open_image_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", ("*.jpg", "*.jpeg", "*.png"))])
    if file_path:
        # Open the image
        image = Image.open(file_path)

        # Check if the image size exceeds a certain threshold
        max_width = 800
        max_height = 600
        if image.width > max_width or image.height > max_height:
            # Resize the image proportionally to fit within the maximum dimensions
            image.thumbnail((max_width, max_height), Image.ANTIALIAS)

        # Display the selected image on the left side
        gsc = GeometricShapeCounter(fileName)
        output=gsc.drawContours(gsc.original, withText=False, withColor=True)
        im = Image.fromarray(output)
        photo= ImageTk.PhotoImage(image=im)
        # output=cv2.cvtColor(output,cv2.COLOR_GRAY2RGB)
        # photo = ImageTk.PhotoImage(output)
        # selected_image_label.configure(image=photo)
        print(photo)
        
        # selected_image_label.image = photo  # Keep a reference to the image to prevent garbage collection

        # # Enable the button to run scripts
        # run_scripts_button["state"] = "normal"

# Create a button to open the image file selection dialog
open_image_button = customtkinter.CTkButton(master=frame, text="Select Image File", command=open_image_file_dialog)
open_image_button.grid(row=5, column=0, columnspan=2, pady=12)

# # Function to run both Geometric Shape Counter.py and ErrorHandler.py
# def run_scripts():
#     if selected_image_label.image:
#         # Get the file path from the image object
#         file_path = selected_image_label.image.filename

#         # Run the other Python scripts
#         subprocess.run(["python", "Geometric Shape Counter.py", file_path])
#         subprocess.run(["python", "ErrorHandler.py", file_path])

# # Create a button to run scripts
# run_scripts_button = customtkinter.CTkButton(master=frame, text="Run Scripts", command=run_scripts, state="disabled")
# run_scripts_button.grid(row=6, column=0, columnspan=2, pady=12)

# Configure grid weights for resizing
frame.grid_rowconfigure(0, weight=5)
frame.grid_columnconfigure(0, weight=5)
frame.grid_columnconfigure(2, weight=5)


# Start the main event loop
root.mainloop()

