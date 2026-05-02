import json
import os
from config import logger

def verify_pipeline_integrity():
    logger.info("--- STARTING FINAL PIPELINE VALIDATION ---")
    
    # 1. Load Inputs
    try:
        with open("pages.json", "r") as f:
            expected_pages = json.load(f)["pages"]
        with open("target_languages.json", "r") as f:
            target_langs = json.load(f)["target_languages"]
    except FileNotFoundError:
        print("❌ CRITICAL: Input config files missing.")
        return

    # 2. Check Stage Artifacts
    required_files = [
        "data/extracted_segments.json",
        "qa_report.json",
        "logs/pipeline.log"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ STAGE COMPLETE: {file} exists.")
        else:
            print(f"❌ STAGE MISSING: {file} is missing.")

    # 3. Verify Page Coverage
    with open("data/extracted_segments.json", "r") as f:
        extracted = json.load(f)
        extracted_urls = {seg['page_url'] for seg in extracted}
    
    for url in expected_pages:
        if url in extracted_urls:
            print(f"✅ PAGE COVERED: {url}")
        else:
            print(f"⚠️ PAGE MISSING: {url} was not processed.")

    # 4. Verify Language Requirements (Arabic Priority)
    lang_codes = [lang['code'] for lang in target_langs]
    if "ar" in lang_codes:
        if os.path.exists("output/ar/index.html"):
            print("✅ ARABIC PRIORITY: Output exists and is correctly located.")
        else:
            print("❌ ARABIC PRIORITY: Arabic was requested but output/ar/index.html is missing.")

    # 5. Check QA Status
    with open("qa_report.json", "r") as f:
        qa = json.load(f)
        if not qa.get("qa_issues"):
            print("✅ QA STATUS: No issues detected in the final segments.")
        else:
            print(f"⚠️ QA STATUS: {len(qa['qa_issues'])} issues flagged. Check qa_report.json.")

    print("\n--- VALIDATION SUMMARY ---")
    print(f"Pages Expected: {len(expected_pages)}")
    print(f"Pages Found:    {len(extracted_urls)}")
    print(f"Languages:      {', '.join(lang_codes)}")

if __name__ == "__main__":
    verify_pipeline_integrity()
