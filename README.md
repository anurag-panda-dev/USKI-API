# USKI API

Unified Serial Killer Information API (USKI API) is a FastAPI project for storing and exposing structured serial killer reference data.

## What this project does

This project provides a lightweight API for managing serial killer reference entries with:
- CRUD endpoints for killer records
- a computed severity score for each entry
- SQLite persistence for local use
- Swagger documentation for testing the API

## Project structure

- `main.py` – FastAPI app and route definitions
- `models.py` – SQLAlchemy database models
- `schemas.py` – Pydantic request and response models
- `crud.py` – database helpers
- `scoring.py` – score calculation logic
- `database.py` – database connection setup
- `seed.py` – optional sample data seeding
- `serial_killers.db` – local SQLite database file

## Requirements

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run locally

From the `src` folder:

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open the docs at:

- http://127.0.0.1:8000/docs

## API endpoints

- `GET /` – basic info endpoint
- `GET /killers` – list killers
- `GET /killers/{id}` – fetch one killer
- `POST /killers` – create a killer
- `PUT /killers/{id}` – update a killer
- `DELETE /killers/{id}` – delete a killer
- `GET /killers/{id}/score` – get the score breakdown

## Database

The API uses a SQLite database file named `serial_killers.db` in this folder by default.

## Export to CSV

To make the database easier to inspect or share on GitHub, run:

```bash
python ../data/export_db_to_csv.py
```

This creates a CSV file at:

- `data/serial_killers.csv`

## Notes

This project is intended for educational and reference use. All data should be sourced from public, verifiable records.
