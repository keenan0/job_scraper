from src.Models.job_model import *
from bs4 import BeautifulSoup
import requests
from threading import Thread
import time
from sortedcontainers import SortedSet
import datetime

class Search:
    def __init__(self, link, frequency, platform, name):
        self.link = link
        self.frequency = frequency
        self.platform = platform
        self.jobs = SortedSet()
        self.links = set()
        self.name = name
        self.active = True
        self.thread = Thread(target=self.period_searching)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name} {self.link}"

    def activate_deactivate(self):
        if self.active:
            self.active = False
        else:
            self.active = True
            if not self.thread.is_alive():
                self.thread.start()
        return self.active
    
    def get_jobs(self):
        return self.jobs

    def job_search(self):
        pass

    def period_searching(self):
        self.job_search()
        time.sleep(self.frequency * 60)
        print(len(self.jobs))
        while self.active:
            self.job_search()
            time.sleep(self.frequency * 60)
