class Job:
    def __init__(self, title, company, location, link, description):
        self.title = title
        self.company = company
        self.location = location
        self.link = link
        self.description = description
        self.saved = False

    def to_dict(self):
        return {
            "Title": self.title,
            "Company": self.company,
            "Location": self.location,
            "Link": self.link,
            "Saved": self.saved
        }

    def __str__(self):
        return f"{self.saved} {self.title} {self.company} {self.location} {self.link}"
