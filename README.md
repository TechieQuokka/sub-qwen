# Qwen2.5-14B Subtitle Translator

Professional multilingual translation system for anime subtitles and multimedia content using Qwen2.5-14B-Instruct.

## Features

- **Model**: Qwen2.5-14B-Instruct Q4_K_M (GGUF)
- **Backend**: llama.cpp with GPU acceleration
- **Context-Aware**: Maintains dialogue continuity across segments
- **Format Support**: ASR JSON subtitle files
- **Languages**: Japanese, Korean, English, Chinese, and more

## Installation

### Prerequisites
- Python 3.8+
- CUDA-capable GPU (recommended, RTX 3060+ with 12GB+ VRAM)
- 10GB disk space for model

### Setup

```bash
# 1. Navigate to project directory
cd ~/workspace/deeplearning/project/autokr2/polyglot-sub-pipeline/sub-qwen

# 2. Install dependencies with GPU support
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
pip install tqdm

# 3. Download model (if not already done)
cd ../models
huggingface-cli download Qwen/Qwen2.5-14B-Instruct-GGUF \
    qwen2.5-14b-instruct-q4_k_m.gguf \
    --local-dir . \
    --local-dir-use-symlinks False
```

## Usage

### Basic Translation

```bash
# Japanese to Korean
python translate.py \
    --input test_input.json \
    --output test_output.json \
    --input-lang ja \
    --target-lang ko
```

### Test with Provided Sample

```bash
# Test with the included 5-segment sample file
python translate.py \
    --input test_input.json \
    --output test_output_kr.json \
    --input-lang ja \
    --target-lang ko
```

### Real Anime Subtitle Translation

```bash
# Translate the 410-segment anime file
python translate.py \
    --input /home/beethoven/workspace/deeplearning/project/autokr2/data/asr_transcription_data/[SubsPlease]\ Yasei\ no\ Last\ Boss\ ga\ Arawareta!\ -\ 08\ \(480p\)\ [30425761].json \
    --output anime_ep08_kr.json \
    --input-lang ja \
    --target-lang ko
```

### Disable Context (Faster)

```bash
python translate.py \
    --input document.json \
    --output document_kr.json \
    --input-lang en \
    --target-lang ko \
    --no-context
```

### Supported Languages

- `ko`: Korean
- `en`: English
- `ja`: Japanese
- `zh`: Chinese (Simplified)
- `zh-tw`: Chinese (Traditional)
- `es`: Spanish
- `fr`: French
- `de`: German
- `ru`: Russian

## Configuration

Edit `config.py` to adjust:

### GPU Settings
```python
GPU_LAYERS = 40          # Increase/decrease based on VRAM
CONTEXT_SIZE = 8192      # Context window size
```

### Translation Quality
```python
TEMPERATURE = 0.1        # Lower (0.05) = more literal, Higher (0.2) = more creative
TOP_P = 0.3             # Sampling parameter
MAX_TOKENS = 512        # Maximum translation length
```

### Context Settings
```python
CONTEXT_HISTORY = 5     # Number of previous segments for context
USE_CONTEXT = True      # Enable/disable context-aware translation
```

## Performance

**Hardware**: RTX 3060 12GB
**Speed**: ~15-25 tokens/sec (~2-3 seconds per segment)
**1000 segments**: ~40-60 minutes

## Troubleshooting

### Out of Memory Errors
Reduce `GPU_LAYERS` in `config.py`:
```python
GPU_LAYERS = 30  # Try 30 → 20 → 10
```

### Slow Inference
- Use `--no-context` flag
- Reduce `CONTEXT_SIZE` in `config.py`
```python
CONTEXT_SIZE = 4096  # Instead of 8192
```

### Verbose Translations
- Lower `MAX_TOKENS` in `config.py`
```python
MAX_TOKENS = 256  # Instead of 512
```
- Update `SYSTEM_PROMPT` to emphasize conciseness

### Monitor GPU Usage
```bash
watch -n 1 nvidia-smi
```

## Output Format

The translator adds a new field to each segment with the language code:

**Input:**
```json
{
  "segments": [
    {
      "start": 0.0,
      "end": 2.5,
      "text": "こんにちは、元気ですか？"
    }
  ]
}
```

**Output:**
```json
{
  "segments": [
    {
      "start": 0.0,
      "end": 2.5,
      "text": "こんにちは、元気ですか？",
      "text_ko": "안녕하세요, 잘 지내세요?"
    }
  ]
}
```

## Testing Workflow

1. **Quick Test** (5 segments, ~10-15 seconds):
   ```bash
   python translate.py --input test_input.json --output test_output.json \
                       --input-lang ja --target-lang ko
   ```

2. **Quality Check**: Manually review `test_output.json`

3. **Full Translation** (410 segments, ~15-25 minutes):
   ```bash
   python translate.py --input <anime_json_path> --output anime_kr.json \
                       --input-lang ja --target-lang ko
   ```

## Project Structure

```
sub-qwen/
├── translate.py           # Main CLI tool
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── test_input.json        # Sample test file
└── utils/
    ├── __init__.py
    ├── model_loader.py    # Model loading
    ├── translator.py      # Translation engine
    └── json_handler.py    # JSON I/O
```

## License

MIT License
