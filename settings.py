import tkinter as tk
from tkinter import Label, Entry, Button, messagebox
import json


def save_changes():
    data = {
        "webhook_url": url_entry.get(),
        "webhook_name": name_entry.get(),
        "webhook_avatar": avatar_entry.get(),
        "detection_interval": interval_entry.get()
    }

    with open('assets/settings.json', 'w') as file:
        json.dump(data, file, indent=4)

    messagebox.showinfo("Confirmation", "Changes saved successfully!")


with open('assets/settings.json', 'r') as file:
    config_data = json.load(file)

root = tk.Tk()
root.title("Configuration Editor")

url_label = Label(root, text="Webhook URL:")
url_label.grid(row=0, column=0, padx=10, pady=5)
url_entry = Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=5)
url_entry.insert(0, config_data["webhook_url"])

name_label = Label(root, text="Webhook Name:")
name_label.grid(row=1, column=0, padx=10, pady=5)
name_entry = Entry(root, width=50)
name_entry.grid(row=1, column=1, padx=10, pady=5)
name_entry.insert(0, config_data["webhook_name"])

avatar_label = Label(root, text="Webhook Avatar:")
avatar_label.grid(row=2, column=0, padx=10, pady=5)
avatar_entry = Entry(root, width=50)
avatar_entry.grid(row=2, column=1, padx=10, pady=5)
avatar_entry.insert(0, config_data["webhook_avatar"])

interval_label = Label(root, text="Detection Interval:")
interval_label.grid(row=3, column=0, padx=10, pady=5)
interval_entry = Entry(root, width=50)
interval_entry.grid(row=3, column=1, padx=10, pady=5)
interval_entry.insert(0, config_data["detection_interval"])

save_button = Button(root, text="Save Changes", command=save_changes)
save_button.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
