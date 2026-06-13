# TaskPlanner — Full Project Documentation

---

## Table of Contents

1. [What This Project Is](#1-what-this-project-is)
2. [How the Project Was Created](#2-how-the-project-was-created)
3. [Project File Structure](#3-project-file-structure)
4. [What Every File Does](#4-what-every-file-does)
5. [The Database — How Data Is Stored](#5-the-database--how-data-is-stored)
6. [How Communication Works (Request to Response)](#6-how-communication-works-request-to-response)
7. [How the App Works From Start to Finish](#7-how-the-app-works-from-start-to-finish)
8. [All URL Routes](#8-all-url-routes)
9. [What Was Changed for Production (Render Deployment)](#9-what-was-changed-for-production-render-deployment)
10. [Commands to Create the Production Files](#10-commands-to-create-the-production-files)

---

## 1. What This Project Is

TaskPlanner is a web application built with **Python** and the **Django** framework.

It allows users to:
- Register an account and log in
- Create tasks with a title, due date/time, and priority level (High, Medium, Low)
- Set tasks to repeat (Daily, Weekly, Monthly)
- Get in-app reminders when a task is approaching its due time
- Mark tasks as done or undone
- Edit or delete tasks
- Filter tasks by: All, Today, Pending, Done
- See a progress bar showing how many tasks are completed

Each user only sees their own tasks. No user can see another user's data.

---

## 2. How the Project Was Created

The project was built using the Django framework. Here is what was done to set it up:

### Step 1 — Install Django
```
pip install django
```

### Step 2 — Create the Django project
```
django-admin startproject taskplanner
cd taskplanner
```

This created the outer `taskplanner/` folder (the project root) and an inner `taskplanner/` folder (the project config package).

### Step 3 — Create the tasks app
```
python manage.py startapp tasks
```

This created the `tasks/` folder which contains all the logic for the task management feature.

### Step 4 — Register the app
In `taskplanner/settings.py`, `'tasks'` was added to `INSTALLED_APPS` so Django knows the app exists.

### Step 5 — Build the models, views, forms, templates, and URLs
All the files described in this document were written to build the full feature set.

### Step 6 — Create and run migrations
```
python manage.py makemigrations
python manage.py migrate
```

This created the database tables based on the models defined in `tasks/models.py`.

### Step 7 — Run the development server
```
python manage.py runserver
```

This starts the app locally at `http://127.0.0.1:8000/`.

---

## 3. Project File Structure

```
taskplanner/                        ← Project root (where you run commands from)
│
├── manage.py                       ← Django command-line tool
├── requirements.txt                ← List of Python packages needed
├── build.sh                        ← Script Render uses to deploy the app
├── .gitignore                      ← Files to exclude from git
├── .env                            ← Secret settings (NOT uploaded to git)
│
├── taskplanner/                    ← Project config package
│   ├── __init__.py
│   ├── settings.py                 ← All Django settings/configuration
│   ├── urls.py                     ← Main URL router (entry point for all URLs)
│   ├── wsgi.py                     ← How web servers connect to this app
│   └── asgi.py                     ← Async version of wsgi.py (not used here)
│
├── tasks/                          ← The main app (all task logic lives here)
│   ├── __init__.py
│   ├── models.py                   ← Defines the Task database table
│   ├── views.py                    ← The logic that runs when a URL is visited
│   ├── forms.py                    ← The form used to create and edit tasks
│   ├── urls.py                     ← URL routes specific to the tasks app
│   ├── admin.py                    ← Registers the Task model in Django admin
│   ├── apps.py                     ← App configuration metadata
│   │
│   ├── migrations/                 ← Database migration history
│   │   ├── __init__.py
│   │   └── 0001_initial.py        ← First migration: creates the tasks table
│   │
│   └── templates/tasks/            ← HTML template files (the pages users see)
│       ├── base.html               ← Master layout (navbar, messages wrapper)
│       ├── dashboard.html          ← Main page showing all tasks
│       ├── task_form.html          ← Create / Edit task page
│       ├── login.html              ← Login page
│       └── register.html           ← Registration page
│
└── static/
    └── css/
        └── style.css               ← All styling for the entire app
```

---

## 4. What Every File Does

### `manage.py`
The command-line tool for Django. You use this to run the server, make migrations, create admin users, etc. You never edit this file.

---

### `requirements.txt`
Lists all Python packages this project needs. When someone (or Render) runs `pip install -r requirements.txt`, it installs everything in this file.

Current contents:
```
Django>=4.2,<5.0     ← The web framework
gunicorn             ← The production web server
whitenoise           ← Serves static files (CSS) in production
python-decouple      ← Reads settings from the .env file
```

---

### `.env`
A file that holds sensitive settings that should never be uploaded to GitHub. It is listed in `.gitignore` so git ignores it completely.

Contents:
```
SECRET_KEY=...    ← A long random string Django uses for security (encryption, sessions)
DEBUG=False       ← Turns off debug mode for production
```

---

### `.gitignore`
Tells git which files and folders to ignore when you commit. Files ignored:
- `venv/` — your virtual environment (huge, not needed on GitHub)
- `db.sqlite3` — the local database file
- `.env` — secret settings
- `__pycache__/` — compiled Python bytecode (auto-generated)
- `staticfiles/` — collected static files (auto-generated on deploy)

---

### `taskplanner/settings.py`
The main configuration file for the entire Django project. Key settings:

| Setting | Purpose |
|---------|---------|
| `SECRET_KEY` | A secret string Django uses to sign cookies, sessions, and tokens |
| `DEBUG` | When True, shows detailed error pages. Must be False in production |
| `ALLOWED_HOSTS` | Which domain names can access the app |
| `INSTALLED_APPS` | List of all apps Django should load |
| `MIDDLEWARE` | A chain of layers every request passes through |
| `DATABASES` | Database connection settings (SQLite file) |
| `STATIC_URL` | The URL prefix for CSS/image files |
| `LOGIN_URL` | Where to redirect unauthenticated users |
| `LOGIN_REDIRECT_URL` | Where to send users after they log in |
| `LOGOUT_REDIRECT_URL` | Where to send users after they log out |

---

### `taskplanner/urls.py`
The main URL router. Every incoming request first hits this file.

```python
urlpatterns = [
    path('admin/', admin.site.urls),   # /admin/ → Django admin panel
    path('', include('tasks.urls')),   # Everything else → tasks/urls.py
]
```

---

### `tasks/urls.py`
Defines the specific URL routes for the tasks app:

| URL | View | Name |
|-----|------|------|
| `/` | dashboard | `dashboard` |
| `/create/` | create_task | `create_task` |
| `/edit/<id>/` | edit_task | `edit_task` |
| `/toggle/<id>/` | toggle_task | `toggle_task` |
| `/delete/<id>/` | delete_task | `delete_task` |
| `/login/` | login_view | `login` |
| `/register/` | register_view | `register` |
| `/logout/` | logout_view | `logout` |

---

### `tasks/models.py`
Defines the `Task` database model — this is the blueprint for what a task looks like in the database.

Every task has these fields:

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey → User | Which user owns this task |
| `title` | Text (max 255 chars) | The task name |
| `due_datetime` | DateTime | When the task is due |
| `priority` | Choice: high / medium / low | How important the task is |
| `repeat` | Choice: none / daily / weekly / monthly | How often it repeats |
| `reminder_offset` | Integer (minutes) | How many minutes before due time to show a reminder |
| `is_done` | Boolean | Whether the task is completed |
| `created_at` | DateTime | When the task was created (auto-set) |

The model also has two helper methods:
- `is_overdue()` — returns True if the task is past its due date and not yet done
- `needs_reminder()` — returns True if we are now within the reminder window (e.g. within 30 minutes of due time)

---

### `tasks/forms.py`
Defines `TaskForm`, which is what users fill out when creating or editing a task.

It is a `ModelForm` — Django automatically generates the form fields from the `Task` model. The fields included are: `title`, `due_datetime`, `priority`, `repeat`, `reminder_offset`.

Custom widgets are applied:
- `due_datetime` renders as a browser date/time picker (`datetime-local` input)
- `title` has a placeholder: "Task title…"
- `reminder_offset` has a minimum value of 0

When editing an existing task, the form pre-fills the date/time field with the existing value in the correct format.

---

### `tasks/views.py`
This is the brain of the app. Each function here handles what happens when a URL is visited.

#### `dashboard(request)`
- Requires login
- Reads the `?filter=` query parameter from the URL to decide which tasks to show
- Fetches tasks from the database filtered by the logged-in user
- Calculates the progress percentage (done / total)
- Builds a reminder list of tasks whose reminder window is open
- Passes all this data to `dashboard.html` to be rendered

#### `create_task(request)`
- Requires login
- If the request is GET: shows an empty form
- If the request is POST: validates the form, saves the task (attaching the current user), then redirects to the dashboard

#### `edit_task(request, pk)`
- Requires login
- Loads the specific task by its ID (`pk`), making sure it belongs to the logged-in user
- If GET: shows the form pre-filled with the task's current values
- If POST: validates and saves the updated values

#### `toggle_task(request, pk)`
- Requires login
- Flips `is_done` between True and False
- Redirects back to wherever the user came from (using the HTTP Referer header)

#### `delete_task(request, pk)`
- Requires login
- Deletes the task from the database
- Redirects to the dashboard

#### `login_view(request)`
- If the user is already logged in, redirects to dashboard
- If GET: shows the login form
- If POST: validates credentials, logs the user in, redirects to dashboard

#### `register_view(request)`
- If the user is already logged in, redirects to dashboard
- If POST: creates a new user account and immediately logs them in
- Handles the case where the username is already taken

#### `logout_view(request)`
- Logs the user out
- Redirects to the login page

---

### `tasks/admin.py`
Registers the `Task` model with Django's built-in admin panel at `/admin/`.

Admin users can:
- See tasks listed by: title, user, due date, priority, repeat, done status
- Filter tasks by: priority, repeat, done status
- Search tasks by: title, username

---

### `tasks/templates/tasks/base.html`
The master HTML layout that all other pages inherit from.

Contains:
- The `<head>` with the CSS link
- The navigation bar showing the app name, username, "New Task" button, and Logout button
- A messages section for showing success/error alerts
- A `{% block content %}` placeholder that child templates fill in

---

### `tasks/templates/tasks/dashboard.html`
The main page. Extends `base.html` and fills in the content block with:

1. **Reminder banner** — shows at the top if any tasks need a reminder (overdue or due soon)
2. **Page header** — "My Tasks" heading
3. **Progress bar** — shows "X / Y done" and a visual fill bar
4. **Filter tabs** — All / Today / Pending / Done links
5. **Task list** — each task displayed as a card with:
   - A checkbox to toggle done/undone
   - The task title
   - Due date, priority badge, repeat badge, overdue badge (if applicable)
   - Edit and Delete buttons

---

### `tasks/templates/tasks/task_form.html`
Used for both creating and editing tasks. Shows the `TaskForm` fields and a submit button labeled either "Create" or "Edit" depending on context.

---

### `tasks/templates/tasks/login.html` and `register.html`
Login and registration pages. Both extend `base.html` and display Django's built-in authentication forms.

---

### `static/css/style.css`
Contains all the visual styling for the app. Key design choices:
- Primary color: purple (`#7F77DD`)
- Task priority is shown as a colored left border: red (high), orange (medium), blue (low)
- Completed tasks are shown with reduced opacity and a strikethrough
- Overdue tasks are highlighted with a red background tint
- The layout uses flexbox for alignment

---

### `build.sh`
A shell script Render runs automatically when deploying:
```bash
pip install -r requirements.txt        # Install all packages
python manage.py collectstatic --no-input  # Gather CSS files into staticfiles/
python manage.py migrate               # Apply any database migrations
```

---

## 5. The Database — How Data Is Stored

The app uses **SQLite**, which is a single file (`db.sqlite3`) that acts as the database. Django manages it automatically.

There are two relevant tables:

### `auth_user` (built into Django)
Stores user accounts. Columns: id, username, password (hashed), email, etc.

### `tasks_task` (created by migration `0001_initial.py`)
Stores all tasks. Columns: id, user_id (foreign key to auth_user), title, due_datetime, priority, repeat, reminder_offset, is_done, created_at.

The `user_id` column links every task to the user who created it. When the dashboard loads tasks, it always filters by `user=request.user` to ensure users only see their own tasks.

---

## 6. How Communication Works (Request to Response)

Every interaction in the app follows this exact flow:

```
Browser
  │
  │  HTTP Request (GET or POST) to a URL
  ▼
Django (manage.py / wsgi.py)
  │
  │  Passes through MIDDLEWARE chain:
  │  - SecurityMiddleware (HTTPS headers)
  │  - WhiteNoiseMiddleware (static files)
  │  - SessionMiddleware (reads session cookie)
  │  - CsrfViewMiddleware (checks CSRF token on POST)
  │  - AuthenticationMiddleware (attaches request.user)
  │  - MessageMiddleware (flash messages)
  │
  ▼
taskplanner/urls.py
  │
  │  Matches the URL pattern
  ▼
tasks/urls.py
  │
  │  Matches the specific route, calls the view function
  ▼
tasks/views.py  (the view function runs)
  │
  │  Reads from / writes to the database via models.py
  │  Builds a context dictionary of data
  │
  ▼
HTML Template (dashboard.html, task_form.html, etc.)
  │
  │  Django fills in the template variables with the context data
  │
  ▼
HTTP Response (rendered HTML page)
  │
  ▼
Browser displays the page
```

### GET vs POST

- **GET request** — The browser is asking to *see* a page. No data is being submitted. Used for: loading the dashboard, loading the create/edit form.
- **POST request** — The browser is *submitting data* to the server. Used for: submitting a create/edit form, toggling a task, deleting a task, logging in, logging out.

### CSRF Token
Every POST form in this app includes `{% csrf_token %}`. This is a hidden security token Django checks to confirm the form submission came from this site and not a malicious external site.

### Sessions and Authentication
When a user logs in, Django stores their user ID in a session cookie in the browser. On every subsequent request, Django reads that cookie and sets `request.user` to the logged-in user. The `@login_required` decorator on views checks this — if `request.user` is not authenticated, the user is redirected to `/login/`.

---

## 7. How the App Works From Start to Finish

### A New User's Journey

**1. User visits the app for the first time**
- They go to `/` (the dashboard)
- Django sees `@login_required` — the user is not logged in
- Django redirects them to `/login/`

**2. User clicks "Register"**
- They go to `/register/`
- Django renders `register.html` with Django's `UserCreationForm`
- The user fills in username and password and submits
- Django validates the form, creates a new row in `auth_user`, and immediately logs the user in
- Django redirects to `/` (the dashboard)

**3. Dashboard loads**
- Django calls `dashboard(request)`
- It queries the database: `Task.objects.filter(user=request.user)` — gets all tasks for this user (empty for a new user)
- It calculates progress: 0/0 = 0%
- It checks for reminders: none yet
- It renders `dashboard.html` with the empty task list

**4. User creates a task**
- User clicks "+ New Task" in the navbar → goes to `/create/`
- Django renders `task_form.html` with an empty `TaskForm`
- User fills in: title, due date/time, priority, repeat setting, reminder minutes
- User clicks submit → POST request sent to `/create/`
- Django validates the form data
- Django saves the task: `task.user = request.user` (links it to the logged-in user), then `task.save()`
- Django adds a success flash message: "Task created."
- Django redirects back to the dashboard

**5. Dashboard shows the task**
- The new task appears in the task list with its priority colour, due date, and badges
- The progress bar updates to show 0/1 (0%)

**6. Time passes — reminder triggers**
- When the current time is within `reminder_offset` minutes of the task's due time, `needs_reminder()` returns True
- The dashboard view adds this task to `reminder_list`
- A yellow reminder banner appears at the top of the dashboard showing the task name and due time, labelled "Due soon" or "Overdue"

**7. User marks the task as done**
- User clicks the checkbox on the task card → POST to `/toggle/<id>/`
- `toggle_task` flips `task.is_done` to True and saves
- The task appears with a strikethrough and reduced opacity
- The progress bar increases

**8. User edits a task**
- User clicks "Edit" → GET to `/edit/<id>/`
- Django loads the specific task (verifying it belongs to the logged-in user)
- `task_form.html` renders pre-filled with the task's current values
- User changes something and submits → POST to `/edit/<id>/`
- Django validates, saves the updated task, redirects to dashboard

**9. User deletes a task**
- User clicks "Delete" → a browser confirmation popup appears ("Delete 'task name'?")
- If confirmed: POST to `/delete/<id>/`
- Django deletes the task from the database
- Redirects to dashboard with "Task deleted." flash message

**10. User filters tasks**
- User clicks "Today" filter → GET to `/?filter=today`
- Dashboard view reads `request.GET.get('filter', 'all')` → `'today'`
- Query is narrowed: `qs.filter(due_datetime__date=timezone.localdate())`
- Only today's tasks are shown

**11. User logs out**
- User clicks "Logout" → POST to `/logout/`
- Django calls `logout(request)` — clears the session cookie
- Redirects to `/login/`

---

## 8. All URL Routes

| URL | Method | What it does | Login Required |
|-----|--------|-------------|----------------|
| `/` | GET | Show the dashboard with task list | Yes |
| `/create/` | GET | Show the empty create task form | Yes |
| `/create/` | POST | Save the new task | Yes |
| `/edit/<id>/` | GET | Show the edit form pre-filled | Yes |
| `/edit/<id>/` | POST | Save the edited task | Yes |
| `/toggle/<id>/` | POST | Flip task done/undone | Yes |
| `/delete/<id>/` | POST | Delete the task | Yes |
| `/login/` | GET | Show the login form | No |
| `/login/` | POST | Authenticate and log in | No |
| `/register/` | GET | Show the registration form | No |
| `/register/` | POST | Create account and log in | No |
| `/logout/` | POST | Log out the user | No |
| `/admin/` | GET | Django admin panel | No (admin login) |

---

## 9. What Was Changed for Production (Render Deployment)

The following changes were made to prepare the project for deployment on Render:

### `.gitignore` (new file)
Prevents sensitive and unnecessary files from being uploaded to GitHub.

### `.env` (new file)
Stores the secret key and DEBUG setting outside of the code so they are not exposed on GitHub.

### `requirements.txt` (updated)
Added three production packages:
- `gunicorn` — the WSGI server Render uses to run the app (Django's built-in server is only for development)
- `whitenoise` — serves the CSS/static files directly from Django without needing a separate server like Nginx
- `python-decouple` — reads `SECRET_KEY` and `DEBUG` from the `.env` file

### `taskplanner/settings.py` (updated)
Three changes:
1. `SECRET_KEY` now reads from `.env` instead of being hardcoded
2. `DEBUG` now reads from `.env` (set to False in production)
3. `WhiteNoiseMiddleware` added to MIDDLEWARE to serve static files
4. `STATIC_ROOT` and `STATICFILES_STORAGE` added so `collectstatic` works

### `build.sh` (new file)
A script Render runs on every deploy:
1. Installs all packages from requirements.txt
2. Runs collectstatic to gather CSS into one folder
3. Runs migrate to apply any new database changes

### On Render's dashboard you also need to set:
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn taskplanner.wsgi:application`
- **Environment Variables**: add `SECRET_KEY` and `DEBUG=False` in Render's settings panel (same values as your `.env` file)

---

## 10. Commands to Create the Production Files

All commands below must be run inside the `taskplanner/` folder (where `manage.py` is).
Open your terminal, navigate there first:

```
cd d:\Rplus\taskplanner
```

---

### Create `.gitignore`

**Windows (PowerShell):**
```powershell
New-Item .gitignore -ItemType File
```

Then open the file and paste this content into it:
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

### Create `.env`

**Windows (PowerShell):**
```powershell
New-Item .env -ItemType File
```

Then open the file and paste this content into it:
```
SECRET_KEY=replace-this-with-a-long-random-string-of-50-or-more-characters
DEBUG=False
```

> **Important:** Replace the `SECRET_KEY` value with a real random string.
> You can generate one by running this Python command in your terminal:
> ```
> python -c "import secrets; print(secrets.token_urlsafe(50))"
> ```
> Copy the output and paste it as the value of `SECRET_KEY`.

---

### Create `requirements.txt`

**Windows (PowerShell):**
```powershell
New-Item requirements.txt -ItemType File
```

Then open the file and paste this content into it:
```
Django>=4.2,<5.0
gunicorn
whitenoise
python-decouple
```

Or, if you want to let pip write it automatically from your current environment:
```
pip freeze > requirements.txt
```

> **Note:** `pip freeze` includes every package installed in your environment.
> It is safer to write the file manually with only the packages you actually need.

---

### Create `build.sh`

**Windows (PowerShell):**
```powershell
New-Item build.sh -ItemType File
```

Then open the file and paste this content into it:
```bash
#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

---

### Install the new packages

After updating `requirements.txt`, install the packages into your virtual environment:

```
pip install -r requirements.txt
```

---

### Full order to run everything

Do these steps in this exact order:

| Step | Command / Action |
|------|-----------------|
| 1 | `cd d:\Rplus\taskplanner` |
| 2 | Create `.gitignore` and paste the content shown above |
| 3 | Create `.env` and paste the content shown above (with your real SECRET_KEY) |
| 4 | Create or update `requirements.txt` with the content shown above |
| 5 | Create `build.sh` and paste the content shown above |
| 6 | `pip install -r requirements.txt` |
| 7 | Update `settings.py` as described in Section 9 |
| 8 | `git init` |
| 9 | `git add .` |
| 10 | `git commit -m "initial commit"` |
| 11 | Create a GitHub repo and push to it |
| 12 | Connect the GitHub repo to Render and deploy |
