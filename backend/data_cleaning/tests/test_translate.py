from django.test import TestCase
from unittest.mock import patch
from data_cleaning.translate import translate_text, translate_texts

class TranslationTests(TestCase):
    @patch('data_cleaning.translate.translator')
    def test_translate_text_french(self, mock_translator):
        """
        Test that a French text is properly translated to English.
        """
        # Mocking the translation output
        mock_translator.return_value = [{"translation_text": "Hello world"}]
        
        french_text = "Bonjour le monde"
        result = translate_text(french_text)
        
        self.assertEqual(result, "Hello world")

    def test_translate_text_english(self):
        """
        Test that an English text is returned as is.
        """
        english_text = "Hello World"
        result = translate_text(english_text)
        
        self.assertEqual(result, english_text)
    
    @patch('data_cleaning.translate.detect_language')
    def test_translate_text_unsupported_language(self, mock_detect_language):
        """
        Test that text in an unsupported language returns an empty string.
        """
        mock_detect_language.return_value = "es"  # Mocking Spanish detection
        
        spanish_text = "Hola Mundo"
        result = translate_text(spanish_text)
        
        self.assertEqual(result, "")
    
    @patch('data_cleaning.translate.translator')
    @patch('data_cleaning.translate.detect_language')
    def test_translate_texts(self, mock_detect_language, mock_translator):
        """
        Test that a list of texts is properly translated, ignoring unsupported languages.
        """
        # Mock the translation for French texts
        mock_translator.return_value = [{"translation_text": "Hello World"}]
        mock_detect_language.side_effect = lambda text: {
            "Bonjour le monde": "fr",
            "Hello World": "en",
            "Hola Mundo": "es"
        }[text]
        
        texts = ["Bonjour le monde", "Hello World", "Hola Mundo"]
        expected_results = ["Hello World", "Hello World"]
        
        result = translate_texts(texts)
        
        self.assertEqual(result, expected_results)

    @patch('data_cleaning.translate.translator')
    @patch('data_cleaning.translate.detect_language')
    def test_translate_text_fails_gracefully(self, mock_detect_language, mock_translator):
        """
        Test that an exception during translation is handled gracefully and returns an empty string.
        """
        mock_detect_language.return_value = "fr"
        mock_translator.side_effect = Exception("Mocked translation failure")
        
        french_text = "Bonjour le monde"
        result = translate_text(french_text)
        
        self.assertEqual(result, "")
