import json
import threading

from src.Models.Search import Search
from src.Models.ejobs_search import EjobsSearch
from src.Models.hipo_search import HipoSearch
from src.Models.linkedin_search import LinkedInSearch
from src.Models.job_model import Job

class SearchService:
    def __init__(self):
        self.json_path = "Data/searches.json"
        self.searches = []
        self.load_search()

    def search_factory(self, title, link, frequency):
        if "linkedin" in link.lower():
            platform = "linkedin"
        elif "ejobs" in link.lower():
            platform = "ejobs"
        elif "hipo" in link.lower():
            platform = "hipo"
        else:
            raise Exception("Unsupported platform or link format")

        if platform == "linkedin":
            return LinkedInSearch(link, frequency, platform, title)
        elif platform == "ejobs":
            return EjobsSearch(link, frequency, platform, title)
        elif platform == "hipo":
            return HipoSearch(link, frequency, platform,title)
        else:
            return Search(link, frequency, platform, title)

    def add_search(self, title, link, frequency):
        try:
            new_search = self.search_factory(title, link, frequency)
        except Exception as e:
            raise e

        self.searches.append(new_search)
        self.save_searches()
        
        if new_search.active:
            threading.Thread(target=new_search.period_searching).start()

        return new_search

    def save_searches(self):
        """ Saves data about searches into searches.json"""

        data = []
        for s in self.searches:
            data.append({
                'name': s.name,
                'link': s.link,
                'platform': s.platform,
                'frequency': s.frequency,
                'active': s.active,
                'jobs': [job.to_dict() for job in s.get_jobs()],
                'links': list(s.links)
            })
        with open(self.json_path, 'w') as f:
            json.dump(data, f, indent=2)

    def load_search(self):
        try:
            with open(self.json_path, 'r') as f:
                try:
                    data = json.load(f)
                    return data
                except json.decoder.JSONDecodeError:
                    print(f"File {self.json_path} is empty or contains invalid JSON")
                    return None
        except FileNotFoundError:
            return
        
        for item in data:
            s = self.search_factory(
                item['name'],
                item['link'],
                item['platform'],
                item['frequency']
            )
            s.active = item.get('active', False)
            for job_dict in item.get('jobs', []):
                job = Job.from_dict(job_dict)
                s.get_jobs().add(job)
            s.links = set(item.get('links', []))
            self.searches.append(s)
            if s.active:
                threading.Thread(target=s.period_searching).start()