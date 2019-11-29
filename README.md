# BlocklyFlask Backend

The backend for a scratch clone that generates Python (flask) code for backend APIs.
This (plus the [frontend](https://github.com/HamishWHC/blocklyflask-frontend/)) is my major project for Software Design
and Development, one of my HSC (Year 12) courses.

## Contributing
Feel free to submit issues/bugs/minor feature requests. I might not accept pull/merge requests as this is an assessment
task.

## Set-up and Installation
You will need to install Python 3.7, PostgreSQL (anything >10 should be fine, I'm not using any particularly crazy
features, and you could probably get away with a SQLite 3 file or another DB by simply using the appropriate URI in
private.ini, but no guarantees on Flask-Migrate and Alembic working) and then all the Python packages in
requirements.txt (in venv directory: `python -m pip install -f requirements.txt`).

Set-up the DB using `flask db upgrade` and then run the dev server using `flask run`.