class Job:
    def __init__(self, title, company, data, link, description = None):
        self.title = title
        self.company = company
        self.data = data
        self.link = link
        self.description = description
        self.saved = False

    def __str__(self):
        return f"{self.saved} {self.title} {self.company} {self.location} {self.link}"
