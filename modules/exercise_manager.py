import re

class ExerciseManager:
    def __init__(self, text):
        self.sentences = self.split_text(text)

    def split_text(self, text):
        # Простое разделение на предложения
        return re.split(r'(?<=[.!?…])\s+', text.strip())

    def get_sentence(self, idx):
        if 0 <= idx < len(self.sentences):
            return self.sentences[idx]
        return ""

    def count(self):
        return len(self.sentences) 