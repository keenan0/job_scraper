from src.Models.job_model import *
from Testing.template_jobs import template_jobs
from bs4 import BeautifulSoup
import requests
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


    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name} {self.link}"

    def activate_deactivate(self):
        if self.active:
            self.active = False
        else:
            self.active = True
        return self.active
    
    def get_jobs(self):
        return self.jobs

    def job_search(self):
        pass

    def period_searching(self):
        self.job_search()
        time.sleep(self.frequency * 60)
        while self.active:
            self.job_search()
            time.sleep(self.frequency * 60)
