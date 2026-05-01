import json
import os

# --- CONTROLLED VOCABULARIES (Strict matching) ---
VALID_SENTIMENTS = {"positive", "negative", "neutral", "mixed"}
VALID_TOPICS = {
    "withdrawal", "account_suspension", "spread_pricing", 
    "product_feedback", "regulatory", "technical", 
    "deposit", "kyc", "general"
}
VALID_TEAMS = {
    "Customer Support", "Legal", "Compliance", 
    "PR/Comms", "Product", "Engineering", "Finance"
}

def validate_pipeline():
    print("🚀 Starting Pipeline Validation...")
    
    required_files = [
        "data/posts.json",
        "output/preprocessed_posts.json",
        "output/classified_posts.json",
        "output/narratives.json",
        "output/risk_scores.json",
        "output/escalation_routing.json",
        "output/response_drafts.md",
        "output/llm_calls.jsonl"
    ]

    # 1. Check File Existence
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")

    # 2. Validate Preprocessing (P10 Malay Translation)
    with open("output/preprocessed_posts.json", "r") as f:
        preprocessed = json.load(f)
        p10 = next((p for p in preprocessed if p["post_id"] == "P10"), None)
        if p10 and p10.get("translated"):
            print("✅ P10 (Malay) successfully translated.")
        else:
            print("❌ P10 translation record missing or incorrect.")

    # 3. Validate Classification Vocabularies
    with open("output/classified_posts.json", "r") as f:
        classified = json.load(f)
        for post in classified:
            if post["sentiment"] not in VALID_SENTIMENTS:
                print(f"❌ Invalid sentiment in {post['post_id']}: {post['sentiment']}")
            if post["topic"] not in VALID_TOPICS:
                print(f"❌ Invalid topic in {post['post_id']}: {post['topic']}")

    # 4. Validate Routing Vocabulary
    with open("output/escalation_routing.json", "r") as f:
        routing = json.load(f)
        for item in routing:
            for team in item["teams"]:
                if team not in VALID_TEAMS:
                    print(f"❌ Invalid team assigned in {item['post_id']}: {team}")

    # 5. Check LLM Logs
    with open("output/llm_calls.jsonl", "r") as f:
        logs = f.readlines()
        if len(logs) >= 4: # Min stages: Classify, Narrate, Route, Draft
            print(f"✅ LLM Logs verified ({len(logs)} calls recorded).")
        else:
            print(f"⚠️ Warning: Fewer LLM calls logged than expected stages.")

    print("\n🏁 Validation Complete. If no '❌' appeared, your pipeline is submission-ready!")

if __name__ == "__main__":
    validate_pipeline()
