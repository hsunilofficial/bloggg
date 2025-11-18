# Personal Blog – A Django Project
Because every great developer deserves a place to rant, write, and delete posts at 3 AM.

---

## What Is This?

A fully functional Django-powered personal blog with an admin dashboard, custom user management, and a layout clean enough to make even Django’s default admin blush.
Built with love, caffeine, and probably a few `TemplateDoesNotExist` errors along the way.

---
## Features That Actually Work:

### Blog Goodness

* Write posts
* Edit posts
* Delete posts (when you realize you overshared)
* Categories & tags
* SEO-friendly URLs (Google will like you)

### User & Admin Dashboard

* Custom admin UI
* Add / update / delete users
* No unnecessary pagination clutter
* Cleaner layout than my life decisions

### File & Static Handling

* Full static & media support
* Proper project structure
* Easy deployment configurations

### Ready for the Outside World

* Production-friendly
* Works with Nginx/Gunicorn or whatever you force it through
* `.env` support (please… do NOT upload it to GitHub)

## Project Structure

```
personal_blog/
│── blog/
│   ├── templates/blog/
│   ├── static/blog/
│   ├── views.py
│   ├── urls.py
│   └── models.py
│
│── personal_blog/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
│── requirements.txt
│── manage.py
│── README.md
```

(*Yes, it’s organized. Yes, I’m proud too.*)

---

## Installation Guide (Human-Friendly)

### Step 1: Clone the repo

```bash
git clone https://github.com/yourusername/personal_blog.git
cd personal_blog
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

### Step 3: Activate it

* Windows: `venv\Scripts\activate`
* Mac/Linux: `source venv/bin/activate`

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Migrate like your database depends on it

```bash
python manage.py migrate
```

### Step 6: Create a superuser

```bash
python manage.py createsuperuser
```

### Step 7: Run the server

```bash
python manage.py runserver
```

Boom! You now have a personal blog running locally.

---

### 🧪 Dev Tips From Hard-Earned Experience

* If a template goes missing, check `templates/blog/` first.
* If static files break, run:

  ```bash
  python manage.py collectstatic
  ```
 *Commit often. Push often. Cry rarely.*

---

## 🛠️ Tech Stack

* **Django 5**
* **Python 3.x**
* **HTML / CSS / JS**
* **Bootstrap or Custom UI**
* **SQLite (or grown-up DBs like PostgreSQL)**


---

## 🛡️ License

This project is open-source.
Fork it. Improve it. Break it. Fix it. Repeat.

---

## 📬 Contact

**Made by: Hitha (@hsunilofficial)**
Feel free to open an issue or send PRs (no judgment… mostly).
Just tell me! <3
