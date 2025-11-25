"""
JSON subtitle file handling utilities
"""
import json
import os
import sys


def load_json(filepath):
    """
    Load ASR JSON subtitle file

    Args:
        filepath (str): Path to JSON file

    Returns:
        dict: Parsed JSON data with 'segments' list

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If JSON structure is invalid
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Input file not found: {filepath}")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Validate structure
        if 'segments' not in data:
            raise ValueError(
                "Invalid subtitle format: 'segments' key not found"
            )

        if not isinstance(data['segments'], list):
            raise ValueError(
                "Invalid subtitle format: 'segments' must be a list"
            )

        print(f"✅ Loaded {len(data['segments'])} segments from {filepath}")
        return data

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON file: {e}", file=sys.stderr)
        raise


def save_json(data, filepath):
    """
    Save translated data to JSON file

    Args:
        data (dict): Data to save
        filepath (str): Output file path
    """
    try:
        # Create directory if needed
        output_dir = os.path.dirname(filepath)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # Save with proper formatting
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ Saved {len(data['segments'])} segments to {filepath}")

    except Exception as e:
        print(f"❌ Failed to save file: {e}", file=sys.stderr)
        raise
