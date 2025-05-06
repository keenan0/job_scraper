from Search import *

class HipoSearch(Search):
    def job_search(self):
        base_url = self.link
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
                link = 'https://www.hipo.ro' + link_tag['href']

                job_new = Job(title.text.strip(), company.text.strip(), date.text.strip(), link)
                if link not in self.jobs.keys():
                    self.jobs[link] = job_new

            if not valid_jobs_found:
                break

            page += 1
            time.sleep(3)

if __name__ == "__main__":
    search = HipoSearch(
        "https://www.hipo.ro/locuri-de-munca/cautajob/IT-Software/Toate-Orasele",
        60,
        "Hipo",
        "HipoSearch"
    )
    search.job_search()