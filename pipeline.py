# pipeline.py

from queue import Queue
from threading import Thread
import time


class Pipeline:
    def __init__(
        self,
        capture,
        ocr,
        translator,
        cache,
        shared_data
    ):
        self.capture = capture

        self.ocr = ocr

        self.translator = translator

        self.cache = cache

        self.shared_data = shared_data

        # всегда только последний кадр
        self.ocr_queue = Queue(maxsize=1)

        # очередь строк
        self.translate_queue = Queue(maxsize=20)

    def start(self):

        Thread(
            target=self.capture_loop,
            daemon=True
        ).start()

        Thread(
            target=self.ocr_loop,
            daemon=True
        ).start()

        Thread(
            target=self.translate_loop,
            daemon=True
        ).start()

        Thread(
            target=self.cleanup_loop,
            daemon=True
        ).start()

    def capture_loop(self):

        while True:

            frame = self.capture.grab()

            # оставляем только последний кадр
            while not self.ocr_queue.empty():

                try:
                    self.ocr_queue.get_nowait()

                except:
                    break

            self.ocr_queue.put(frame)

            # realtime delay
            time.sleep(0.35)

    def ocr_loop(self):

        while True:

            frame = self.ocr_queue.get()

            lines = self.ocr.extract_lines(
                frame
            )

            # очищаем старые OCR задачи
            while not self.translate_queue.empty():

                try:
                    self.translate_queue.get_nowait()

                except:
                    break

            for line in lines:

                if self.translate_queue.full():
                    break

                self.translate_queue.put(line)

    def translate_loop(self):

        while True:

            item = self.translate_queue.get()

            text = item["text"]

            print("TRANSLATING:", text)

            # игнор русского
            if any(
                "а" <= c.lower() <= "я"
                or c.lower() == "ё"
                for c in text
            ):
                continue

            # мусор UI
            ui_words = [
                "Файл",
                "Правка",
                "Справка",
                "Вид",
                "Format"
            ]

            if text in ui_words:
                continue

            normalized = (
                self.translator.normalize(
                    text
                )
            )

            if not normalized:
                continue

            # уже недавно переводили?
            recently_seen = False

            for existing in self.shared_data[
                "translations"
            ].values():

                existing_text = existing.get(
                    "original",
                    ""
                )

                if existing_text == normalized:

                    if time.time() - existing[
                        "timestamp"
                    ] < 5:

                        recently_seen = True
                        break

            if recently_seen:
                continue

            # cache
            cached = self.cache.get(
                normalized
            )

            if cached:

                translation = cached

            else:

                try:

                    translation = (
                        self.translator.translate(
                            normalized
                        )
                    )

                    print(
                        "RESULT:",
                        translation
                    )

                    if not translation:
                        continue

                    self.cache.set(
                        normalized,
                        translation
                    )

                except Exception as e:

                    print(
                        "TRANSLATION ERROR:",
                        e
                    )

                    continue

            # ключ по позиции
            key = (
                f"{item['x']//100}_"
                f"{item['y']//40}_"
                f"{normalized}"
            )

            now = time.time()

            existing = self.shared_data[
                "translations"
            ].get(key)

            # не заменяем хороший текст
            # плохим OCR
            if existing:

                old_len = len(
                    existing["original"]
                )

                new_len = len(
                    normalized
                )

                if new_len < old_len:
                    continue

            self.shared_data[
                "translations"
            ][key] = {

                "x": item["x"],

                "y": item["y"],

                "translation": translation,

                "original": normalized,

                "timestamp": now
            }

    def cleanup_loop(self):

        while True:

            now = time.time()

            to_delete = []

            for key, item in self.shared_data[
                "translations"
            ].items():

                # долго держим текст
                if now - item[
                    "timestamp"
                ] > 30:

                    to_delete.append(
                        key
                    )

            for key in to_delete:

                del self.shared_data[
                    "translations"
                ][key]

            time.sleep(2)