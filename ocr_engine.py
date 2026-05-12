# ocr_engine.py

from rapidocr_onnxruntime import RapidOCR


class OCREngine:
    def __init__(self):

        self.engine = RapidOCR()

    def extract_lines(self, image):

        result, _ = self.engine(image)

        if not result:
            return []

        items = []

        for item in result:

            try:

                box = item[0]

                text = item[1].strip()

                if not text:
                    continue

                # фикс OCR для I
                if text == "|":
                    text = "I"

                if text == "l":
                    text = "I"
                    
                if text == "工":
                    text = "I"
                    
                if text == "1":
                    text = "I"

                # игнор русского текста
                if any(
                    "а" <= c.lower() <= "я"
                    or c.lower() == "ё"
                    for c in text
                ):
                    continue

                x = int(box[0][0])

                y = int(box[0][1])

                items.append({

                    "text": text,

                    "x": x,

                    "y": y
                })

            except:
                pass

        # сортировка:
        # сверху вниз, слева направо
        items.sort(
            key=lambda i: (i["y"], i["x"])
        )

        lines = []

        current = []

        current_y = None

        for item in items:

            if current_y is None:

                current_y = item["y"]

                current.append(item)

                continue

            # слова одной строки
            if abs(item["y"] - current_y) < 25:

                current.append(item)

            else:

                # ВАЖНО:
                # сортировка слева направо
                current.sort(
                    key=lambda w: w["x"]
                )

                line_text = " ".join(
                    x["text"]
                    for x in current
                )

                lines.append({

                    "text": line_text,

                    "x": current[0]["x"],

                    "y": current[0]["y"]
                })

                current = [item]

                current_y = item["y"]

        # последняя строка
        if current:

            current.sort(
                key=lambda w: w["x"]
            )

            line_text = " ".join(
                x["text"]
                for x in current
            )

            lines.append({

                "text": line_text,

                "x": current[0]["x"],

                "y": current[0]["y"]
            })

        return lines