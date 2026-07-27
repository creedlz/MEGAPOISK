import os
import tkinter as tk
from tkinter import filedialog, messagebox

import history

results = []

frame = None
folder_entry = None
search_entry = None
result_list = None
back_button = None

# выбор папы который раз
def choose_folder():
    folder = filedialog.askdirectory(title="Выберите папку")
    if folder:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)

# поиск файлов по нейму
def search_files():
    results.clear()
    result_list.delete(0, tk.END)

    folder = folder_entry.get().strip()
    query = search_entry.get().strip().lower()
    history.add(query)

    if not os.path.isdir(folder):
        messagebox.showerror(
            "Ошибка",
            "Папка не найдена")
        return
    
    if not query:
        messagebox.showwarning(
            "Внимание",
            "Введите название файла")
        return

    for root, _, files in os.walk(folder):
        for file in files:
            if query in file.lower():
                path = os.path.join(root, file)
                results.append(path)
                result_list.insert(tk.END, f"📄 {file}")

    if not results:
        result_list.insert(tk.END, "Ничего не найдено 😓")

# опен файл
def open_result(event=None):
    sel = result_list.curselection()
    if sel:
        path = results[sel[0]]
        try:
            os.startfile(path)
        except Exception as e:  # noqa: BLE001
            messagebox.showerror("Ошибка открытия", str(e))

# интерфейс, о боже исусе
def init(parent):

    global frame
    global folder_entry
    global search_entry
    global result_list
    global back_button

    frame = tk.Frame(parent, bg="#202124")

    title = tk.Label(
        frame,
        text="📁 Поиск по имени файла",
        font=("Segoe UI",16,"bold"),
        fg="white",
        bg="#202124")
    title.pack(pady=15)

    #папочкаааааа
    folder_frame = tk.Frame(frame, bg="#202124")

    folder_frame.pack(
        fill="x",
        padx=20,
        pady=5)

    folder_entry = tk.Entry(folder_frame)

    folder_entry.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0,10))

    tk.Button(
        folder_frame,
        text="📁 Выбрать",
        width=12,
        command=choose_folder).pack(side="right")

    # сёртч 333
    search_frame = tk.Frame(frame, bg="#202124")

    search_frame.pack(
        fill="x",
        padx=20,
        pady=10
    )

    search_entry = tk.Entry(search_frame)

    search_entry.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0,10)
    )

    tk.Button(
        search_frame,
        text="🔍 Найти",
        width=12,
        command=search_files).pack(side="right")

    #итог
    result_list = tk.Listbox(frame, font=("Consolas",10))

    result_list.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10)

    result_list.bind("<Double-Button-1>", open_result)

    #кнопка-опен
    tk.Button(
        frame,
        text="📂 Открыть файл",
        font=("Segoe UI",10,"bold"),
        height=2,
        command=open_result).pack(fill="x", padx=20, pady=(0,10))

    # бек(енд)
    back_button = tk.Button(frame, text="⬅ Назад")

    back_button.pack(
        fill="x",
        padx=20,
        pady=(0,15))

# Показ / скрытие
def show():
    frame.pack(fill="both", expand=True )

def hide():
    frame.pack_forget()

def set_back(command):
    back_button.config(command=command)