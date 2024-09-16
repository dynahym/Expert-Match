from langdetect import detect, DetectorFactory
from typing import List
from transformers import pipeline

# Ensure consistent results from langdetect
DetectorFactory.seed = 0

translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")

def detect_language(text: str) -> str:
    """
    Detect the language of a given text using the langdetect library.

    Args:
        text (str): The input text to detect language from.

    Returns:
        str: The detected language code (e.g., 'fr' for French, 'en' for English).
    """
    try:
        lang = detect(text)
        return lang
    except Exception as e:
        print(f"Language detection failed: {e}")
        return ""

def translate_text(text: str) -> str:
    """
    Translate the text from French to English if detected as French.
    If the text is in English, return it as is. For other languages, return an empty string.

    Args:
        text (str): The input text to translate.

    Returns:
        str: The translated text if it's French, the original text if it's English,
             or an empty string if the language is neither French nor English.
    """
    detected_lang = detect_language(text)
    if detected_lang == "fr":
        try:
            translation = translator(text, max_length=400)
            return translation[0]["translation_text"]
        except Exception as e:
            print(f"Translation failed: {e}")
            return ""
    elif detected_lang == "en":
        return text
    else:
        return ""

def translate_texts(texts: List[str]) -> List[str]:
    """
    Translate a list of texts. French texts will be translated to English.
    English texts will be returned as is. Other languages will be ignored.

    Args:
        texts (List[str]): A list of texts to translate.

    Returns:
        List[str]: A list of translated or original texts, excluding unsupported languages.
    """
    translated_texts = [translate_text(text) for text in texts if translate_text(text) != ""]
    return translated_texts
