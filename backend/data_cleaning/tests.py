from django.test import TestCase
from unittest.mock import patch
from .clean import normalize_text, is_similar, remove_duplicates, fetch_researcher_data

class TestCleanFunctions(TestCase):
    
    def test_normalize_text(self):
        self.assertEqual(normalize_text('Hello $World$!'), 'hello')
        self.assertEqual(normalize_text('[Test]  Example!!'), 'example')

    def test_is_similar(self):
        self.assertTrue(is_similar('Hello World', 'Hello World'))
        self.assertFalse(is_similar('Hello World', 'Goodbye World', threshold=70))

    def test_remove_duplicates(self):
        data = [
            'Hello World',
            'Hello    World!',
            'Another Article',
            'Another   Article!!'
        ]
        unique_data = remove_duplicates(data)
        self.assertEqual(unique_data, ['Hello World', 'Another Article'])
