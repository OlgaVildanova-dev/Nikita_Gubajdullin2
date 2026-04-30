import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

# Файл для хранения истории паролей
HISTORY_FILE = "password_history.json"

def load_history():
    """Загружает историю паролей из файла JSON."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    """Сохраняет историю паролей в файл JSON."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def generate_password():
    """Генерирует пароль на основе выбранных параметров."""
    length = int(length_var.get())
    use_digits = digits_var.get()
    use_letters = letters_var.get()
    use_special = special_var.get()

    # Проверка длины пароля
    if length < 4 or length > 32:
        messagebox.showerror("Ошибка", "Длина пароля должна быть от 4 до 32 символов.")
        return

    # Формируем набор символов для генерации
    chars = ""
    if use_digits:
        chars += string.digits
    if use_letters:
        chars += string.ascii_letters
    if use_special:
        chars += string.punctuation

    if not chars:
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов.")
        return

    # Генерация пароля
    password = ''.join(random.choices(chars, k=length))
    
    # Отображение и сохранение
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    
    history.append(password)
    save_history(history)
    update_history_table()

def update_history_table():
    """Обновляет таблицу истории в GUI."""
    for i in history_table.get_children():
        history_table.delete(i)
    for p in history[-10:]:  # Показываем последние 10 паролей
        history_table.insert("", "end", values=(p,))

# Загрузка истории при старте приложения
history = load_history()

# --- Создание главного окна ---
root = tk.Tk()
root.title("Генератор случайных паролей")
root.geometry("500x450")
root.resizable(False, False)

# --- Элементы интерфейса ---
tk.Label(root, text="Длина пароля (4-32):").pack(pady=5)
length_var = tk.IntVar(value=12)
tk.Scale(root, from_=4, to=32, orient=tk.HORIZONTAL, variable=length_var).pack(pady=5)

tk.Label(root, text="Типы символов:").pack(pady=5)
digits_var = tk.BooleanVar(value=True)
letters_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Цифры", variable=digits_var).pack()
tk.Checkbutton(root, text="Буквы", variable=letters_var).pack()
tk.Checkbutton(root, text="Спецсимволы", variable=special_var).pack()

tk.Button(root, text="Сгенерировать пароль", command=generate_password).pack(pady=10)
password_entry = tk.Entry(root, width=40)
password_entry.pack(pady=5)

# Таблица истории
history_frame = tk.Frame(root)
history_frame.pack(pady=10, fill=tk.BOTH, expand=True)
history_table = ttk.Treeview(history_frame, columns=("password",), show="headings")
history_table.heading("password", text="История паролей")
history_table.column("password", width=450)
history_table.pack(fill=tk.BOTH, expand=True)
update_history_table()

root.mainloop()
