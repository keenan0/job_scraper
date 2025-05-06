from Models import *

class SearchService:
    def __init__(self):
        self.searches = []

    def add_search(self, title, link, platform, frequency):
        # Create a new search object and add it to the list
        new_search = Search(link, frequency, platform, title)
        self.searches.append(new_search)