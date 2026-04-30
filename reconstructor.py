import json
import os
import re
from config import logger, PROTECTED_TERMS

class Reconstructor:
    def __init__(self, term_map):
        # We need the mapping from Phase 2 to swap placeholders back
        self.term_map = term_map

    def restore_terms(self, text):
        """Swaps [[TERM_X]] back to the original brand name."""
        restored_text = text
        for placeholder, original_term in self.term_map.items():
            restored_text = restored_text.replace(placeholder, original_term)
        return restored_text

    def reconstruct_html(self, original_segments, translated_segments, lang_code, direction):
        """
        In a full build, this would inject text back into a BeautifulSoup object.
        For this step, we will create a structured 'Final Page' artifact.
        """
        logger.info(f"Reconstructing HTML for {lang_code} ({direction})")
        
        final_output = []
        
        # Create a lookup for translated text by segment_id
        translations = {s['segment_id']: s['translated_text'] for s in translated_segments}

        for orig in original_segments:
            seg_id = orig['segment_id']
            translated_text = translations.get(seg_id, orig['source_text'])
            
            # Restore terms
            final_text = self.restore_terms(translated_text)
            
            final_output.append({
                "id": seg_id,
                "url": orig['page_url'],
                "tag": orig['html_path'],
                "content": final_text
            })

        # Create a simple HTML-like preview file
        html_content = f"<!DOCTYPE html>\n<html lang='{lang_code}' dir='{direction}'>\n<body>\n"
        for item in final_output:
            html_content += f"  <{item['tag']}>{item['content']}</{item['tag']}>\n"
        html_content += "</body>\n</html>"

        return html_content

# --- TEST THIS STEP ---
if __name__ == "__main__":
    # 1. Load data from previous phases
    with open("data/extracted_segments.json", "r") as f:
        original_segments = json.load(f)
    
    # Assuming Arabic test from Phase 3
    lang_code = "ar"
    try:
        with open(f"translations/{lang_code}/segments.json", "r", encoding='utf-8') as f:
            translated_segments = json.load(f)
    except FileNotFoundError:
        logger.error("Translations not found! Run Phase 3 first.")
        exit()

    # 2. Re-create the term map (In a real app, this would be persisted)
    # For the test, we'll rebuild it based on config
    term_map = {f"[[TERM_{i}]]": term for i, term in enumerate(PROTECTED_TERMS)}

    recon = Reconstructor(term_map)
    final_html = recon.reconstruct_html(original_segments[:3], translated_segments, lang_code, "rtl")

    # 3. Save the final output
    output_dir = f"output/{lang_code}"
    os.makedirs(output_dir, exist_ok=True)
    with open(f"{output_dir}/index.html", "w", encoding='utf-8') as f:
        f.write(final_html)

    logger.info(f"Phase 4 Test Complete. Final HTML saved to {output_dir}/index.html")