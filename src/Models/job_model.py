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

    def to_dict(self):
        return {
            "title": self.title,
            "company": self.company,
            "data": self.data.isoformat() if self.data else None,
            "link": self.link,
            "description": self.description,
            "saved": self.saved,
            "applied": self.applied,
            "fetch_date": self.fetch_date.isoformat() if self.fetch_date else None
        }