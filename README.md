# key value

A key-value storage API!


## Getting Started
1. Clone this repository to your local machine:
```
git clone https://github.com/shahriar-fattahi/phone-catalog.git
```
2- SetUp a Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
```
or(for Windows)
```
python -m venv venv
venv/scripts/activate
```
3- install Dependencies
```
pip install -r requirements/local.txt
```
4- run Docker Compose
```
docker compose -f docker-compose.local.yml up -d     
```

5- make migrations
```
python manage.py makemigrations
```
6- migrate
```
python manage.py migrate
```

7- create an admin
```
python manage.py createsuperuser
```

8- run the project
```
python manage.py runserver
```

## Create a key-value
Format for Sending Data to Set Key API:
```
{
    "data":{
        "key": "keyname",
        "value": value
    }
}
```
