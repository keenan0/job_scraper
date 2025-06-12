# tests/test_blacklist_service.py
import json
from src.Services.BlacklistServices import BlacklistService

class DummyJob:
    def __init__(self, link):
        self.link = link

def test_add_and_is_blacklisted(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    svc = BlacklistService()
    job = DummyJob("http://example.com/job1")

    assert not svc.is_blacklisted(job)
    svc.add_to_blacklist(job)
    assert svc.is_blacklisted(job)

    data = json.loads((tmp_path / "blacklist.json").read_text())
    assert data == ["http://example.com/job1"]

# Verifica ca BlacklistService.is_blacklisted returneaza False cand fisierul nu exista
# Verifica ca add_to_blacklist adauga link-ul in blacklist.json si is_blacklisted intoarce True
