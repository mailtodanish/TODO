> **Note**: Upgrading project from DJANGO 3 to DJANGO 4
# TODO

Based on Django , **secure** and **shareable**.  Create daily activities , schedule activities and add notes to do revision in future.

1.  Add your notes to keep them for future use and you can revise them.

2.  Add activities , Schedule activities

## Running Project locally

### Create pipenv and install all dependencies.

```bash
pip install pipenv

$ pipenv install

$ pipenv shell
```

### Clone repository to your local machine

*   [ ] `git clonehttps://github.com/mailtodanish/TODO.git`

<!---->

*   [ ] `Install requirements.txt`

<!---->

*   [ ] `Apply migrations`

### Don't forget to load applictaion data

    python manage.py migrate
    python manage.py createsuperuser
    python manage.py loaddata ApplictaionData.json 

**Update your secrets Key in seting.py**

**python manage.py runserver**

### Screen Shot

![Image](img/screen_shot1.png)
![Image](img/screen_shot2.png)

