from bs4 import BeautifulSoup
import requests
import time

base_url = 'https://www.hipo.ro/locuri-de-munca/cautajob/IT-Software/Toate-Orasele'
page = 1

while True:
    url = f"{base_url}/{page}"
    print(f"\nPagina {page}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    jobs = soup.find_all('div', class_='job-item p-3 mb-4')

    valid_jobs_found = False

    for job in jobs:
        title = job.find('a', class_='job-title')
        company = job.find('p', class_='company-name')
        date = job.find('div', class_='d-flex mb-1')
        link_tag = title

        if not title or not company or not date or not link_tag or 'href' not in link_tag.attrs:
            continue

        valid_jobs_found = True
        link = link_tag['href']
        print(title.text.strip(), '|', company.text.strip(), '|', date.text.strip(), '|', 'https://www.hipo.ro' + link)

    if not valid_jobs_found:
        print("Nu mai sunt joburi.")
        break

    page += 1
    time.sleep(1)