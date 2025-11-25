"""
Model loading utilities for Qwen2.5-14B GGUF model
"""
from llama_cpp import Llama
import os
import sys

from config import MODEL_PATH, GPU_LAYERS, CONTEXT_SIZE, N_THREADS, N_BATCH


def load_model():
    """
    Load Qwen2.5-14B-Instruct GGUF with GPU acceleration

    Returns:
        Llama: Loaded model instance

    Raises:
        FileNotFoundError: If model file doesn't exist
        RuntimeError: If model loading fails
    """
    # Validate model path
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}\n"
            f"Please download the model using:\n"
            f"  huggingface-cli download Qwen/Qwen2.5-14B-Instruct-GGUF "
            f"qwen2.5-14b-instruct-q4_k_m.gguf --local-dir {os.path.dirname(MODEL_PATH)}"
        )

    print(f"Loading model: {MODEL_PATH}")
    print(f"GPU layers: {GPU_LAYERS}, Context: {CONTEXT_SIZE}, Batch: {N_BATCH}")

    try:
        model = Llama(
            model_path=MODEL_PATH,
            n_ctx=CONTEXT_SIZE,
            n_gpu_layers=GPU_LAYERS,
            n_threads=N_THREADS,
            n_batch=N_BATCH,
            verbose=False
        )

        print("✅ Model loaded successfully!")
        return model

    except Exception as e:
        print(f"❌ Failed to load model: {e}", file=sys.stderr)
        raise RuntimeError(f"Model loading failed: {e}")
