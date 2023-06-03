import os


class Config:
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    server = os.getenv("POSTGRES_SERVER", "db")
    db = os.getenv("POSTGRES_DB", "test_db")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@{server}:5432/{db}"
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")


class TestConfig:
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    db = os.getenv("POSTGRES_DB", "test_db")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@localhost:5433/{db}"
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
