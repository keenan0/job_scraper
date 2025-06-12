import json
import os

BLACKLIST_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Data/blacklist.json"))

class BlacklistService:
    def __init__(self):
        self.blacklisted_links = set()
        self.load_blacklist()

    def add_to_blacklist(self, job):
        self.blacklisted_links.add(job.link)
        self.save_blacklist()

    def is_blacklisted(self, job):
        return job.link in self.blacklisted_links

    def save_blacklist(self):
        with open(BLACKLIST_FILE, 'w') as f:
            json.dump(list(self.blacklisted_links), f, indent=4)

    def load_blacklist(self):
        os.makedirs(os.path.dirname(BLACKLIST_FILE), exist_ok=True)

        if not os.path.exists(BLACKLIST_FILE):
            with open(BLACKLIST_FILE, 'w') as f:
                json.dump([], f)

        if os.path.getsize(BLACKLIST_FILE) > 0:
            with open(BLACKLIST_FILE, 'r') as f:
                self.blacklisted_links = set(json.load(f))
        else:
            self.blacklisted_links = set()