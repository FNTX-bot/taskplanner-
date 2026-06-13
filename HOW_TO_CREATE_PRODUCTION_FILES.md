# How to Create the Production Files

Before pushing to GitHub and deploying to Render, you need to create 4 files
and update 1 existing file. All of this is done inside the `taskplanner/` folder
(the one that contains `manage.py`).

Open your terminal and navigate there first:

```
cd d:\Rplus\taskplanner
```

---

## File 1 — `.gitignore`

This file tells git which files to ignore and NOT upload to GitHub.

### Create it

```powershell
New-Item .gitignore -ItemType File
```

### Open it and paste this exact content

```
venv/
db.sqlite3
__pycache__/
*.pyc
*.pyo
.env
*.sqlite3
staticfiles/
```

---

## File 2 — `.env`

This file holds your secret settings. It will NOT be uploaded to GitHub
because `.gitignore` excludes it.

### Create it

```powershell
New-Item .env -ItemType File
```

### Generate a secret key first

Run this command in your terminal to get a random secret key:

```
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

It will print a long random string like this (yours will be different):
```
3Kx9mPqL7vJ0wE4uT6yA2sBcD1hGfZ8pW5nRsQeYdXoKbHjLmNt
```

Copy that output.

### Open `.env` and paste this content (replace the key with yours)

```
SECRET_KEY=paste-your-generated-key-here
DEBUG=False
```

---

## File 3 — `requirements.txt`

This file lists all the Python packages the project needs.
You already have this file — you just need to update it.

### Open `requirements.txt` and replace everything in it with this

```
Django>=4.2,<5.0
gunicorn
whitenoise
python-decouple
```

### Then install the new packages

```
pip install -r requirements.txt
```

---

## File 4 — `build.sh`

This is the script Render runs every time it deploys your app.

### Create it

```powershell
New-Item build.sh -ItemType File
```

### Open it and paste this exact content

```bash
#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

---

## File 5 — `taskplanner/settings.py` (update existing)

You do not create this file — it already exists. You need to make
4 changes to it.

Open `taskplanner/settings.py` in your editor.

### Change 1 — Add this line at the very top (line 1)

```python
from decouple import config
```

### Change 2 — Replace the SECRET_KEY and DEBUG lines

Find these lines:
```python
SECRET_KEY = 'django-insecure-taskplanner-change-this-in-production'

DEBUG = True
```

Replace them with:
```python
SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)
```

### Change 3 — Add WhiteNoise to MIDDLEWARE

Find this line inside MIDDLEWARE:
```python
'django.middleware.security.SecurityMiddleware',
```

Add this line directly below it:
```python
'whitenoise.middleware.WhiteNoiseMiddleware',
```

### Change 4 — Add static file settings at the bottom

Find this line near the bottom:
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

Add these two lines directly below:
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## Checklist — Do These in Order

| # | What to do |
|---|-----------|
| 1 | Create `.gitignore` and paste the content |
| 2 | Generate a secret key with the Python command |
| 3 | Create `.env` and paste the content with your secret key |
| 4 | Update `requirements.txt` with the new packages |
| 5 | Run `pip install -r requirements.txt` |
| 6 | Create `build.sh` and paste the content |
| 7 | Make the 4 changes to `taskplanner/settings.py` |
| 8 | Tell me when done so I can verify everything is correct |
