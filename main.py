from capture import ScreenCapture
from ocr_engine import OCREngine
from translator import OfflineTranslator
from cache import TranslationCache
from pipeline import Pipeline
from overlay import run_overlay

def main():
    shared_data = {
        "translations": {}
    }

    capture = ScreenCapture()

    ocr = OCREngine()

    translator = OfflineTranslator()

    cache = TranslationCache()

    pipeline = Pipeline(
        capture,
        ocr,
        translator,
        cache,
        shared_data
    )

    pipeline.start()

    # Qt должен запускаться в main thread
    run_overlay(shared_data)


if __name__ == "__main__":
    main()