# import datetime
import os
import time
import requests, json

import tkinter as tk
from PIL import ImageTk, Image

complete_url = "http://10.156.0.236//TestAlert.json"

root = tk.Tk()

alertDict = {
    "Generic": "generic.jpg"
}

# Define the image path
img_dir_path = os.path.join("..","..","AlertPhotos") # relative directory
img_name = alertDict["Generic"]
img_path = os.path.join(img_dir_path, img_name)
image = Image.open(img_path)

# Load the image file
photo = ImageTk.PhotoImage(image)
root.attributes("-fullscreen", True)
root.configure(bg = "white")

# Create a label widget to display the image
image_label = tk.Label(root, image=photo)
image_label.place(relx=0.5, rely=0.5, anchor="center")
#image_label.pack()
text_label = tk.Label(root, text="Alert",font=("Arial", 20),bg="white",highlightthickness=0, highlightbackground="white")

# Create a label widget to display the text

while True:

    response = requests.get(complete_url) 

    x = response.json()


    with open("sample.json", "w") as outfile:
        json.dump(x, outfile)

    print(x["alerts"][0]["Description"])

    
    text_label.config(text=x["alerts"][0]["Description"]+"\n\n\n\n\n")
    text_label.pack(side="bottom", anchor="center")
    

#text_label.pack()
    
    root.update()
    time.sleep(3)
    
    
