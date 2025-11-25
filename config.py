"""
Qwen2.5-14B Subtitle Translation Configuration
"""
import os

# ====== Model Configuration ======
MODEL_PATH = os.path.expanduser(
    "~/workspace/deeplearning/project/autokr2/polyglot-sub-pipeline/models/"
    "qwen2.5-14b-instruct-q4_k_m.gguf"
)

# GPU Settings (RTX 3060 12GB)
GPU_LAYERS = 40              # Adjust based on VRAM
CONTEXT_SIZE = 8192          # Qwen2.5 supports up to 32K
N_THREADS = 4
N_BATCH = 1024

# ====== Language Configuration ======
LANGUAGE_MAP = {
    'ko': 'Korean',
    'en': 'English',
    'ja': 'Japanese',
    'zh': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'ru': 'Russian'
}

FIELD_PREFIX = 'text_'  # Output field: text_ko, text_en, etc.

# ====== Inference Parameters ======
TEMPERATURE = 0.1
TOP_P = 0.3
MAX_TOKENS = 512
STOP_SEQUENCES = ["<|im_end|>", "\n\n\n"]

# ====== Context Settings ======
CONTEXT_HISTORY = 10         # Previous segments for context
USE_CONTEXT = True           # Enable context-aware translation

# ====== Prompt Templates ======
SYSTEM_PROMPT = """You are a professional translator specializing in anime subtitles and multimedia content.

Guidelines:
- Translate naturally while preserving the original meaning and nuance
- Maintain cultural references and context
- Keep translations concise and suitable for subtitles (avoid verbose explanations)
- Preserve formatting and punctuation style
- Do NOT add explanations or notes - only provide the direct translation"""

USER_PROMPT_TEMPLATE = "Translate the following {source_lang_name} text to {target_lang_name}:\n\n{text}"
