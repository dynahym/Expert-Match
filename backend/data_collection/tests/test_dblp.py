import unittest, requests
from unittest.mock import patch, MagicMock
import data_collection.dblp
from data_collection.dblp import get_dblp_articles, get_html_content


class TestDblpArticles(unittest.TestCase):

    @patch('data_collection.dblp.requests.get')
    def test_get_html_content_success(self, mock_get):
        # Mock a successful request
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html>Test HTML Content</html>"
        mock_get.return_value = mock_response

        url = "https://example.com"
        result = get_html_content(url)
        self.assertEqual(result, "<html>Test HTML Content</html>")
        mock_get.assert_called_once_with(url)

    @patch('data_collection.dblp.requests.get')
    def test_get_html_content_failure(self, mock_get):
        # Mock a failed request
        mock_get.side_effect = requests.RequestException("Error fetching content")

        url = "https://example.com"
        result = get_html_content(url)
        self.assertEqual(result, "")  # Expecting an empty string on failure
        mock_get.assert_called_once_with(url)

    @patch('data_collection.dblp.get_html_content')
    @patch('data_collection.dblp.requests.get')
    def test_get_dblp_articles_success(self, mock_get, mock_get_html_content):
        # Mock the DBLP API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "hits": {
                    "hit": [
                        {
                            "score": "1.0",
                            "info": {
                                "author": "Test Author",
                                "url": "https://dblp.org/test-author-url"
                            }
                        }
                    ]
                }
            }
        }
        mock_get.return_value = mock_response

        # Mock the HTML content fetch
        mock_get_html_content.return_value = """
        <html>
            <div class="title">First Article</div>
            <div class="title">Second Article</div>
        </html>
        """

        author_name = "Test Author"
        articles = get_dblp_articles(author_name)

        # Assert expected articles
        self.assertEqual(articles, ["first article", "second article"])

        # Ensure the API call and HTML fetching were done
        mock_get.assert_called_once_with(
            data_collection.dblp.API_URL, headers=data_collection.dblp.HEADERS, params={'q': author_name, 'format': 'json'}
        )
        mock_get_html_content.assert_called_once_with("https://dblp.org/test-author-url")

    @patch('data_collection.dblp.requests.get')
    def test_get_dblp_articles_no_results(self, mock_get):
        # Mock an empty DBLP API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": {"hits": {"hit": []}}}
        mock_get.return_value = mock_response

        author_name = "Unknown Author"
        articles = get_dblp_articles(author_name)

        self.assertEqual(articles, [])
        mock_get.assert_called_once()

    @patch('data_collection.dblp.requests.get')
    def test_get_dblp_articles_request_exception(self, mock_get):
        # Simulate a request exception
        mock_get.side_effect = requests.RequestException("Error fetching data")

        author_name = "Test Author"
        articles = get_dblp_articles(author_name)

        self.assertEqual(articles, [])
        mock_get.assert_called_once()

if __name__ == '__main__':
    unittest.main()
