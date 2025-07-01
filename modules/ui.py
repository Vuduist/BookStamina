import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from modules.book_loader import BookLoader
from modules.progress_manager import ProgressManager
from modules.exercise_manager import ExerciseManager
from modules.text_display import TextDisplay
from modules.keyboard_visualizer import KeyboardVisualizer
from modules.input_checker import InputChecker
from modules.session_manager import SessionManager
from modules.stats import Stats
from modules.storage import Storage
import time
import threading
import os

book_loader = BookLoader()
progress_manager = ProgressManager()
session_manager = SessionManager()
storage = Storage()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BookStamina")
        self.geometry("1200x600")
        self.exercise_manager = None
        self.text_display = None
        self.keyboard_visualizer = None
        self.input_checker = InputChecker()
        self.current_sentence = ""
        self.typed = ""
        self.stats = Stats()
        self.training_mode = None
        self.training_start_time = None
        self.training_timer = None
        self.training_running = False
        self.current_book_path = None
        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()
        frame = tk.Frame(self)
        frame.pack(pady=10)
        btn_open = ttk.Button(frame, text="Открыть книгу (fb2)", command=self.open_book_dialog)
        btn_open.grid(row=0, column=0, padx=5)
        btn_timer = ttk.Button(frame, text="Режим таймера", command=self.select_timer_mode)
        btn_timer.grid(row=0, column=1, padx=5)
        btn_read = ttk.Button(frame, text="Режим чтения", command=self.select_read_mode)
        btn_read.grid(row=0, column=2, padx=5)
        self.show_catalog_panel()
        self.show_history_table()

    def show_catalog_panel(self):
        panel = tk.Frame(self)
        panel.pack(pady=10, fill="x")
        tk.Label(panel, text="Избранные книги:", font=("Arial", 12, "bold")).pack(anchor="w")
        favs = storage.get_recent_books(only_favorites=True)
        self._show_books(panel, favs, favorite_section=True)
        tk.Label(panel, text="Недавно открытые книги:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10,0))
        recents = storage.get_recent_books(only_favorites=False)
        self._show_books(panel, recents, favorite_section=False)

    def _show_books(self, parent, books, favorite_section):
        for book in books:
            path, title, last_opened, favorite = book
            row = tk.Frame(parent)
            row.pack(fill="x", pady=1)
            btn_open = ttk.Button(row, text=title, width=40, command=lambda p=path: self.open_book_from_catalog(p))
            btn_open.pack(side="left")
            tk.Label(row, text=os.path.basename(path), fg="gray").pack(side="left", padx=5)
            tk.Label(row, text=last_opened, fg="gray").pack(side="left", padx=5)
            fav_btn = ttk.Button(row, text="★" if favorite else "☆", width=2,
                                 command=lambda p=path, f=not favorite: self.toggle_favorite(p, f))
            fav_btn.pack(side="left", padx=5)

    def toggle_favorite(self, path, fav):
        storage.set_favorite(path, fav)
        self.create_main_menu()

    def open_book_dialog(self):
        filepath = filedialog.askopenfilename(filetypes=[("FB2 files", "*.fb2")])
        if filepath:
            self.open_book(filepath)

    def open_book_from_catalog(self, path):
        if os.path.exists(path):
            self.open_book(path)
        else:
            messagebox.showerror("Ошибка", f"Файл не найден: {path}")

    def open_book(self, filepath):
        text = book_loader.load_fb2(filepath)
        if text:
            self.current_book_path = filepath
            storage.add_recent_book(filepath, book_loader.title)
            self.exercise_manager = ExerciseManager(text)
            session_manager.set_book(book_loader.title)
            pos = progress_manager.load_progress(book_loader.title)
            session_manager.set_position(pos)
            self.start_training()

    def select_timer_mode(self):
        self.training_mode = "timer"
        self.ask_timer_duration()

    def select_read_mode(self):
        self.training_mode = "read"
        self.open_book_dialog()

    def ask_timer_duration(self):
        win = tk.Toplevel(self)
        win.title("Выберите длительность (мин)")
        tk.Label(win, text="Минут:").pack(side="left", padx=5)
        duration_var = tk.IntVar(value=5)
        entry = tk.Entry(win, textvariable=duration_var, width=5)
        entry.pack(side="left", padx=5)
        def start():
            self.timer_minutes = duration_var.get()
            win.destroy()
            self.open_book_dialog()
        btn = ttk.Button(win, text="Начать", command=start)
        btn.pack(side="left", padx=5)

    def show_history_table(self):
        history = storage.get_history()
        frame = tk.Frame(self)
        frame.pack(pady=10)
        cols = ("#", "Дата/время", "Скорость", "Точность", "Символы", "Длительность (сек)")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=8)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        for row in history:
            row = list(row)
            row[2] = int(round(row[2]))
            row[3] = int(round(row[3]))
            row[5] = int(round(row[5]))
            tree.insert("", "end", values=row)
        tree.pack()

    def start_training(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.typed = ""
        self.current_idx = session_manager.current_position
        self.current_sentence = self.exercise_manager.get_sentence(self.current_idx)
        self.stats.reset()
        self.stats.set_start(time.time())
        self.training_start_time = time.time()
        self.training_running = True
        frame_top = tk.Frame(self)
        frame_top.pack(fill="x")
        btn_menu = ttk.Button(frame_top, text="Завершить тренировку", command=self.finish_training)
        btn_menu.pack(side="left")
        self.canvas = tk.Canvas(self, width=850, height=80, bg="white")
        self.canvas.pack(pady=20)
        self.text_display = TextDisplay(self.canvas)
        self.text_display.show_text(self.current_sentence, 0)
        frame_kb = tk.Frame(self)
        frame_kb.pack()
        self.keyboard_visualizer = KeyboardVisualizer(frame_kb)
        self.update_keyboard_highlight()
        self.bind("<Key>", self.on_key)
        self.bind("<Escape>", lambda e: self.finish_training())
        if self.training_mode == "timer":
            self.training_timer = threading.Timer(self.timer_minutes * 60, self.finish_training)
            self.training_timer.start()

    def update_keyboard_highlight(self):
        pos = len(self.typed)
        if pos < len(self.current_sentence):
            expected = self.current_sentence[pos]
            self.keyboard_visualizer.highlight_key(expected.upper())
        else:
            self.keyboard_visualizer.highlight_key(None)

    def on_key(self, event):
        if not self.current_sentence or not self.training_running:
            return
        if event.keysym == "BackSpace":
            if self.typed:
                self.typed = self.typed[:-1]
                self.update_keyboard_highlight()
        elif event.char:
            pos = len(self.typed)
            if pos < len(self.current_sentence):
                expected = self.current_sentence[pos]
                if event.char == expected:
                    self.typed += event.char
                    self.stats.add_typed(1)
                    self.text_display.show_text(self.current_sentence, len(self.typed))
                    self.update_keyboard_highlight()
                    if self.typed == self.current_sentence:
                        progress_manager.save_progress(book_loader.title, self.current_idx + 1)
                        self.next_sentence()
                    return
                else:
                    self.stats.add_error(1)
        self.text_display.show_text(self.current_sentence, len(self.typed))

    def next_sentence(self):
        self.typed = ""
        self.current_idx += 1
        session_manager.set_position(self.current_idx)
        self.current_sentence = self.exercise_manager.get_sentence(self.current_idx)
        if not self.current_sentence:
            self.finish_training()
            return
        self.text_display.show_text(self.current_sentence, 0)
        self.update_keyboard_highlight()

    def finish_training(self):
        if not self.training_running:
            return
        self.training_running = False
        if self.training_mode == "timer" and self.training_timer:
            self.training_timer.cancel()
        self.stats.set_end(time.time())
        duration = self.stats.end_time - self.training_start_time
        speed = int(round(self.stats.get_speed()))
        accuracy = int(round(self.stats.get_accuracy()))
        chars = self.stats.chars_typed
        duration_rounded = int(round(duration))
        storage.add_history(speed, accuracy, chars, duration_rounded)
        messagebox.showinfo("Статистика", f"Скорость: {speed} зн/мин\nТочность: {accuracy}%\nСимволы: {chars}\nДлительность: {duration_rounded} сек")
        self.create_main_menu()


def run_app():
    app = App()
    app.mainloop() 