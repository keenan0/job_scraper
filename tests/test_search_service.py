# tests/test_search_service.py
import pytest
from src.Services.SearchServices import SearchService
from src.Models.ejobs_search    import EjobsSearch
from src.Models.hipo_search     import HipoSearch
from src.Models.linkedin_search import LinkedInSearch

@pytest.mark.parametrize("link,cls", [
    ("https://www.linkedin.com/jobs", LinkedInSearch),
    ("https://www.ejobs.ro",       EjobsSearch),
    ("https://www.hipo.ro",        HipoSearch),
])
def test_search_factory_valid_platforms(link, cls):
    svc  = SearchService()
    inst = svc.search_factory("TestSearch", link, frequency=5)
    assert isinstance(inst, cls)
    assert inst.link == link
    assert inst.frequency == 5

def test_search_factory_unsupported_link():
    svc = SearchService()
    with pytest.raises(Exception):
        svc.search_factory("TestSearch", "https://foo.bar", frequency=5)

# Verifica ca search_factory returneaza clasa corecta pentru linkedin, ejobs si hipo
# Verifica ca pentru link neacceptat se ridica exceptie

