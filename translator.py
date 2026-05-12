# translator.py

import os
import torch
import re

from transformers import (
    MarianMTModel,
    MarianTokenizer
)


class OfflineTranslator:
    def __init__(self):

        # ПУТЬ К ЛОКАЛЬНОЙ МОДЕЛИ
        model_path = (
            r"C:\Users\louk\Desktop\codes\project\model"
        )

        print("LOADING LOCAL MODEL...")

        # tokenizer
        self.tokenizer = (
            MarianTokenizer.from_pretrained(
                model_path,
                local_files_only=True
            )
        )

        # model
        self.model = (
            MarianMTModel.from_pretrained(
                model_path,
                local_files_only=True
            )
        )

        # устройство
        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.model.to(self.device)

        self.model.eval()

        print("MODEL LOADED")

    def normalize(self, text):

        text = text.strip()

        # нормализуем пробелы
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text

    def translate(self, text):

        text = self.normalize(text)

        if not text:
            return ""

        try:

            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                padding=True
            ).to(self.device)

            with torch.no_grad():

                translated = self.model.generate(
                    **inputs,
                    max_new_tokens=32
                )

            result = self.tokenizer.decode(
                translated[0],
                skip_special_tokens=True
            )

            return result

        except Exception as e:

            print(
                "TRANSLATION ERROR:",
                e
            )

            return ""