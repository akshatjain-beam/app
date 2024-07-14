## How to setup your project

1. `python3.11 -m venv venv && source venv/bin/activate`
2. `pip install --upgrade pip`
3. (optional):
   - `pip install pip-tools`
   - `pip-compile --resolver=backtracking requirements.in`
4. `pip install -r requirements.txt`

## Run the Repository
```bash
fastapi dev main.py
```

## Folder structure
```md
.
├── README.md
├── __init__.py
├── __pycache__
│   ├── __init__.cpython-311.pyc
│   └── main.cpython-311.pyc
├── main.py
├── models
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   ├── database.cpython-311.pyc
│   │   └── item.cpython-311.pyc
│   ├── database.py
│   └── item.py
├── products.db
├── requirements.in
├── requirements.txt
├── routers
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   ├── items.cpython-311.pyc
│   │   └── users.cpython-311.pyc
│   └── items.py
├── schemas
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   └── item.cpython-311.pyc
│   └── item.py
└── utils
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-311.pyc
    │   ├── logger.cpython-311.pyc
    │   ├── requester.cpython-311.pyc
    │   └── scraper.cpython-311.pyc
    ├── logger.py
    ├── requester.py
    └── scraper.py
```
