# MyFarm


## Notes
### Generate file requirements.txt
```
pip freeze > requirements.txt
```

### Install fastapi
```
pip install "fastapi[all]"
pip install sqlalchemy
```

### Start my app
```
uvicorn main:app --reload
```

### Config Path of PostgreSQL
```
export PATH=/Library/PostgreSQL/17/bin:$PATH
```
