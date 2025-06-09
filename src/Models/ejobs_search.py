from src.Models.Search import *
import dateparser

class EjobsSearch(Search):
    def job_search(self):

        base_url = self.link
        page = 1

        while True:

            url = f"{base_url}/pagina{page}"
            print(f"\nPagina {page}")
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            jobs = soup.find_all('div', class_='job-card-content')

            valid_jobs_found = False

            for job in jobs:
                valid_jobs_found = True

                title = job.find('h2', class_='job-card-content-middle__title').find('span', recursive=True).text.strip()

                link_href = job.find('h2', class_='job-card-content-middle__title').find('a')['href']
                link = "ejobs.ro" + link_href

                if link in self.links:
                    continue

                company = job.find('h3', class_='job-card-content-middle__info').find('a').text.strip()

                str_date = job.find('div', class_='job-card-content-top__date').text.strip()
                date = dateparser.parse(str_date, languages=['ro'])

                fetch_date = datetime.datetime.now()

                new_job = Job(title, company, date, link, fetch_date)

                self.links.add(link)
                self.jobs.add(new_job)

            if not valid_jobs_found:
                print("Nu mai sunt joburi.")
                break

            page += 1
            time.sleep(0.1)