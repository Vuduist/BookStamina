import tkinter as tk
import threading

# Цвета зон (пальцев)
ZONE_COLORS = {
    'left_pinky': '#f4cccc',
    'left_ring': '#ffe599',
    'left_middle': '#b6d7a8',
    'left_index': '#a2c4c9',
    'thumbs': '#d9d2e9',
    'right_index': '#a2c4c9',
    'right_middle': '#b6d7a8',
    'right_ring': '#ffe599',
    'right_pinky': '#f4cccc',
    'other': '#e6e6e6',
}

# Распределение клавиш по зонам (пальцам)
KEY_ZONES = {
    'Ё': 'left_pinky', '1': 'left_pinky', '2': 'left_ring', '3': 'left_middle', '4': 'left_index', '5': 'left_index',
    'Tab': 'left_pinky', 'Й': 'left_pinky', 'Ц': 'left_ring', 'У': 'left_middle', 'К': 'left_index', 'Е': 'left_index',
    'Caps Lock': 'left_pinky', 'Ф': 'left_pinky', 'Ы': 'left_ring', 'В': 'left_middle', 'А': 'left_index', 'П': 'left_index',
    'Shift': 'left_pinky', 'Я': 'left_pinky', 'Ч': 'left_ring', 'С': 'left_middle', 'М': 'left_index', 'И': 'left_index',
    'Ctrl': 'thumbs', 'Alt': 'thumbs', 'Space': 'thumbs',
    '6': 'right_index', '7': 'right_index', '8': 'right_middle', '9': 'right_ring', '0': 'right_pinky', '-': 'right_pinky', '=': 'right_pinky',
    'Н': 'right_index', 'Г': 'right_index', 'Ш': 'right_middle', 'Щ': 'right_ring', 'З': 'right_pinky', 'Х': 'right_pinky', 'Ъ': 'right_pinky', '/': 'right_pinky',
    'Р': 'right_index', 'О': 'right_index', 'Л': 'right_middle', 'Д': 'right_ring', 'Ж': 'right_pinky', 'Э': 'right_pinky', 'Enter': 'right_pinky',
    'Т': 'right_index', 'Ь': 'right_index', 'Б': 'right_middle', 'Ю': 'right_ring', '.': 'right_pinky',
}

class KeyboardVisualizer:
    def __init__(self, frame):
        self.frame = frame
        self.keys = {}
        self._create_keyboard()
        self.last_highlighted = None

    def _create_keyboard(self):
        layout = [
            ["Ё", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace"],
            ["Tab", "Й", "Ц", "У", "К", "Е", "Н", "Г", "Ш", "Щ", "З", "Х", "Ъ", "/"],
            ["Caps Lock", "Ф", "Ы", "В", "А", "П", "Р", "О", "Л", "Д", "Ж", "Э", "Enter"],
            ["Shift", "Я", "Ч", "С", "М", "И", "Т", "Ь", "Б", "Ю", ".", "Shift"],
            ["Ctrl", "Alt", "Space", "Alt", "Ctrl"]
        ]
        for r, row in enumerate(layout):
            for c, key in enumerate(row):
                zone = KEY_ZONES.get(key, 'other')
                btn = tk.Label(self.frame, text=key, width=4, height=2, relief="ridge", bg=ZONE_COLORS[zone])
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.keys[key] = btn

    def highlight_key(self, key):
        # Сначала сбрасываем все цвета по зонам
        for k, btn in self.keys.items():
            zone = KEY_ZONES.get(k, 'other')
            btn.config(bg=ZONE_COLORS[zone])
        # Затем подсвечиваем нужную клавишу
        if key in self.keys:
            self.keys[key].config(bg="#ff0000")  # ярко-красный
            # Анимация: через 200 мс вернуть цвет зоны
            def reset():
                zone = KEY_ZONES.get(key, 'other')
                self.keys[key].config(bg=ZONE_COLORS[zone])
            threading.Timer(0.2, reset).start() 