import unittest
import tkinter as tk
from src.GUI.SearchView import SearchView
from src.Services.SearchServices import SearchService
from unittest.mock import MagicMock

class TestSearchView(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Nu afișa fereastra
        self.mock_search_service = SearchService()
        self.mock_search_service.searches = []
        self.mock_search_service.add_search = MagicMock(side_effect=self.fake_add_search)

        self.favorites_service = MagicMock()  # Poate fi un stub pentru test
        self.search_view = SearchView(self.root, self.root, {"FONT_FAMILY": "Arial", "FONT_SIZE": 12},
                                      self.mock_search_service, self.favorites_service)

    def fake_add_search(self, title, link, platform, frequency):
        # Creează un obiect mock Search cu metoda job_search
        mock_search = MagicMock()
        mock_search.title = title
        mock_search.link = link
        mock_search.platform = platform
        mock_search.frequency = frequency
        mock_search.active = True
        mock_search.job_search = MagicMock()
        self.mock_search_service.searches.append(mock_search)
        return mock_search

    def test_add_hipo_search(self):
        self.search_view.search_service_title.set("Test SWE Search")
        self.search_view.search_service_link.set("https://www.hipo.ro/locuri-de-munca/cautajob/Toate-Domeniile/Toate-Orasele/swe")
        self.search_view.search_platform.set("Hipo")
        self.search_view.search_freq.set("30 Minutes")

        self.search_view.callback_add_new_search()

        self.assertEqual(len(self.mock_search_service.searches), 1)
        added_search = self.mock_search_service.searches[0]
        self.assertEqual(added_search.title, "Test SWE Search")
        self.assertEqual(added_search.link, "https://www.hipo.ro/locuri-de-munca/cautajob/Toate-Domeniile/Toate-Orasele/swe")
        self.assertEqual(added_search.platform, "Hipo")
        self.assertEqual(added_search.frequency, 30)
        added_search.job_search.assert_called_once()

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()