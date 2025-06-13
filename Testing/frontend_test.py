import unittest
import tkinter as tk
import time
from unittest.mock import MagicMock
from src.GUI.SearchView import SearchView
from src.Services.SearchServices import SearchService
from src.Services.FavoritesServices import FavoritesService
from src.Services.BlacklistServices import BlacklistService

class TestSearchView(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        
        self.mock_search_service = SearchService()
        self.mock_search_service.searches = []
        self.mock_search_service.add_search = MagicMock(side_effect=self.fake_add_search)
        
        self.favorites_service = FavoritesService()
        self.blacklist_service = BlacklistService()
        
        self.add_link_button = MagicMock()
        
        self.search_view = SearchView(
            self.root, self.root, {"FONT_FAMILY": "Arial", "FONT_SIZE": 12},
            self.mock_search_service, self.favorites_service, self.blacklist_service, self.add_link_button
        )

    def fake_add_search(self, title, link, frequency):
        mock_search = MagicMock()
        mock_search.title = title
        mock_search.link = link
        mock_search.frequency = frequency
        mock_search.active = True
        mock_search.jobs = ["Mock Job 1", "Mock Job 2"] 
        self.mock_search_service.searches.append(mock_search)
        return mock_search

    def test_add_hipo_search(self):
        self.search_view.search_service_title.set("Test SWE Search")
        self.search_view.search_service_link.set("https://www.hipo.ro/locuri-de-munca/cautajob/Toate-Domeniile/Toate-Orasele/swe")
        self.search_view.search_platform.set("Hipo")
        self.search_view.search_freq.set("30 Minutes")

        self.search_view.callback_add_new_search()

        start = time.time()
        while time.time() - start < 2:
            if len(self.mock_search_service.searches) == 1:
                break
            time.sleep(0.05)

        self.assertEqual(len(self.mock_search_service.searches), 1)
        added_search = self.mock_search_service.searches[0]

        self.assertEqual(added_search.title, "Test SWE Search")
        self.assertEqual(added_search.link, "https://www.hipo.ro/locuri-de-munca/cautajob/Toate-Domeniile/Toate-Orasele/swe")
        self.assertEqual(added_search.frequency, 30)

        self.assertTrue(hasattr(added_search, "jobs"))
        self.assertGreater(len(added_search.jobs), 0)

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
