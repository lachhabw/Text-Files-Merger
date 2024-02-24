import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tqdm import tqdm
import threading

def merge_text_files(folder_path, show_filename, save_path, success_label):
    try:
        # Check if the folder path exists
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            raise FileNotFoundError(f"Folder path: '{folder_path}' does not exist.")
        
        # Check if the save path can be created
        try:
            with open(save_path, 'w') as f:
                pass
        except:
            raise FileNotFoundError(f"Cannot create file: '{save_path}'")
        
        with open(save_path, 'wb') as merged_file:
            file_list = sorted(os.listdir(folder_path))
            for filename in tqdm(file_list, desc="Merging", unit="file"):
                file_path = os.path.join(folder_path, filename)
                try:
                    with open(file_path, 'rb') as current_file:
                        text = current_file.read()
                        if show_filename:
                            text = (f" ** {filename} **\n").encode() + text + "\n\n".encode()
                        merged_file.write(text)
                except:
                    messagebox.showwarning("Warning", f"Cannot read file '{filename}'")
    except Exception as e:
        messagebox.showerror("Error", e)
    else:
        success_label.config(text="Merging Finished!", fg="green")

def select_folder(entry_widget):
    folder_path = filedialog.askdirectory()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, folder_path)

def select_save_file(entry_widget):
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, save_path)


def start_merge_thread(folder_entry, save_entry, include_filename_var, merge_button, success_label):
    merge_thread = threading.Thread(target=start_merge, args=(folder_entry, save_entry, include_filename_var, merge_button, success_label))
    merge_thread.start()

def start_merge(folder_entry, save_entry, include_filename_var, merge_button, success_label):
    folder_path = folder_entry.get()
    save_path = save_entry.get()
    show_filename = include_filename_var.get()

    if not folder_path or not save_path:
        messagebox.showerror("Error", "Please select both folder and save file.")
        return

    merge_button.config(state=tk.DISABLED)  # Disable the button during the process
    merge_text_files(folder_path, show_filename, save_path, success_label)
    merge_button.config(state=tk.NORMAL)  # Enable the button after the process


def main():
    # Create the main application window
    app = tk.Tk()
    app.title("Text Files Merger")
    app.geometry("450x200")
    app.resizable(False, False)

    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)
    app.grid_columnconfigure(2, weight=1)
    app.grid_rowconfigure(3, weight=1)

    # Create and place widgets in the window
    tk.Label(app, text="Select Folder:").grid(row=0, column=0, sticky="e")
    folder_entry = tk.Entry(app, width=40)
    folder_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Button(app, text="Browse", command=lambda: select_folder(folder_entry)).grid(row=0, column=2, padx=5, pady=5)

    tk.Label(app, text="Select Save File:").grid(row=1, column=0, sticky="e")
    save_entry = tk.Entry(app, width=40)
    save_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(app, text="Browse", command=lambda: select_save_file(save_entry)).grid(row=1, column=2, padx=5, pady=5)

    include_filename_var = tk.BooleanVar(value=True)
    tk.Checkbutton(app, text="Include Filename", variable=include_filename_var).grid(row=2, column=1, padx=5, pady=5)

    success_label = tk.Label(app, text="")
    success_label.grid(row=4, column=0, columnspan=3, pady=10)

    merge_button = tk.Button(app, text="Start Merge", command=lambda: start_merge_thread(folder_entry, save_entry, include_filename_var, merge_button, success_label))
    merge_button.grid(row=3, column=0, columnspan=3, pady=10)

    # Run the application
    app.mainloop()

if __name__ == "__main__":
    main()