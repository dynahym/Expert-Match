import os
from django.test import TestCase
from .classifier import clean_area, classify_article, classify_articles

class ClassifierTests(TestCase):
    
    def setUp(self):
        """Set up any necessary data for the tests."""
        self.valid_article_text = (
            "This article discusses the advances in artificial intelligence (AI) "
            "and its impact on various domains such as healthcare, finance, and education."
        )
        self.invalid_article_text = "This article has no relevant content."

        self.articles = [
            "Exploring deep learning techniques in natural language processing.",
            "Recent advancements in quantum computing applications.",
            "A study on the impacts of climate change on biodiversity.",
        ]

    def test_clean_area(self):
        """Test the clean_area function."""
        area = "Artificial Intelligence (AI)"
        expected = "artificial intelligence"
        result = clean_area(area)
        self.assertEqual(result, expected)

    def test_classify_article_valid(self):
        """Test classify_article with a valid article."""
        result = classify_article(self.valid_article_text)
        # Check if the result is a list and has expected items
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)  # Ensure the list is not empty

    def test_classify_article_invalid(self):
        """Test classify_article with an invalid article."""
        result = classify_article(self.invalid_article_text)
        # Assuming an empty list is returned for invalid content
        self.assertEqual(result, [])

    def test_classify_articles_empty(self):
        """Test classify_articles with an empty list."""
        result = classify_articles([])
        self.assertEqual(result, [])  # Should return an empty list
