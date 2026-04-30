import json
import os
from config import logger, PROTECTED_TERMS

class QAEngine:
    def __init__(self):
        self.report = []

    def run_checks(self, original_segments, translated_segments, lang_code):
        logger.info(f"Running QA for {lang_code}...")
        
        # Create lookup
        translations = {s['segment_id']: s for s in translated_segments}

        for orig in original_segments:
            seg_id = orig['segment_id']
            trans = translations.get(seg_id)

            issue = {
                "segment_id": seg_id,
                "language": lang_code,
                "checks": []
            }

            if not trans:
                issue["checks"].append("MISSING_TRANSLATION")
            else:
                text = trans['translated_text']
                
                # Check 1: Placeholder Corruption
                if "[[" in text and "]]" in text:
                     # This is actually GOOD for this stage because we haven't 
                     # restored them in the translation file yet, but we check 
                     # if the brackets are balanced.
                     if text.count("[[") != text.count("]]"):
                         issue["checks"].append("CORRUPTED_PLACEHOLDER")

                # Check 2: Empty Strings
                if not text.strip():
                    issue["checks"].append("EMPTY_TRANSLATION")

                # Check 3: Tag preservation (Basic count check)
                if orig['source_text'].count('<') != text.count('<'):
                    issue["checks"].append("HTML_TAG_MISMATCH")

            if issue["checks"]:
                self.report.append(issue)

        return self.report

    def generate_cost_report(self, translated_segments):
        # Mocking cost based on gpt-4o-mini pricing ($0.15 / 1M input tokens)
        # We'll estimate 1 token per 4 characters for the demo
        total_chars = sum(len(s['translated_text']) for s in translated_segments)
        estimated_tokens = total_chars / 4
        estimated_cost = (estimated_tokens / 1000000) * 0.15

        report = {
            "total_segments_processed": len(translated_segments),
            "estimated_token_usage": round(estimated_tokens, 2),
            "estimated_cost_usd": f"${estimated_cost:.6f}",
            "status": "Finalised"
        }
        return report

# --- TEST THIS STEP ---
if __name__ == "__main__":
    with open("data/extracted_segments.json", "r") as f:
        orig_segs = json.load(f)
    
    lang_code = "ar"
    with open(f"translations/{lang_code}/segments.json", "r", encoding='utf-8') as f:
        trans_segs = json.load(f)

    qa = QAEngine()
    qa_results = qa.run_checks(orig_segs[:3], trans_segs, lang_code)
    cost_data = qa.generate_cost_report(trans_segs)

    # Save final artifacts
    with open("qa_report.json", "w") as f:
        json.dump({"qa_issues": qa_results, "summary": cost_data}, f, indent=2)

    logger.info("Phase 5 Test Complete. qa_report.json generated.")
    print("\n--- PIPELINE SUMMARY ---")
    print(json.dumps(cost_data, indent=2))