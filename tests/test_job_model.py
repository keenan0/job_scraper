# tests/test_job_model.py
import datetime
from src.Models.job_model import Job

def test_job_lt_descending_order():
    now = datetime.datetime.now()
    job_low  = Job("Dev", "CompA", data=10, link="url1", fetch_date=now)
    job_high = Job("Dev", "CompA", data=20, link="url2", fetch_date=now)

    assert job_high < job_low

    jobs = [job_low, job_high]
    assert sorted(jobs) == [job_high, job_low]

def test_job_str_representation():
    now = datetime.datetime.now()
    job = Job("Title", "Company", data=5, link="url", fetch_date=now)
    expected = f"{job.saved} {job.title} {job.company}  {job.link}"
    assert str(job) == expected

# Verifica ca Job.__lt__ sorteaza descrescator dupa data si ca sorted() respecta asta
# Verifica ca Job.__str__ produce formatul "{saved} {title} {company}  {link}"
