from django.test import TestCase
from unittest.mock import patch, MagicMock
from data_collection.gate import names_match, get_gate_profile_url, get_gate_articles_interests

class TestGateFunctions(TestCase):

    def test_names_match(self):
        first_names = ["john"]
        last_names = ["doe"]
        profile_names = ["john", "doe"]
        self.assertTrue(names_match(first_names, last_names, profile_names))

        profile_names = ["jane", "doe"]
        self.assertFalse(names_match(first_names, last_names, profile_names))

        profile_names = ["john", "smith"]
        self.assertFalse(names_match(first_names, ["doe"], profile_names))

        profile_names = ["doe", "john"]
        self.assertTrue(names_match(first_names, last_names, profile_names))

    @patch('data_collection.gate.sync_playwright')
    def test_get_gate_profile_url(self, mock_playwright):
        mock_browser = MagicMock()
        mock_page = MagicMock()
        mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page
        mock_page.goto.return_value = None
        mock_page.content.return_value = '<html><div class="nova-legacy-v-entity-item__title"><a href="profile/1">John Doe</a></div></html>'

        result = get_gate_profile_url("John", "Doe")
        expected_url = "https://www.researchgate.net/profile/1"
        self.assertEqual(result, expected_url)

    @patch('data_collection.gate.sync_playwright')
    def test_get_gate_articles_interests(self, mock_playwright):
        mock_browser = MagicMock()
        mock_page = MagicMock()
        mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page
        mock_page.goto.return_value = None
        mock_page.content.return_value = '''
            <html>
                <div class="js-target-skills">
                    <div class="nova-legacy-l-flex__item">AI</div>
                    <div class="nova-legacy-l-flex__item">ML</div>
                </div>
                <div class="nova-legacy-v-publication-item__title">Publication One</div>
                <div class="nova-legacy-v-publication-item__title">Publication Two</div>
            </html>
        '''

        interests, articles = get_gate_articles_interests("https://www.researchgate.net/profile/1")
        self.assertEqual(interests, ["AI", "ML"])
        self.assertEqual(articles, ["publication one", "publication two"])
