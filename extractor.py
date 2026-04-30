import requests
from bs4 import BeautifulSoup
import json
import re
from config import PROTECTED_TERMS, logger

class Extractor:
    def __init__(self):
        self.term_map = {}

    def shield_terms(self, text):
        """Replaces protected terms with [[TERM_ID]] to prevent translation."""
        temp_text = text
        for i, term in enumerate(PROTECTED_TERMS):
            placeholder = f"[[TERM_{i}]]"
            self.term_map[placeholder] = term
            # Case insensitive replacement
            temp_text = re.sub(re.escape(term), placeholder, temp_text, flags=re.IGNORECASE)
        return temp_text

    def fetch_and_extract(self, url):
        logger.info(f"Fetching: {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        segments = []
        # Target specific tags for translation
        tags_to_extract = ['h1', 'h2', 'h3', 'p', 'a', 'button']
        
        for i, element in enumerate(soup.find_all(tags_to_extract)):
            source_text = element.get_text().strip()
            if not source_text: continue
            
            segments.append({
                "segment_id": f"seg_{i}",
                "page_url": url,
                "html_path": str(element.name), # Simplified for this demo
                "source_text": source_text,
                "shielded_text": self.shield_terms(source_text),
                "contains_html": len(element.find_all()) > 0
            })
            
        return segments, str(soup)

# --- TEST THIS STEP ---
if __name__ == "__main__":
    ex = Extractor()
    test_url = "https://deriv.com/"
    segments, raw_html = ex.fetch_and_extract(test_url)
    
    with open("data/extracted_segments.json", "w") as f:
        json.dump(segments, f, indent=2)
    
    logger.info(f"Extracted {len(segments)} segments. Test Passed.")