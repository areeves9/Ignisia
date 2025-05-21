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
FLASK_APP=run.py
FLASK_ENV=development
JWT_SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://your_user@localhost:5432/ignisia
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