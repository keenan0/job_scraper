import datetime

from bs4 import BeautifulSoup
from src.Models.Search import *

class LinkedInSearch(Search):
    def job_search(self):

        base_url = self.link
        # page = 1

        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'lxml')
        jobs = soup.find('ul', class_='jobs-search__results-list').find_all('li')

        valid_jobs_found = False

        for job in jobs:
            link_tag = job.find('a', class_='base-card__full-link', recursive=True)
            link = link_tag['href']
            if link in self.links:
                continue
            title = job.find('h3', class_='base-search-card__title', recursive=True)
            company = job.find('a', class_='hidden-nested-link', recursive=True)
            date = job.find('time', class_='job-search-card__listdate--new', recursive=True)

            fetch_date = datetime.datetime.now()
            if not title or not company or not date or not link_tag or 'href' not in link_tag.attrs:
                continue

            valid_jobs_found = True
            link = link_tag['href']
            new_job = Job(title.text.strip(), company.text.strip(), date.text.strip(), link, fetch_date)
            self.links.append(link)
            self.jobs.add(new_job)

        if not valid_jobs_found:
            print("Nu mai sunt joburi.")

            # page += 1
            # time.sleep(1)