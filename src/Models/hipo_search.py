from src.Models.Search import *


class HipoSearch(Search):    
    def job_search(self):
        """
            After running job_search(), self.jobs will be a dicitonary of key: value pairs, where key=found_link, value=Job(data).
        """

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
                link_tag = title
                link = 'https://www.hipo.ro' + link_tag['href']
                if link in self.links:
                    continue
                company = job.find('p', class_='company-name')
                date = job.find('div', class_='d-flex mb-1')

                fetch_date = datetime.datetime.now()

                if not title or not company or not date or not link_tag or 'href' not in link_tag.attrs:
                    continue

                valid_jobs_found = True
                link = 'https://www.hipo.ro' + link_tag['href']

                job_new = Job(title.text.strip(), company.text.strip(), date.text.strip(), link)
                self.links.append(link)
                self.jobs.add(job_new)

            if not valid_jobs_found:
                break

            page += 1
            time.sleep(3)