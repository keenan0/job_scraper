# Job Scraper
Un instrument inteligent cu interfață grafică pentru căutarea, filtrarea și salvarea joburilor de pe platforme populare precum eJobs, Hipo și LinkedIn.

## Descriere

`Job Scraper` este o aplicație desktop dezvoltată în Python, care permite utilizatorilor să caute oferte de muncă de pe mai multe site-uri, să salveze anunțuri favorite și să ignore anunțuri irelevante printr-o listă neagră.

Interfața grafică facilitează o experiență ușoară și intuitivă, oferind suport pentru:
- căutări personalizate
- salvarea anunțurilor interesante în favorite
- evitarea afișării anunțurilor nedorite
- exportul și managementul datelor locale

## Funcționalități

- Căutare automată după cuvinte-cheie pe:
  - [x] eJobs.ro
  - [x] Hipo.ro
  - [x] LinkedIn Jobs
- Marcarea anunțurilor favorite
- Blacklist pentru anunțuri sau angajatori ignorați
- Salvarea rezultatelor local (format JSON)
- Interfață grafică (Tkinter)
- Teste pentru componentele de scraping

## Stack Tehnologic

- Python 3.10+
- Tkinter – pentru interfața grafică
- requests, BeautifulSoup – pentru web scraping
- json – pentru salvarea locală a datelor
- unittest – pentru testare automată

## Structura Proiectului

```
job_scraper/
│
├── src/
│   ├── GUI/           # Interfața grafică
│   ├── Models/        # Logica de scraping și structuri de date
│   └── Services/      # Filtrare, salvare, blacklist etc.
│
├── Data/              # Fișiere locale (favorites, searches etc.)
├── Testing/           # Teste pentru componente
├── UMLDiagram/        # Diagrama de arhitectură
├── main.py            # Punctul de intrare în aplicație
└── README.md
```

## 1. User Stories și Backlog Creation

1. Ca utilizator, vreau să pot exporta anunțurile de joburi în format CSV sau JSON, pentru a le putea partaja sau analiza offline.  
2. Ca sistem, am nevoie să salvez anumite fișiere pe PC pentru a păstra un istoric.  
3. Ca sistem, trebuie să încarc și să afișez rezultatele căutării în bucăți (chunk-uri), astfel încât performanța interfeței să rămână acceptabilă chiar și la sute de rezultate.  
4. Ca sistem, trebuie să verific că linkul oferit este valid (și conduce către o căutare de joburi).  
5. Ca utilizator, vreau să pot adăuga în blacklist anumite companii sau anunțuri, astfel încât să nu mai văd joburi irelevante sau nedorite.  
6. Ca sistem, vreau să validez datele introduse, pentru a returna rezultate corecte și relevante.  
7. Ca sistem, vreau să extrag titlul jobului, numele companiei, data și linkul anunțului, pentru a structura datele.  
8. Ca utilizator, vreau să pot furniza o listă de linkuri către joburi, pe care aplicația să le monitorizeze pentru a primi anunțuri relevante.  
9. Ca sistem, vreau să detectez și să evit anunțurile duplicate, pentru a nu stoca date redundante.  
10. Ca sistem, vreau să stochez datele despre joburi într-un format structurat, pentru a putea fi ușor procesate și analizate.  
11. Ca utilizator, vreau să pot vizualiza anunțurile de joburi într-un dashboard bine organizat, pentru a le analiza ușor.  
12. Ca utilizator, vreau să pot marca anunțurile ca „salvate” sau „aplicate”, pentru a-mi urmări progresul în căutarea unui job.  
13. Ca utilizator, vreau să pot adăuga un link nou ce urmează să fie procesat printr-un formular intuitiv.  
14. Ca sistem, vreau să detectez automat modificările în anunțurile de joburi, astfel încât utilizatorii să aibă informații actualizate.

## 2. Diagrame

(UMLDiagram/second_diagram.png)
(UMLDiagram/diagram_updated.png)



## 3. Source Control cu Git

Se face un pull local din ramura `main`, apoi se creează un branch nou pentru dezvoltare. După finalizarea lucrului pe acel branch, modificările se fac merge local în `main`, iar în final se face push către remote.

## 4. Teste Automate

Testele sunt organizate în directorul `Testing/`, unde sunt acoperite următoarele componente:

- Scraper logic – validarea extragerii corecte a datelor de pe eJobs, Hipo și LinkedIn  
- Blacklist și Favorites – verificarea funcționării corecte a mecanismelor de filtrare și salvare locală  
- Interfață grafică – teste funcționale asupra componentelor de bază ale UI-ului

## 5. Raportare bug si rezolvare cu pull request


## 6. Coding Standards

Fișierul [`SearchView.py`](src/GUI/SearchView.py) respectă o serie de principii și bune practici de programare care asigură lizibilitate, întreținere facilă și scalabilitate:

- **Tipare de proiectare (OOP):** Clasa `SearchView` extinde `BaseView` și aplică principiile responsabilității unice și separării logicii de UI față de servicii externe.
- **Anotări de tip (type hints):** Sunt utilizate extensiv pentru a clarifica așteptările de input/output, contribuind la detecția timpurie a erorilor și la o mai bună colaborare între dezvoltatori.
- **Naming clar și consecvent:** Variabilele, metodele și componentele UI au denumiri semnificative, în limba engleză, care reflectă rolul lor în aplicație.
- **Separarea logicii UI de servicii externe:** Codul utilizează instanțe separate (`SearchService`, `FavoritesService`, `BlacklistService`) pentru a gestiona datele și acțiunile, în conformitate cu arhitectura MVC.

## 7. Design Patterns

### Strategy Pattern – pentru diversificarea surselor de căutare

Fișierele din `src/Models/` (`ejobs_search.py`, `hipo_search.py`, `linkedin_search.py`) implementează metode similare pentru căutare, fiecare adaptată structurii HTML specifice platformei.

- Fiecare clasă reprezintă o strategie concretă de scraping.  
- Clasa `Search` acționează ca context, delegând sarcina către strategiile specializate.

### Factory Pattern 

Clasa `Search` decide dinamic ce instanțe de scraping rulează, comportându-se similar cu un Factory ce generează obiecte din aceeași familie de interfețe.

### MVC (Model-View-Controller) adaptat

- `GUI/` – interfață vizuală și controlere  
- `Models/` – logica de extragere date  
- `Services/` – logică auxiliară și prelucrare  

## 8. Prompt Engineering – Documentarea folosirii toolurilor de AI

### ChatGPT (GPT-4)

- Sugestii pentru arhitectura modulară (GUI, Models, Services)  
- Scrierea inițială a scraperelor cu BeautifulSoup  
- Asistență în debugging și crearea testelor  

### Claude (3.5 / 3.7)

- Refactor pentru codul de scraping (ex: `hipo_search.py`)  
- Optimizarea logicii de blacklist și evitarea duplicatelor  
- Claritate în designul responsabilităților  

### Gemini (Google)

- Salvare/încărcare fișiere JSON cu fallback pentru corupere  

Link live video:
https://www.youtube.com/watch?v=yktghzSj2R0