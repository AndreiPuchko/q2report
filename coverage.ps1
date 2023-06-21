coverage erase
coverage run -m pytest tests
coverage html
explorer .\htmlcov\index.html