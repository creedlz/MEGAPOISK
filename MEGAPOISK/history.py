import json
import os

FILE = "history.json"

#добавить
def add(query):
    history = load()
    if query not in history:
        history.append(query)
    save(history)



#загрузка
def load():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:  # noqa: BLE001
        return []



#сохранение
def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

#Очистка
def clear():
    save([])