from src.Models.Search import Search

from src.Models.ejobs_search import EjobsSearch
from src.Models.hipo_search import HipoSearch
from src.Models.linkedin_search import LinkedInSearch

class SearchService:
    def __init__(self):
        self.searches = []
        self.load_searches()

    def search_factory(self, title, link, platform, frequency):
        platform = platform.lower()
        
        if platform == "linkedin":
            return LinkedInSearch(link, frequency, platform, title)
        elif platform == "ejobs":
            return EjobsSearch(link, frequency, platform, title)
        elif platform == "hipo":
            return HipoSearch(link, frequency, platform, title)
        else:
            return Search(link, frequency, platform, title)

    def add_search(self, title, link, platform, frequency):
        new_search = self.search_factory(title, link, platform, frequency)
        self.searches.append(new_search)
        
        return new_search