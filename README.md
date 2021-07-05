# Projet

Développez une application Web en utilisant Django

## Installation

clone repository locally

```bash
git clone https://github.com/nasr-edine/P9_drai_nasr-edine.git
```

Move to the P9_drai_nasr-edine root folder with:

```bash
cd P9_drai_nasr-edine
```

Create a virtual environment in root folder of project

```bash
python3 -m venv env
```

Activate virtual environment

```bash
source ./env/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Move to litrreview folder with:

```bash
cd litrreview
```

Migrate

```bash
django m
```

You can create a super user in command line:

```bash
django csu
```

## Usage

Run the Django Server:

```bash
django r
```

Go to your browser to view django website with locahost URL
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

You can create a user with the URL below or click on signup button
[http://127.0.0.1:8000/users/signup/](http://127.0.0.1:8000/users/signup/)

After signup, you can login with your credentials (username and password)
[http://127.0.0.1:8000/users/login/](http://127.0.0.1:8000/users/login/)

You can make a new ticket with URL below or in click on "Demander une critique" button:
[http://127.0.0.1:8000/tickets/new/](http://127.0.0.1:8000/tickets/new/)

You can also make a new ticket and review in the same time with URL below or in click on "Creer une critique":
[http://127.0.0.1:8000/tickets/newticketreview/](http://127.0.0.1:8000/tickets/newticketreview/)

And finally, you can view your followers and following with URL below or click on 'abonnements' button:
[http://127.0.0.1:8000/users/follow](http://127.0.0.1:8000/users/follow)

### Folder Structure

    .
    ├── litrreview/                  # django project folder
    ├── setup.cfg                    # Content the customise rules for flake8
    ├── requirements.txt             # for install all dependencies necessary for this project
    └── README.md
