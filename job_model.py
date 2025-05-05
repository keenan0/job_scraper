class Job:
    def __init__(self, title, company, location, link, description):
        self.title = title
        self.company = company
        self.location = location
        self.link = link
        self.description = description

    def to_dict(self):
        return {
            "Title": self.title,
            "Company": self.company,
            "Location": self.location,
            "Link": self.link
        }
