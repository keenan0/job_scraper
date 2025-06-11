class Job:
    def __init__(self, title, company, data, link, fetch_date, description = None):
        self.title = title
        self.company = company
        self.data = data
        self.link = link
        self.description = description
        self.saved = False
        self.applied = False
        self.fetch_date = fetch_date

    def __str__(self):
        return f"{self.saved} {self.title} {self.company}  {self.link}"

    def __lt__(self, other):
        return self.data > other.data
