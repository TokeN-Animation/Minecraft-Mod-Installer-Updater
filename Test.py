import tkinter as tk
import tkinter.filedialog as filedialog
import subprocess
import requests
import os
import zipfile
import shutil
import datetime
import json
import tkinter.font as tkfont

minecraft_dir = os.path.join(os.getenv('APPDATA'), '.minecraft', 'mods')
history_file_path = os.path.join(os.path.dirname(__file__), "history.json")

class App:
    def __init__(self, master):
        self.master = master

        master.title("Minecraft Mod Installer and Updater")
        master.iconbitmap("icon.ico")
        self.font = tkfont.Font(family="Kanit-Light.tff", size=12)

        self.install_label = tk.Label(master, text="Install Location:")
        self.install_label.pack(side=tk.LEFT)
        self.install_textbox = tk.Entry(master)
        self.install_textbox.pack(side=tk.LEFT)
        self.install_textbox.insert(0, minecraft_dir)

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_directory)
        self.browse_button.pack()

        self.history_label = tk.Label(master, text="File History:")
        self.history_label.pack()
        self.history_listbox = tk.Listbox(master)
        self.history_listbox.pack()

        self.install_button = tk.Button(master, text="Install", command=self.install_file)
        self.install_button.pack()

        self.update_button = tk.Button(master, text="Update [Coming Soon]", command=self.update_file)
        self.update_button.pack()

        master.geometry("500x300")

    def browse_directory(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.install_textbox.delete(0, tk.END)
            self.install_textbox.insert(0, dir_path)
            
    def install_file(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        url = "https://codeload.github.com/Sea-Ch/Minecraft-Mode-Test/zip/refs/heads/main"
        filename = f"mod_{timestamp}.zip"

        dir_path = self.install_textbox.get()
        if not dir_path:
            dir_path = filedialog.askdirectory()
            if not dir_path:
                return

        file_path = os.path.join(dir_path, filename)

        response = requests.get(url)

        with open(file_path, "wb") as f:
            f.write(response.content)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            extracted_folder = os.path.join(dir_path, os.path.splitext(filename)[0])
            zip_ref.extractall(extracted_folder)

        extracted_files_path = os.path.join(extracted_folder, "Minecraft-Mode-Test-main")
        for item in os.listdir(extracted_files_path):
            item_path = os.path.join(extracted_files_path, item)
            if os.path.isfile(item_path):
                shutil.move(item_path, dir_path)
            elif os.path.isdir(item_path):
                shutil.move(item_path, os.path.join(dir_path, item))

        shutil.rmtree(extracted_folder)

        self.history_listbox.insert(0, file_path)

        history = {"timestamp": timestamp, "file_path": file_path}
        history_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history.json")
        if os.path.exists(history_file_path):
            with open(history_file_path, "r") as f:
                data = json.load(f)
        else:
            data = []
        data.append(history)
        with open(history_file_path, "w") as f:
            json.dump(data, f)

        tk.messagebox.showinfo("Install File", "File installed successfully!")
root = tk.Tk()
app = App(root)
root.mainloop()