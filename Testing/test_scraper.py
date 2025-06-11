import time

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
url = "https://www.ejobs.ro/locuri-de-munca/intern/sort-publish/pagina3"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)
driver.get(url)
time.sleep(0.5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
soup = BeautifulSoup(driver.page_source, 'lxml')
jobs = soup.find_all('div', class_='job-card-content')

valid_jobs_found = False

for job in jobs:
    valid_jobs_found = True

    title = job.find('h2', class_='job-card-content-middle__title').find('span', recursive=True).text.strip()

    link_href = job.find('h2', class_='job-card-content-middle__title').find('a')['href']
    link = "ejobs.ro" + link_href

    company = job.find('h3', class_='job-card-content-middle__info').find('a').text.strip()

    str_date = job.find('div', class_='job-card-content-top__date').text.strip()

    print(f"Title: {title}, Company: {company}, Link: {link}, Date: {str_date}")