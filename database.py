import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse
import socket

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from supabase import create_client, Client

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

def _get_ipv4_url(url: str) -> str:
    parsed = urlparse(url)
    hostname = parsed.hostname
    port = parsed.port or 5432
    
    try:
        ips = socket.getaddrinfo(hostname, port, socket.AF_INET, socket.SOCK_STREAM)
        ipv4 = ips[0][4][0]
        netloc = f"{parsed.username}:{parsed.password}@{ipv4}:{port}" if parsed.password else f"{parsed.username}@{ipv4}:{port}"
        query = f"sslmode=require"
        if parsed.query:
            query += "&" + parsed.query
        return f"{parsed.scheme}://{netloc}{parsed.path}?{query}"
    except Exception:
        return url

FIXED_DATABASE_URL = _get_ipv4_url(DATABASE_URL)

engine = create_engine(
    FIXED_DATABASE_URL,
    pool_pre_ping=True,
    future=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()