import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from config import logger

load_dotenv()

class Translator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini" # Using mini for cost-efficiency

    def translate_segments(self, segments, target_lang):
        """Translates a batch of segments into the target language."""
        logger.info(f"Starting translation for: {target_lang['name']}")
        
        # Prepare the instructions
        system_instruction = (
            f"You are a professional localization expert for Deriv. "
            f"Translate the following content into {target_lang['name']}. "
            f"IMPORTANT: \n"
            f"1. DO NOT translate anything inside double brackets like [[TERM_0]].\n"
            f"2. Preserve all HTML tags (e.g., <strong>, <a>) exactly.\n"
            f"3. Maintain the professional, high-tech tone of a trading platform.\n"
            f"4. For Arabic, use Modern Standard Arabic and ensure natural phrasing."
        )

        translated_data = []

        # In a real build, we'd batch these to save tokens, 
        # but for this step, we'll process them to ensure clarity.
        for seg in segments:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": seg['shielded_text']}
                    ],
                    temperature=0.3 # Low temperature for consistency
                )
                
                translated_text = response.choices[0].message.content
                
                translated_data.append({
                    "segment_id": seg['segment_id'],
                    "language_code": target_lang['code'],
                    "source_text": seg['source_text'],
                    "translated_text": translated_text,
                    "protected_terms_restored": False, # Will handle in Phase 4
                    "qa_status": "pending"
                })
            except Exception as e:
                logger.error(f"Failed to translate segment {seg['segment_id']}: {e}")

        return translated_data

# --- TEST THIS STEP ---
if __name__ == "__main__":
    # Load extracted segments from Phase 2
    with open("data/extracted_segments.json", "r") as f:
        segments = json.load(f)

    # Pick Arabic as the test language (High priority)
    target_lang = {"code": "ar", "name": "Arabic", "direction": "rtl"}
    
    translator = Translator()
    # Test with just the first 3 segments to save your credits
    results = translator.translate_segments(segments[:3], target_lang)
    
    # Save results
    lang_dir = f"translations/{target_lang['code']}"
    os.makedirs(lang_dir, exist_ok=True)
    with open(f"{lang_dir}/segments.json", "w", encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Phase 3 Test Complete. Translated segments saved to {lang_dir}/segments.json")