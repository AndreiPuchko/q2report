coverage erase
coverage run -m pytest tests
coverage html
del .coverage
explorer .\htmlcov\index.html