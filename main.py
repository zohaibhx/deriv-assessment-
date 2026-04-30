# main.py
from extractor import Extractor
from translator import Translator
from reconstructor import Reconstructor
from qa_engine import QAEngine
import json
from config import logger, PROTECTED_TERMS

def run_pipeline():
    # 1. INIT
    logger.info("--- PIPELINE START ---")
    target_lang = {"code": "ar", "name": "Arabic", "direction": "rtl"}
    url = "https://deriv.com/"

    # 2. FETCH & EXTRACT
    ex = Extractor()
    segments, raw_html = ex.fetch_and_extract(url)

    # 3. TRANSLATE
    tr = Translator()
    # For speed in test, we translate 2 segments
    translations = tr.translate_segments(segments[:2], target_lang)

    # 4. RECONSTRUCT
    term_map = {f"[[TERM_{i}]]": term for i, term in enumerate(PROTECTED_TERMS)}
    recon = Reconstructor(term_map)
    final_html = recon.reconstruct_html(segments[:2], translations, "ar", "rtl")

    # 5. QA
    qa = QAEngine()
    qa_report = qa.run_checks(segments[:2], translations, "ar")
    
    logger.info("--- PIPELINE COMPLETE ---")
    print("Check 'output/ar/index.html' for the result!")

if __name__ == "__main__":
    run_pipeline()