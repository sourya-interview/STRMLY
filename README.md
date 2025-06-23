```markdown
# 🎬 STRMLY — Video Sharing Platform (Backend + Frontend)

This project replicates the core functionality of a video streaming platform similar to YouTube. It includes:

- ✅ JWT-based authentication system (signup/login/logout)
- ✅ Secure video upload to **Cloudinary**
- ✅ Public video feed with metadata
- ✅ User profile with all uploaded videos
- ✅ Responsive UI using pure HTML/CSS/JS
- ✅ MongoDB Atlas backend integration
- ✅ API and browser-rendered pages
- ✅ Clean folder structure and environment setup

---

## 📁 Folder Structure

```

company-projects/
└── strmly/
├── authentication/       # Signup/Login logic (JWT & password hashing)
├── vid\_upld/             # Video upload & feed
├── templates/            # All HTML pages
├── static/               # CSS/JS and other static files
├── stream/               # Django project core + settings
│   └── cloudinary.py     # Cloudinary config
├── .env                  # 🔐 Your secrets (NOT pushed to GitHub)
├── .env.example          # ✅ Sample .env for others
├── .gitignore
├── manage.py
└── requirements.txt

````

---

## ⚙️ 1. Setup Instructions (For Forkers)

### 📌 Prerequisites

- Python 3.10+
- MongoDB Atlas account (free tier)
- Cloudinary account (free tier)
- Git installed
- A virtual environment (recommended)

---

### 📦 Step-by-Step Setup

#### 🔹 Step 1: Clone the repo

```bash
git clone https://github.com/your-username/STRMLY.git
cd STRMLY
````

#### 🔹 Step 2: Create virtual environment & activate it

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

#### 🔹 Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

#### 🔹 Step 4: Setup your `.env`

Create a `.env` file in the root (`strmly/`) and add the following:

```env
MONGO_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/yourDB
SECRET_KEY=your-django-secret
JWT_SECRET=your-jwt-secret

CLOUD_NAME=your-cloudinary-name
CLOUD_API_KEY=your-cloudinary-key
CLOUD_API_SECRET=your-cloudinary-secret
```

✅ Check `.env.example` for help.

---

### 🔹 Step 5: Connect to MongoDB Atlas

MongoDB is used via **MongoEngine** (ODM). Connection happens in `stream/__init__.py`:

```python
from mongoengine import connect
from dotenv import load_dotenv
import os

load_dotenv()

connect(
    db='strmly',
    host=os.getenv("MONGO_URI"),
    alias='default'
)
```

Make sure your Mongo Atlas cluster is running, and IP whitelisting is enabled for `0.0.0.0/0`.

---

### 🔹 Step 6: Cloudinary Config

Cloudinary credentials are set in `stream/cloudinary.py`:

```python
import cloudinary

cloudinary.config(
    cloud_name = os.getenv("CLOUD_NAME"),
    api_key = os.getenv("CLOUD_API_KEY"),
    api_secret = os.getenv("CLOUD_API_SECRET"),
    secure=True
)
```

---

### 🔹 Step 7: Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to test.

---

## 🔐 Authentication System

* `/signup` – register with `name`, `email`, `password`
* `/login` – returns a JWT token
* JWT is stored in `localStorage`
* Custom decorator `get_user_frm_request(request)` is used to extract the user from the `Authorization` header

### Login Flow:

```js
localStorage.setItem("token", data.token);
```

Authorization header format:

```
Authorization: Bearer <token>
```

---

## 📤 Video Upload (Cloudinary + MongoDB)

* POST `/upload`
* Accepts:

  * Title
  * Description
  * Video file (MP4)
* Video is uploaded to Cloudinary
* Metadata is stored in MongoDB

---

## 📺 Video Feed (Public)

* GET `/videos`
* Returns:

  * Title
  * Cloudinary Video URL
  * Uploader name
  * Upload timestamp
* Rendered using browser template (`video_feed.html`)
* Sorted by newest first

---

## 👤 Profile Page (Protected)

* GET `/profile`
* Header: `Authorization: Bearer <token>`
* Displays:

  * Name, email, password (hidden), joined date
  * All videos uploaded by that user

---

## 🚪 Logout

Handled via JS:

```js
document.getElementById("logout-btn").addEventListener("click", function () {
  localStorage.removeItem("token");
  window.location.href = "/login";
});
```

---

## ⚠️ Security Features

* Passwords are hashed using `bcrypt`
* JWT tokens expire after a set period (optional)
* All protected views validate tokens via headers
* `.env` secrets are used everywhere
* `.gitignore` ensures no sensitive files are committed

---

## 🌐 Frontend

* Plain HTML/CSS/JS (no frameworks)
* Responsive video cards using CSS Grid
* Fully styled:

  * Signup
  * Login
  * Video Upload
  * Feed
  * Profile

---

## 📃 API Overview

| Method | Endpoint   | Description                |
| ------ | ---------- | -------------------------- |
| POST   | `/signup`  | Register new user          |
| POST   | `/login`   | Login and return token     |
| POST   | `/upload`  | Upload video to Cloudinary |
| GET    | `/videos`  | Get public feed            |
| GET    | `/profile` | Get logged-in user info    |

---

## 📝 Notes

* No deployment was required (not hosted).
* You can optionally integrate Firebase or deploy to Render/Vercel later.
* Feel free to build on this foundation!

---

## 📎 License

This project is for educational/demo purposes only.

---

```

```
