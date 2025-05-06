class Job:
    def __init__(self, title, company, location, link, description):
        self.title = title
        self.company = company
        self.location = location
        self.link = link
        self.description = description
        self.saved = False

    def __str__(self):
        return f"{self.saved} {self.title} {self.company} {self.location} {self.link}"
