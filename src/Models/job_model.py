from datetime import datetime

class Job:
    def __init__(
        self,
        title: str,
        company: str,
        data: datetime,
        link: str,
        fetch_date: datetime,
        description: str | None = None,
        saved: bool = False,
        applied: bool = False,
    ):
        self.title = title
        self.company = company
        self.data = data
        self.link = link
        self.description = description
        self.saved = saved
        self.applied = applied
        self.fetch_date = fetch_date

    def __str__(self) -> str:
        return f"{self.saved} {self.title} {self.company}  {self.link}"

    def __lt__(self, other: "Job") -> bool:
        return self.data > other.data

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "company": self.company,
            "data": self.data.isoformat() if self.data else None,
            "link": self.link,
            "description": self.description,
            "saved": self.saved,
            "applied": self.applied,
            "fetch_date": self.fetch_date.isoformat() if self.fetch_date else None,
        }