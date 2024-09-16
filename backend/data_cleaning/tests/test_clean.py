from django.test import TestCase
from data_cleaning.clean import remove_duplicates

class RemoveDuplicatesTests(TestCase):

    def setUp(self):
        # Test data
        self.articles = [
            "The quick brown fox jumps over the lazy dog.",
            "The quick brown fox jumps over the lazy dog.",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "A completely different article.",
            "Short",
            "The quick brown fox jumps over the lazy dog."
        ]

    def test_remove_duplicates_basic(self):
        result = remove_duplicates(self.articles, threshold=0.9)
        expected = [
            "The quick brown fox jumps over the lazy dog.",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "A completely different article."
        ]
        self.assertCountEqual(result, expected)

    def test_remove_duplicates_with_lower_threshold(self):
        result = remove_duplicates(self.articles, threshold=0.7)
        expected = [
            "The quick brown fox jumps over the lazy dog.",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "A completely different article."
        ]
        self.assertCountEqual(result, expected)

    def test_remove_duplicates_empty_list(self):
        result = remove_duplicates([])
        self.assertEqual(result, [])

    def test_remove_duplicates_single_article(self):
        result = remove_duplicates(["Single article"])
        self.assertEqual(result, ["Single article"])

    def test_remove_duplicates_articles_with_different_length(self):
        result = remove_duplicates([
            "One Short article",
            "Short",
            "A different article altogether",
            "Another one"
        ])
        expected = [
            "One Short article",
            "A different article altogether",
        ]
        self.assertCountEqual(result, expected)

    def test_remove_duplicates_very_similar_content(self):
        result = remove_duplicates([
            "The quick brown fox jumps over the lazy dog.",
            "The quick brown fox jumps over the lazy dog!",
            "The quick brown fox jumped over the lazy dog.",
            "A completely different article."
        ], threshold=0.8)
        expected = [
            "The quick brown fox jumps over the lazy dog.",
            "A completely different article."
        ]
        self.assertCountEqual(result, expected)
