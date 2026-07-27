import tkinter as tk

import history

frame = None
listbox = None
back_button = None


# клир хистори (как лаконично)
def clear_history():
    history.clear()
    listbox.delete(0, tk.END)

#создание окна
def init(parent):

    global frame
    global listbox
    global back_button

    frame = tk.Frame(parent, bg="#202124")

    tk.Label(
        frame,
        text="🕘 История поиска",
        font=("Segoe UI",16,"bold"),
        fg="white",
        bg="#202124").pack(pady=20)

    #список истории на лето
    listbox = tk.Listbox(frame, font=("Segoe UI",12))
    listbox.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    # кнопка клира
    tk.Button(
        frame,
        text="🗑 Очистить историю",
        width=20,
        command=clear_history).pack(pady=10)

    #кнопка бек
    back_button = tk.Button(frame, text="⬅ Назад", width=20)
    back_button.pack(fill="x", padx=20, pady=10)

#показ модоокон
def show():
    listbox.delete(0,tk.END)
    for item in history.load():
        listbox.insert(tk.END, item)
    frame.pack(fill="both", expand=True)

# Скрытие этот позор, но нет это скрыть окно
def hide():
    frame.pack_forget()

# Кнопка бек
def set_back(command):
    back_button.config(command=command)