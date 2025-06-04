# 🔥 Ignisia

**Ignisia** is a Flask-based web application that simulates combustion reactions using [Cantera](https://cantera.org/) and visualizes results such as adiabatic flame temperature and species profiles. Built for engineers, researchers, and curious tinkerers, Ignisia provides a simple interface to explore rich combustion behavior.

---

## 🚀 Features

- 🔐 JWT-based user authentication
- 🧪 Equilibrium flame simulations using Cantera
- 📊 Plot-ready output (flame temperature, species mole fractions)
- 💾 PostgreSQL with Alembic for migrations
- ☁️ Optional S3 upload support (for storing/exporting plots)
- 🔧 Modular Flask app structure with Blueprints
- 🧼 Code quality tools: Black, isort, flake8

---

## 🧱 Tech Stack

| Layer       | Tech              |
|-------------|-------------------|
| Backend     | Flask + SQLAlchemy |
| Auth        | Flask-JWT-Extended |
| DB          | PostgreSQL        |
| Simulation  | Cantera           |
| Migrations  | Flask-Migrate     |
| Frontend    | Chart.js or Plotly (planned) |
| Optional    | AWS S3 for plot uploads      |

---

## 🛠️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ignisia.git
cd ignisia
```

### 2. Create environment

```bash
conda create -n ignisia python=3.11
conda activate ignisia
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
conda install -c cantera cantera  # Cantera must be installed via conda
```

### 4. Environment variables

```bash
cp .env.example .env
```

```bash
# .env
# Flask settings
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://your-db-user@localhost:5432/your-db-name
SQLALCHEMY_TRACK_MODIFICATIONS=False

# JWT configuration
JWT_SECRET_KEY=your-secret-key
JWT_ACCESS_TOKEN_EXPIRES=900 # 15 minutes
JWT_REFRESH_TOKEN_EXPIRES=604800 # 7 days
JWT_COOKIE_SECURE=boolean
JWT_TOKEN_LOCATION=some-strings
JWT_REFRESH_COOKIE_NAME=refresh_token
JWT_COOKIE_SAMESITE=Strict
JWT_COOKIE_CSRF_PROTECT=boolean
JWT_CSRF_IN_COOKIES=boolean
```

### 5. Setup the database

```bash
flask db init        # only once
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the app

```bash
flask run
```


## 🖼 Frontend Setup (Tailwind CSS + Alpine.js + Chart.js via esbuild)

This app uses a single static HTML frontend (`app/static/index.html`) powered by:

- **Tailwind CSS** — Utility-first styling
- **Alpine.js** — Lightweight JS interactivity
- **Chart.js** — Charts and visualizations
- **esbuild** — Fast JS bundling

---

### ⚙️ Prerequisites

- Node.js ≥ 18
- npm (comes with Node)

---

### 📦 Install dependencies

From the project root:

```bash
npm install
```

## ⚙️ Build & Watch Commands

Ignisia uses **Tailwind CSS** and **esbuild** to compile styles and JavaScript. Use the following commands during development or when preparing production builds.

---

### ✅ Run Build

**All you need to do:**

```bash
npm run build
```

### ✅ Tailwind CSS

```bash
npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/output.css --minify
```

### ✅ JavaScript

# Bundle JavaScript into bundle.js
```bash
npx esbuild app/static/js/main.js --bundle --outfile=app/static/js/bundle.js --minify
```