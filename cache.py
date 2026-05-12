import time

class TranslationCache:
    def __init__(self, ttl=3600):
        self.cache = {}
        self.ttl = ttl

    def normalize(self, text):
        return text.lower().strip()

    def get(self, text):
        key = self.normalize(text)

        if key in self.cache:
            value, timestamp = self.cache[key]

            if time.time() - timestamp < self.ttl:
                return value

            del self.cache[key]

        return None

    def set(self, text, translation):
        key = self.normalize(text)

        self.cache[key] = (
            translation,
            time.time()
        )