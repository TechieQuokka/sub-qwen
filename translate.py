#!/usr/bin/env python3
"""
Qwen2.5-14B Subtitle Translation CLI Tool

Usage:
    python translate.py --input subtitle.json --output subtitle_kr.json \
                        --input-lang ja --target-lang ko
"""
import argparse
import sys
from tqdm import tqdm

from utils import load_model, translate_segment, get_field_name, load_json, save_json
from config import LANGUAGE_MAP, CONTEXT_HISTORY, USE_CONTEXT


def main():
    parser = argparse.ArgumentParser(
        description='Qwen2.5-14B Multilingual Subtitle Translator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Japanese to Korean
  python translate.py --input subtitle.json --output subtitle_kr.json --input-lang ja --target-lang ko

  # English to Korean
  python translate.py --input subtitle.json --output subtitle_en.json --input-lang en --target-lang ko

  # Korean to English (no context)
  python translate.py --input subtitle.json --output subtitle_en.json --input-lang ko --target-lang en --no-context

Supported languages: ko, en, ja, zh, zh-tw, es, fr, de, ru
        """
    )

    # Required arguments
    parser.add_argument('--input', required=True, help='Input JSON subtitle file')
    parser.add_argument('--output', required=True, help='Output JSON file')
    parser.add_argument('--input-lang', required=True, choices=list(LANGUAGE_MAP.keys()),
                       help='Source language code')
    parser.add_argument('--target-lang', required=True, choices=list(LANGUAGE_MAP.keys()),
                       help='Target language code')

    # Optional arguments
    parser.add_argument('--no-context', action='store_true',
                       help='Disable context-aware translation')

    args = parser.parse_args()

    print("=" * 60)
    print("🔄 Qwen2.5-14B Subtitle Translator")
    print("=" * 60)

    # Step 1: Load model
    print("\n[1/4] Loading Qwen2.5-14B model...")
    try:
        model = load_model()
    except Exception as e:
        print(f"\n❌ Model loading failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Step 2: Load input JSON
    print(f"\n[2/4] Loading input file: {args.input}")
    try:
        data = load_json(args.input)
        segments = data['segments']
    except Exception as e:
        print(f"\n❌ Failed to load input file: {e}", file=sys.stderr)
        sys.exit(1)

    # Step 3: Translate segments
    use_context = USE_CONTEXT and not args.no_context
    context_mode = "with context" if use_context else "without context"
    print(f"\n[3/4] Translating from {LANGUAGE_MAP[args.input_lang]} to "
          f"{LANGUAGE_MAP[args.target_lang]} ({context_mode})...")

    field_name = get_field_name(args.target_lang)
    failed_count = 0

    for i, seg in enumerate(tqdm(segments, desc="Progress", unit="segment")):
        try:
            # Build context from previous segments
            if use_context and i > 0:
                start_idx = max(0, i - CONTEXT_HISTORY)
                context_history = [segments[j]['text'] for j in range(start_idx, i)]
            else:
                context_history = None

            # Translate
            translation = translate_segment(
                seg['text'],
                args.input_lang,
                args.target_lang,
                model,
                context_history
            )
            seg[field_name] = translation

            # Track failures
            if translation.startswith("[Translation Error"):
                failed_count += 1

        except KeyboardInterrupt:
            print("\n\n⚠️  Translation interrupted by user")
            print("Saving progress...")
            break

        except Exception as e:
            print(f"\n⚠️  Unexpected error: {e}")
            seg[field_name] = f"[Error: {str(e)}]"
            failed_count += 1

    # Step 4: Save results
    print(f"\n[4/4] Saving results to: {args.output}")
    try:
        save_json(data, args.output)
    except Exception as e:
        print(f"\n❌ Failed to save output: {e}", file=sys.stderr)
        sys.exit(1)

    # Summary
    print("\n" + "=" * 60)
    print("✅ Translation Complete!")
    print("=" * 60)
    print(f"Total segments: {len(segments)}")
    print(f"Successful: {len(segments) - failed_count}")
    if failed_count > 0:
        print(f"Failed: {failed_count}")
    print(f"Output: {args.output}")
    print("=" * 60)


if __name__ == '__main__':
    main()
