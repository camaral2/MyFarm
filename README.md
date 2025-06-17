# MyFarm

https://www.classcentral.com/classroom/freecodecamp-python-api-development-comprehensive-course-for-beginners-104903
https://github.com/Sanjeev-Thiyagarajan/fastapi-course

## Notes
### Generate file requirements.txt
```
pip freeze > requirements.txt
pip install -r requirements.txt
```

### Install fastapi
```
pip install "fastapi[all]"
pip install sqlalchemy
```

### Start my app
```
uvicorn app.main:app --reload
```

### Config Path of PostgreSQL
```
export PATH=/Library/PostgreSQL/17/bin:$PATH
```

## Commnad of Git
```
git config --global user.email "you@email.com"
git config --global user.name "Your name""

git add bees.txt
git commit -m "Added bees.txt"
git branch -M main
git remote add origin http:\\....git

git push -u origin main
```

## Alembic of update database
```
pip install alembic
alembic init alembic
[edit file with config database]

alembic revision -m "add start tables"
alembic current
alembic upgrade head
alembic downgrade -1
alembic revision --autogenerate -m "Added Phone Number in User"
```

## Test in Python
```
pip install pytest

```

## Coverage Test
```
pip install pytest-cov
pytest --cov=<your_package_or_module>
pytest --cov=.
pytest --cov=<your_package_or_module> --cov-report=html
pytest --cov=<your_package_or_module> --cov-fail-under=90


```