from dotenv import load_dotenv
from peewee import *
import os

load_dotenv()

db = PostgresqlDatabase(
    os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
)
"""
try:
    db.connect()
    print("good job")
    db.close()
except Exception as e:
    print(f"u made a steak at: {e}")
"""