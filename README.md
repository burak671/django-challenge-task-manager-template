# Django Challenge: Task Manager Backend

This repository is a beginner-friendly Django backend exercise focused on CRUD and SQLite.

It is intentionally a starter template:

- task examples are hard-coded in `tasks/views.py`
- create/edit/delete handlers contain TODOs
- students must replace hard-coded logic with database-backed CRUD

## Quick start (no Make required)

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

## Run tests

```bash
python manage.py test
```

The tests describe expected CRUD behavior. In this starter template, several tests will fail until students implement the backend.

## Optional Make commands

If `make` is available, you can use the shortcuts below:

```bash
make install
make migrate
make run
make test
```

## Windows note

Use this activation command in PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## What is included in the template

- `Task` model backed by SQLite
- Starter views with hard-coded examples and TODO markers
- URL wiring for CRUD routes
- Admin registration for `Task`
- Django tests for list/create/edit/delete behavior

## Branches

- `solution`: complete working implementation
- `template`: starter version for students
