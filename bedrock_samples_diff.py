import os
import shutil
import hashlib
import subprocess
import sys
from tkinter import *
from tkinter import ttk, messagebox
from tkinterdnd2 import *

def calculate_file_hash(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def compare_folders(old_folder, new_folder, output_folder):
    result_text.delete(1.0, END)
    result_text.insert(END, "Starting Bedrock Samples comparison...\n")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    old_files = {}
    for root, _, files in os.walk(old_folder):
        for filename in files:
            old_path = os.path.join(root, filename)
            file_hash = calculate_file_hash(old_path)
            relative_path = os.path.relpath(old_path, old_folder)
            old_files[relative_path] = file_hash
    
    for root, _, files in os.walk(new_folder):
        for filename in files:
            new_path = os.path.join(root, filename)
            relative_path = os.path.relpath(new_path, new_folder)
            new_hash = calculate_file_hash(new_path)
            
            if relative_path not in old_files or old_files[relative_path] != new_hash:
                output_path = os.path.join(output_folder, relative_path)
                output_dir = os.path.dirname(output_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                shutil.copy2(new_path, output_path)
                result_text.insert(END, f"New/changed sample saved: {relative_path}\n")
    
    result_text.insert(END, "Comparison complete!\n")
    show_completion_popup(output_folder)

def clean_path(path):
    return path.strip().strip('{}')

def drop_old(event):
    cleaned_path = clean_path(event.data)
    old_path.set(cleaned_path)
    status_label.config(text="OLD Bedrock Samples assigned")

def drop_new(event):
    cleaned_path = clean_path(event.data)
    new_path.set(cleaned_path)
    status_label.config(text="NEW Bedrock Samples assigned")

def start_comparison():
    old = old_path.get()
    new = new_path.get()
    output = output_path.get() or "NEW BEDROCK SAMPLES"
    
    if not old or not new:
        result_text.delete(1.0, END)
        result_text.insert(END, "Please assign both OLD and NEW Bedrock Samples!\n")
        return
    
    if not os.path.exists(old):
        result_text.delete(1.0, END)
        result_text.insert(END, "OLD Bedrock Samples folder does not exist!\n")
        return
    if not os.path.exists(new):
        result_text.delete(1.0, END)
        result_text.insert(END, "NEW Bedrock Samples folder does not exist!\n")
        return
    
    try:
        compare_folders(old, new, output)
    except Exception as e:
        result_text.insert(END, f"Error: {str(e)}\n")

def show_completion_popup(output_folder):
    popup = Toplevel(root)
    popup.title("Bedrock Samples Diff")
    popup.geometry("300x150")
    popup.configure(bg="#F5F6F5")
    popup.resizable(False, False)
    popup.transient(root)
    popup.grab_set()
    
    popup.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() // 2) - (popup.winfo_width() // 2)
    y = root.winfo_y() + (root.winfo_height() // 2) - (popup.winfo_height() // 2)
    popup.geometry(f"+{x}+{y}")
    
    msg = ttk.Label(popup, text="Comparison completed successfully!", style="Pro.TLabel")
    msg.pack(pady=20)
    
    def open_folder():
        if os.name == 'nt':
            os.startfile(output_folder)
        elif os.name == 'posix':
            subprocess.run(['open' if sys.platform == 'darwin' else 'xdg-open', output_folder])
        popup.destroy()
    
    btn_frame = ttk.Frame(popup, style="Pro.TFrame")
    btn_frame.pack(pady=10)
    
    open_btn = ttk.Button(btn_frame, text="Open Folder", command=open_folder, style="Pro.TButton")
    open_btn.pack(side=LEFT, padx=5)
    
    ok_btn = ttk.Button(btn_frame, text="OK", command=popup.destroy, style="Pro.TButton")
    ok_btn.pack(side=LEFT, padx=5)

root = TkinterDnD.Tk()
root = TkinterDnD.Tk()
root.title("Bedrock Samples Diff By 0x")
root.geometry("1000x700")
root.configure(bg="#F5F6F5")

style = ttk.Style()
style.theme_use('clam')
style.configure("Pro.TFrame", background="#F5F6F5")
style.configure("Pro.TLabel", background="#F5F6F5", foreground="#333333", font=("Segoe UI", 11))
style.configure("Pro.TButton", background="#0078D4", foreground="#FFFFFF", 
                font=("Segoe UI", 10, "bold"), borderwidth=0, padding=5)
style.map("Pro.TButton", background=[('active', '#005EA6')])
style.configure("Pro.TEntry", fieldbackground="#FFFFFF", foreground="#333333", 
                font=("Segoe UI", 10), borderwidth=1, relief="solid")

main_frame = ttk.Frame(root, style="Pro.TFrame")
main_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)

left_frame = ttk.Frame(main_frame, style="Pro.TFrame", relief="flat")
left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 7.5))

old_label = ttk.Label(left_frame, text="OLD Bedrock Samples", style="Pro.TLabel")
old_label.pack(pady=(0, 5))

old_drop = ttk.Frame(left_frame, width=400, height=200, relief="solid", borderwidth=1, style="Pro.TFrame")
old_drop.pack(padx=0, pady=5)
old_drop.drop_target_register(DND_FILES)
old_drop.dnd_bind('<<Drop>>', drop_old)
old_drop_label = ttk.Label(old_drop, text="Drag & Drop OLD Samples Here", style="Pro.TLabel", foreground="#666666")
old_drop_label.place(relx=0.5, rely=0.5, anchor="center")

old_path = StringVar()
old_entry = ttk.Entry(left_frame, textvariable=old_path, width=50, style="Pro.TEntry")
old_entry.pack(padx=0, pady=5)

right_frame = ttk.Frame(main_frame, style="Pro.TFrame", relief="flat")
right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(7.5, 0))

new_label = ttk.Label(right_frame, text="NEW Bedrock Samples", style="Pro.TLabel")
new_label.pack(pady=(0, 5))

new_drop = ttk.Frame(right_frame, width=400, height=200, relief="solid", borderwidth=1, style="Pro.TFrame")
new_drop.pack(padx=0, pady=5)
new_drop.drop_target_register(DND_FILES)
new_drop.dnd_bind('<<Drop>>', drop_new)
new_drop_label = ttk.Label(new_drop, text="Drag & Drop NEW Samples Here", style="Pro.TLabel", foreground="#666666")
new_drop_label.place(relx=0.5, rely=0.5, anchor="center")

new_path = StringVar()
new_entry = ttk.Entry(right_frame, textvariable=new_path, width=50, style="Pro.TEntry")
new_entry.pack(padx=0, pady=5)

bottom_frame = ttk.Frame(root, style="Pro.TFrame")
bottom_frame.pack(fill=X, padx=15, pady=(0, 15))

output_label = ttk.Label(bottom_frame, text="Output Folder:", style="Pro.TLabel")
output_label.pack(side=LEFT, padx=(0, 5))

output_path = StringVar()
output_entry = ttk.Entry(bottom_frame, textvariable=output_path, width=30, style="Pro.TEntry")
output_entry.insert(0, "NEW BEDROCK SAMPLES")
output_entry.pack(side=LEFT, padx=(0, 10))

compare_button = ttk.Button(bottom_frame, text="Compare Samples", command=start_comparison, style="Pro.TButton")
compare_button.pack(side=LEFT, padx=0)

status_label = ttk.Label(bottom_frame, text="Ready", style="Pro.TLabel", foreground="#666666")
status_label.pack(side=LEFT, padx=10)

result_frame = ttk.Frame(root, style="Pro.TFrame")
result_frame.pack(fill=BOTH, expand=True, padx=15, pady=(0, 15))

result_text = Text(result_frame, height=10, width=80, bg="#FFFFFF", fg="#333333", 
                  font=("Segoe UI", 10), borderwidth=1, relief="solid")
result_text.pack(fill=BOTH, expand=True)
scrollbar = ttk.Scrollbar(result_frame, command=result_text.yview)
scrollbar.pack(side=RIGHT, fill=Y)
result_text.config(yscrollcommand=scrollbar.set)

root.mainloop()
