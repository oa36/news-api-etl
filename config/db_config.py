import os

db_config = {
    'drivername': 'postgresql',
    'username': os.getenv("POSTGRES_USER"),
    'password': os.getenv("POSTGRES_PASSWORD"),
    'host': os.getenv("POSTGRES_HOST"),
    'port': os.getenv("POSTGRES_PORT"),
    'database': os.getenv("POSTGRES_DB"),
}