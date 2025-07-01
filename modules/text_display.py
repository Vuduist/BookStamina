import tkinter as tk
import tkinter.font as tkFont

class TextDisplay:
    def __init__(self, canvas, font=("Courier New", 22)):
        self.canvas = canvas
        self.font = font
        self.tkfont = tkFont.Font(family=self.font[0], size=self.font[1])

    def show_text(self, text, typed_len):
        self.canvas.delete("all")
        x0 = 100  # фиксированная точка (например, центр или отступ слева)
        y = 40
        # Введённая часть
        correct = text[:typed_len]
        # Оставшаяся часть
        rest = text[typed_len:]
        # Ширина введённой части
        width_correct = self.tkfont.measure(correct)
        # Рисуем введённое (серым)
        self.canvas.create_text(x0 - width_correct, y, anchor="w", text=correct, fill="#bbbbbb", font=self.font)
        # Рисуем оставшееся (чёрным, жирным)
        bold_font = self.tkfont.copy()
        bold_font.configure(weight="bold")
        self.canvas.create_text(x0, y, anchor="w", text=rest, fill="black", font=bold_font)

    def _text_width(self, text):
        # Используем tkinter font для точной ширины
        font = self.font
        return self.canvas.create_text(0, 0, text=text, font=font, anchor="nw", tags="measure") or 0 