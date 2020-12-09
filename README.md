# Simple dataset upload and booking
This project, allows users to upload a datasets in a .zip file, after then user can book the datasets and download the booked dataset from the system, no direct download allowed or download datasets without booking at the first place. 

## Stacks 
- flask
- bcrypt
- gunicorn
- sqlalchemy
- sqlite

## to run this project or to deploy with docker
### clone to your local directory
```
git clone https://github.com/yudanta/simple-dataset-booking.git
```
### local via venv 
```
# create virtual env 
python3 -m venv simple-dataset-booking

cd simple-dataset-booking

# activate venv 
source bin/activate 

# install dependency 
pip install -r requirements.txt

# performing migration and data seeders
## init db migration 
python dbmigration.py SqlDB init
python dbmigration.py SqlDB migrate
python dbmigration.py SqlDB upgrade

##Seed user data
python dbmigration.py do_seed_user

# run directly using python3 
python3 run.py

# run from gunicorn 
gunicorn app:app 
```

### via docker-compose
```
docker-compose up --build
```

The app will be available at http://localhost:8000


## sample user (from db data seeder)
```
# username:password
watson:098321
adler:098321
haruki:098321
brown:098321
```

##
Online demo via heroku can be accessed at http://tumbu.herokuapp.com