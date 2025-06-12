# tests/test_favorites_service.py
import json
import pytest
from src.Services.FavoritesServices import FavoritesService
from src.Models.job_model import Job

def test_add_and_remove_favorite(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    svc = FavoritesService()
    job = Job("Dev", "Comp", data=0, link="u1", fetch_date=None)

    assert svc.add_favorite_job(job) is True
    assert job in svc.get_all_favorites()
    assert svc.add_favorite_job(job) is False

    assert svc.remove_favorite_job(job) is True
    assert job not in svc.get_all_favorites()
    assert svc.remove_favorite_job(job) is False

    data = json.loads((tmp_path / "favorites.json").read_text())
    assert data == []

# Verifica ca add_favorite_job returneaza True la prima adaugare si False la duplicat
# Verifica ca remove_favorite_job returneaza True la stergerea existenta si False la inexistent