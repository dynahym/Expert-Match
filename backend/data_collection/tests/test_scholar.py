from django.test import TestCase
from unittest.mock import patch, MagicMock
from data_collection.scholar import get_scholar_articles_interests

class TestScholarFunctions(TestCase):
    
    @patch('data_collection.scholar.scholarly.search_author')
    @patch('data_collection.scholar.scholarly.fill')
    def test_get_scholar_articles_interests(self, mock_fill, mock_search_author):
        mock_author = MagicMock()
        mock_search_author.return_value = iter([mock_author])
        
        mock_fill.return_value = {
            "publications": [
                {"bib": {"title": "First Publication"}},
                {"bib": {"title": "Second Publication"}},
            ],
            "interests": ["machine learning", "artificial intelligence"]
        }
        
        interests, publications = get_scholar_articles_interests("Test Author")
        
        self.assertEqual(interests, ["machine learning", "artificial intelligence"])
        self.assertEqual(publications, ["first publication", "second publication"])

    def test_get_scholar_articles_no_results(self):
        with patch('data_collection.scholar.scholarly.search_author', return_value=iter([])):
            interests, publications = get_scholar_articles_interests("Unknown Author")
            self.assertEqual(interests, [])
            self.assertEqual(publications, [])
