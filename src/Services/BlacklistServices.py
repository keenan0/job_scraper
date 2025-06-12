import json
import os

BLACKLIST_FILE = "blacklist.json"

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
        if os.path.exists(BLACKLIST_FILE):
            with open(BLACKLIST_FILE, 'r') as f:
                self.blacklisted_links = set(json.load(f))