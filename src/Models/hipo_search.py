from src.Models.Search import *

class HipoSearch(Search):    
    def job_search(self):

        base_url = self.link

        page = 1
        total_pages = None

        while total_pages is None or page <= total_pages:


            url = f"{base_url}/{page}"
            print(f"\nPagina {page}")
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')

            if total_pages is None:
                str_nr_pages = soup.find('div', class_='job-item').text.strip()
                total_pages = int(str_nr_pages.split(' ')[0]) / 40

            jobs = soup.find_all('div', class_='text-start')
            valid_jobs_found = False

            for job in jobs:
                valid_jobs_found = True

                title = job.find('a', class_='job-title').find('h5').text.strip()

                link_href = job.find('a', class_='job-title')['href']
                link = 'https://www.hipo.ro' + link_href

                if link in self.links:
                    continue

                company = job.find('p', class_='company-name').text.strip()

                info = job.find_all('div', class_='d-flex mb-1')
                if len(info) == 2:
                    str_date = info[0]
                    str_date = info[0]
                else:
                    str_date = info[1]

                str_date = str_date.text.strip()

                date = datetime.datetime.strptime(str_date, '%d-%m-%Y')

                fetch_date = datetime.datetime.now()


                new_job = Job(title, company, date, link, fetch_date)

                self.links.add(link)
                self.jobs.add(new_job)

            if not valid_jobs_found:
                break

            page += 1
            time.sleep(0.1)