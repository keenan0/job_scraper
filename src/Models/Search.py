from bs4 import BeautifulSoup
import requests
import time

class Search:
    def __init__(self, link, frequency, platform, name):
        self.link = link
        self.frequency = frequency
        self.platform = platform
        self.jobs = {}
        self.name = name
        self.active = True
        with open('Data/searches.json', 'a') as f:
            f.write(f"{self.name} {self.link} {self.frequency} {self.platform} {self.active}\n")

    def __str__(self):
        return f"{self.name} {self.link}"

    def __repr__(self):
        return f"{self.name} {self.link}"

    def activate_deactivate(self):
        if self.active:
            self.active = False
        else:
            self.active = True
        return self.active

    def job_search(self):
        pass

