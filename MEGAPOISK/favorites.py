import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox

FILE_NAME = "favorites.json"

frame = None
list_box = None
back_button = None

favorites = []

#загрузка
def load_favorites():
    global favorites
    try:
        with open(
            FILE_NAME,
            "r",
            encoding="utf-8"
        ) as f:
            favorites = json.load(f)
    except:  # noqa: E722
        favorites = []

# сейв
def save_favorites():
    with open(
        FILE_NAME,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            favorites,
            f,
            indent=4,
            ensure_ascii=False
        )



# выбор папы
def add_folder():
    folder = filedialog.askdirectory(title="Выберите папку" )
    if folder:
        if folder not in favorites:
            favorites.append(folder)
            save_favorites()
            update_list()
        else:
            messagebox.showinfo(
                "Информация",
                "Эта папка уже есть в избранном"
            )

# удалить папу 😓
def delete_folder():
    sel = list_box.curselection()
    if sel:
        folder = favorites[sel[0]]
        favorites.remove(folder)
        save_favorites()
        update_list()

# открыть папу 🐣
def open_folder(event=None):
    sel = list_box.curselection()
    if sel:
        folder = favorites[sel[0]]
        if os.path.exists(folder):
            os.startfile(folder)
        else:
            messagebox.showerror(
                "Ошибка",
                "Папка больше не существует")

# обновление списка
def update_list():
    list_box.delete(0, tk.END)
    for folder in favorites:
        list_box.insert(tk.END, "📁 " + folder)

# Инициализация (я даже загуглил. не слово, а пиздень)
def init(parent):
    global frame
    global list_box
    global back_button
    load_favorites()
    frame = tk.Frame(parent, bg="#202124")
    title = tk.Label(
        frame,
        text="⭐ Избранные папки",
        font=("Segoe UI",16,"bold"),
        fg="white",
        bg="#202124"
    )
    title.pack(pady=15)

    # список папочек
    list_box = tk.Listbox(frame, font=("Consolas",11))
    list_box.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )
    list_box.bind("<Double-Button-1>", open_folder)

    # кнопки
    button_frame = tk.Frame(frame, bg="#202124")
    button_frame.pack(pady=10)
    tk.Button(
        button_frame,
        text="➕ Добавить папку",
        width=18,
        command=add_folder).pack(side="left", padx=5)
    tk.Button(
        button_frame,
        text="❌ Удалить",
        width=18,
        command=delete_folder).pack(side="left", padx=5)
    back_button = tk.Button(frame, text="⬅ Назад")
    back_button.pack(
        fill="x",
        padx=20,
        pady=10
    )

# Показ / скрытие
def show():
    frame.pack(fill="both", expand=True)
    update_list()

def hide():
    frame.pack_forget()

def set_back(command):
    back_button.config(
        command=command)