from src.Models.Search import *

class EjobsSearch(Search):
    def job_search(self):

        base_url = self.link
        page = 1
        jobs = []
        while True:
            url = f"{base_url}/pagina{page}"
            print(f"\nPagina {page}")
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            jobs = soup.find_all('div', class_='job-card-content')

            valid_jobs_found = False

            for job in jobs:
                title = job.find('h2', class_='job-card-content-middle__title').find('span', recursive=True)
                company = job.find('h3', class_='job-card-content-middle__info').find('a')
                date = job.find('div', class_='job-card-content-top__date')
                link_tag = job.find('h2', class_='job-card-content-middle__title').find('a')

                if not title or not company or not date or not link_tag or 'href' not in link_tag.attrs:
                    continue

                valid_jobs_found = True
                link = "ejobs.ro" + link_tag['href']
                new_job = Job(title.text.strip(), company.text.strip(), date.text.strip(), link)

            if not valid_jobs_found:
                print("Nu mai sunt joburi.")
                break

            page += 1
            time.sleep(1)