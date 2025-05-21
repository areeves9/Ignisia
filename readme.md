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