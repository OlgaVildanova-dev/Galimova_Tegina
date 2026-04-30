import tkinter as tk
from tkinter import messagebox, Listbox, END
import requests
import json

# Загрузка избранных
def load_favorites():
    try:
        with open('favorites.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Сохранение избранных
def save_favorites(favorites):
    with open('favorites.json', 'w') as f:
        json.dump(favorites, f)

# Поиск пользователя
def search_user():
    username = entry.get()
    if not username:
        messagebox.showerror("Ошибка", "Поле не должно быть пустым!")
        return
    try:
        response = requests.get(f"https://api.github.com/users/{username}")
        user = response.json()
        listbox.insert(END, f"{user['name']} (@{user['login']})")
    except Exception as e:
        messagebox.showerror("Ошибка", "Пользователь не найден!")

# Добавление в избранное
def add_to_favorites():
    selected = listbox.get(listbox.curselection())
    favorites.append(selected)
    save_favorites(favorites)
    messagebox.showinfo("Успех", "Пользователь добавлен в избранное!")

# GUI
root = tk.Tk()
root.title("GitHub User Finder")

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

btn_search = tk.Button(root, text="Поиск", command=search_user)
btn_search.pack()

listbox = Listbox(root, width=50, height=15)
listbox.pack(pady=10)

btn_fav = tk.Button(root, text="В избранное", command=add_to_favorites)
btn_fav.pack()

favorites = load_favorites()

root.mainloop()
