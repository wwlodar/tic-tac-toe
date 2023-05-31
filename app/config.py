import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    server = os.getenv("POSTGRES_SERVER", "db")
    db = os.getenv("POSTGRES_DB", "test_db")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@localhost:5432/{db}"
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
