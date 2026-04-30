# Deriv Localization Pipeline

A professional, modular, and replayable translation pipeline built for Deriv website content. This engine automates the extraction of translatable strings, protects brand assets, and reconstructs localized HTML with RTL support.

## 🛠 Features

- **Structural Integrity:** Extracts text from `<h1>`, `<p>`, `<a>`, and `<button>` tags while keeping HTML skeletons intact.
- **Brand Protection:** Uses a deterministic regex-shielding system to ensure terms like `Deriv Bot` and `SmartTrader` are never incorrectly translated.
- **Arabic RTL Optimization:** Automatically injects `dir="rtl"` and `lang="ar"` metadata into reconstructed pages.
- **Cost & QA Reporting:** Generates an automated audit trail (`qa_report.json`) including token usage estimates and HTML tag validation.
- **Modular Design:** Segregated stages (Extract -> Translate -> Reconstruct -> QA) following the PDR (Plan, Design, Run) framework.

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.12+ installed.

### 2. Installation
```powershell
# Clone the repository
git clone <your-repo-url>
cd deriv-assessment

# Install dependencies
py -m pip install requests beautifulsoup4 python-dotenv openai
