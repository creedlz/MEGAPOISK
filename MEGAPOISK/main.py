# Ну что блять. я снова сел писать. 
# Пара коментов для тех кто будет это читать. Я - НЕ прогрмист, я школьник. 
# Я не претендую на то что это хороший код. ( он точно не хороший )
# Мне просто очень понравилась идея и я захотел воссоздать её в код. Не судите строго.
# И как я пишу во всех своих проектах: ДАЛЬШЕ БОГА НЕТ!

import tkinter as tk

import excel_search
import favorites
import filename_search
import history_view
import settings
import word_search

#главное окно
root = tk.Tk()
root.title(settings.APP_NAME)
root.geometry(settings.WINDOW_SIZE)
root.configure(bg=settings.BG_COLOR)

#леваки понель
menu = tk.Frame(root, width=230, bg=settings.PANEL_COLOR)
menu.pack(side="left", fill="y")

#рабочая область рот
content = tk.Frame(root, bg=settings.BG_COLOR)
content.pack(side="right", fill="both", expand=True)

#модули
excel_search.init(content)
word_search.init(content)
filename_search.init(content)
favorites.init(content)
history_view.init(content)

#сокрытие
def hide_all():

    excel_search.hide()
    word_search.hide()
    filename_search.hide()
    favorites.hide()
    history_view.hide()

#октрытие
def open_word():
    hide_all()
    word_search.show()

def open_excel():
    hide_all()
    excel_search.show()

def open_filename():
    hide_all()
    filename_search.show()

def open_favorites():
    hide_all()
    favorites.show()

def open_history():
    hide_all()
    history_view.show()

#бек
def back():
    hide_all()
    open_word()

excel_search.set_back(back)
word_search.set_back(back)
filename_search.set_back(back)
favorites.set_back(back)
history_view.set_back(back)

#меню
tk.Label(
    menu,
    text="MEGAPOISK",
    font=("Segoe UI",18,"bold"),
    fg="white",
    bg=settings.PANEL_COLOR).pack(pady=30)

tk.Button(
    menu,
    text="📄 Поиск Word",
    font=("Segoe UI",11),
    width=22,
    height=3,
    command=open_word).pack(pady=8)

tk.Button(
    menu,
    text="📊 Поиск Excel",
    font=("Segoe UI",11),
    width=22,
    height=3,
    command=open_excel).pack(pady=8)

tk.Button(
    menu,
    text="📁 Поиск по имени файла",
    font=("Segoe UI",11),
    width=22,
    height=2,
    command=open_filename).pack(pady=8)

tk.Button(
    menu,
    text="⭐ Избранные папки",
    font=("Segoe UI",11),
    width=22,
    height=2,
    command=open_favorites).pack(pady=8)

tk.Button(
    menu,
    text="🕘 История поиска",
    font=("Segoe UI",11),
    width=22,
    height=2,
    command=open_history).pack(pady=8)

#запускеее
open_word()
root.mainloop()