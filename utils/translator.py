"""
Translation engine for subtitle segments
"""
from config import (
    LANGUAGE_MAP, FIELD_PREFIX, TEMPERATURE, TOP_P, MAX_TOKENS,
    STOP_SEQUENCES, SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
)


def get_field_name(target_lang):
    """Generate output field name (e.g., 'text_ko', 'text_en')"""
    return f"{FIELD_PREFIX}{target_lang}"


def build_prompt(text, input_lang, target_lang, context_history=None):
    """
    Build ChatML-formatted prompt for Qwen2.5

    Args:
        text (str): Source text to translate
        input_lang (str): Input language code
        target_lang (str): Target language code
        context_history (list): Optional previous dialogue lines

    Returns:
        str: Formatted ChatML prompt
    """
    source_lang_name = LANGUAGE_MAP[input_lang]
    target_lang_name = LANGUAGE_MAP[target_lang]

    # Build user message with context if available
    if context_history and len(context_history) > 0:
        context_lines = "\n".join([f"- {ctx}" for ctx in context_history])
        user_message = f"""Previous dialogue for context:
{context_lines}

Now translate the following {source_lang_name} text to {target_lang_name}:
{text}"""
    else:
        user_message = USER_PROMPT_TEMPLATE.format(
            source_lang_name=source_lang_name,
            target_lang_name=target_lang_name,
            text=text
        )

    # ChatML format
    prompt = f"""<|im_start|>system
{SYSTEM_PROMPT}<|im_end|>
<|im_start|>user
{user_message}<|im_end|>
<|im_start|>assistant
"""

    return prompt


def translate_segment(text, input_lang, target_lang, model, context_history=None):
    """
    Translate a single subtitle segment

    Args:
        text (str): Source text
        input_lang (str): Input language code
        target_lang (str): Target language code
        model: Loaded Llama model instance
        context_history (list): Optional previous dialogue lines

    Returns:
        str: Translated text

    Raises:
        ValueError: If language codes are invalid
    """
    # Validate languages
    if input_lang not in LANGUAGE_MAP:
        raise ValueError(
            f"Unsupported input language: {input_lang}\n"
            f"Supported: {list(LANGUAGE_MAP.keys())}"
        )

    if target_lang not in LANGUAGE_MAP:
        raise ValueError(
            f"Unsupported target language: {target_lang}\n"
            f"Supported: {list(LANGUAGE_MAP.keys())}"
        )

    # Build prompt
    prompt = build_prompt(text, input_lang, target_lang, context_history)

    # Generate translation
    try:
        response = model(
            prompt,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            stop=STOP_SEQUENCES,
            echo=False
        )

        # Extract translation
        translated = response['choices'][0]['text'].strip()
        return translated

    except Exception as e:
        print(f"⚠️  Translation failed for: {text[:50]}...")
        print(f"   Error: {e}")
        return f"[Translation Error: {str(e)}]"
