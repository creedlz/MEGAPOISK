import os
import tkinter as tk
from tkinter import filedialog, messagebox

from docx import Document
from pypdf import PdfReader

import history

results = []

frame = None
folder_entry = None
search_entry = None
result_list = None
back_button = None

#выбор папы
def choose_folder():
    folder = filedialog.askdirectory(title="Выберите папку")
    if folder:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0,folder)

#TXT
def search_txt(path, query):
    found = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f, start=1):
                if query in line.lower():
                    found.append(f"Строка {i}: {line.strip()[:120]}")
    except Exception as e:  # noqa: BLE001
        print(e)
    return found

#DOCX
def search_docx(path, query):
    found = []
    try:
        import re
        doc = Document(path)

        for paragraph_num, paragraph in enumerate(doc.paragraphs, start=1):
            text = paragraph.text.strip()
            if not text:
                continue
            sentences = re.split(r'(?<=[.!?])\s+', text)

            for sentence in sentences:
                if query in sentence.lower():
                    found.append(f"Абзац {paragraph_num}: {sentence.strip()}")
                    break
    except Exception as e:  # noqa: BLE001
        print(e)
    return found

#PDF-файл ХАХАХААХХА
def search_pdf(path, query):
    found = []
    try:
        pdf = PdfReader(path) #я всё ещё угораю с PDF
        for page_num, page in enumerate(pdf.pages,start=1):
            text = page.extract_text() or ""
            text_low = text.lower()
            if query in text_low:
                pos = text_low.find(query)
                fragment = text[max(0, pos-50): pos+120]
                found.append(f"Страница {page_num}: {fragment}")
    except Exception as e:  # noqa: BLE001
        print(e)
    return found

#DOC
def search_doc(path, query):
    found = []
    try:
        import subprocess
        result = subprocess.run(
    ["antiword", path],
    capture_output=True,
    text=True,
    errors="ignore",
    check=False)
        
        text = result.stdout

        if query in text.lower():
            pos = text.lower().find(query)
            fragment = text[max(0, pos-50): pos+120]
            found.append(f"Найдено: {fragment}")

    except Exception as e:  # noqa: BLE001
        print("DOC ошибка:",e)
    return found

#общий поиск
def search_files():
    results.clear()
    result_list.delete(0, tk.END)

    folder = folder_entry.get().strip()
    query = search_entry.get().strip().lower()
    history.add(query)

    if not os.path.isdir(folder):
        messagebox.showerror(
            "Ошибка",
            "Папка не найдена"
        )
        return

    if not query:
        messagebox.showwarning(
            "Внимание",
            "Введите текст для поиска"
        )
        return

    for root, _, files in os.walk(folder):
        for fn in files:
            path = os.path.join(root,fn)
            ext = os.path.splitext(fn)[1].lower()
            matches = []

            if ext == ".docx":
                matches = search_docx(path, query)
            elif ext == ".doc":
                matches = search_doc(path, query)
            elif ext == ".pdf":
                matches = search_pdf(path, query)
            elif ext == ".txt":
                matches = search_txt(path, query)

            for match in matches:
                results.append(path)
                result_list.insert(tk.END, f"{fn} | {match}")

    if not results:
        result_list.insert(tk.END,"Ничего не найдено 😓")

#опен файло
def open_result(event=None):
    sel = result_list.curselection()
    if sel:
        os.startfile(results[sel[0]])

# Интерфейс (ну его нахуй)
def init(parent):

    global frame
    global folder_entry
    global search_entry
    global result_list
    global back_button

    frame = tk.Frame(parent, bg="#202124")

    # заглоталог
    title = tk.Label(
        frame,
        text="📄 Поиск Word / PDF / TXT",
        font=("Segoe UI", 16, "bold"),
        fg="white",
        bg="#202124")
    title.pack(pady=15)

    #папочка
    folder_frame = tk.Frame(frame, bg="#202124")
    folder_frame.pack(
        fill="x",
        padx=20,
        pady=5)
    folder_entry = tk.Entry(folder_frame,)
    folder_entry.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 10))
    tk.Button(
        folder_frame,
        text="📁 Выбрать",
        width=12,
        command=choose_folder).pack(side="right")

    #сёрч
    search_frame = tk.Frame(frame, bg="#202124")
    search_frame.pack(
        fill="x",
        padx=20,
        pady=10)
    search_entry = tk.Entry(search_frame,)
    search_entry.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 10))

    tk.Button(
        search_frame,
        text="🔍 Найти",
        width=12,
        command=search_files).pack(side="right")

    #итого
    result_frame = tk.Frame(frame, bg="#202124")
    result_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10)
    scroll = tk.Scrollbar(result_frame)
    scroll.pack(side="right", fill="y")
    result_list = tk.Listbox(result_frame, font=("Consolas", 10), yscrollcommand=scroll.set)
    result_list.pack(side="left", fill="both", expand=True)
    scroll.config(command=result_list.yview)

    result_list.bind("<Double-Button-1>", open_result)
    
#кнопка открытия файлоса *фалоса*
    tk.Button(
    frame,
    text="📂 Открыть файл",
    font=("Segoe UI", 10, "bold"),
    height=2,
    command=open_result).pack(fill="x", padx=20, pady=10)

#кнопка бека
    back_button = tk.Button(
    frame,
    text="⬅ Назад",
    width=12)

    back_button.pack(
    fill="x",
    padx=20,
    pady=(0, 15))

#Показ / скрытие
def show():
    frame.pack(fill="both", expand=True)
def hide():
    frame.pack_forget()
def set_back(command):
    back_button.config(command=command)