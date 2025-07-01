import xml.etree.ElementTree as ET
from tkinter import filedialog
import re

class BookLoader:
    def __init__(self):
        self.text = ""
        self.title = ""

    def preprocess_text(self, text):
        # Удаляем табуляции, длинные тире, кавычки-ёлочки, невидимые символы
        text = text.replace('\t', ' ')
        text = text.replace('\u2014', '-')  # длинное тире —
        text = text.replace('\u2013', '-')  # короткое тире –
        text = text.replace('«', '"').replace('»', '"')
        text = re.sub(r'[\u200b\u00a0\ufeff]', '', text)  # невидимые символы
        # Оставляем только символы, которые есть на стандартной русской клавиатуре
        allowed = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?;:-_=+()[]{}'\"/\\|@#$%^&*<>~`№ "
        text = ''.join(ch for ch in text if ch in allowed)
        # Удаляем повторяющиеся пробелы
        text = re.sub(r' +', ' ', text)
        return text

    def load_fb2(self, filepath=None):
        if not filepath:
            filepath = filedialog.askopenfilename(filetypes=[("FB2 files", "*.fb2")])
        if not filepath:
            return None
        tree = ET.parse(filepath)
        root = tree.getroot()
        ns = {'fb2': 'http://www.gribuser.ru/xml/fictionbook/2.0'}
        bodies = root.findall('.//fb2:body', ns)
        text = []
        for body in bodies:
            for p in body.findall('.//fb2:p', ns):
                if p.text:
                    text.append(p.text)
        raw_text = '\n'.join(text)
        clean_text = self.preprocess_text(raw_text)
        self.text = clean_text
        self.title = root.find('.//fb2:book-title', ns)
        if self.title is not None:
            self.title = self.title.text
        else:
            self.title = "Без названия"
        return self.text 