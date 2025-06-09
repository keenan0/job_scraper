from bs4 import BeautifulSoup
import requests

base_url = "https://www.hipo.ro/locuri-de-munca/cautajob/Toate-Domeniile/Toate-Orasele/internship-abc/"
page = 1

while True:
    url = f"{base_url}/{page}"
    print(f"\nPagina {page}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    jobs = soup.find_all('div', class_='job-item p-3 mb-4')
    print(jobs[1])
    jobs = jobs[1:]