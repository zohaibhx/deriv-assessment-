import logging
import os

# 1. Protected Terms (Inferred from Deriv context)
PROTECTED_TERMS = {
    "Deriv", "Deriv Bot", "Deriv MT5", "Deriv X", 
    "SmartTrader", "Forex", "Synthetic Indices", 
    "Multipliers", "CFDs", "Binary.com"
}

# 2. Setup Logging for the "Audit Trail"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("DerivPipeline")

# 3. Ensure directories exist
for folder in ["translations", "output", "data"]:
    os.makedirs(folder, exist_ok=True)