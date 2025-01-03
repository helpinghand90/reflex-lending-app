import reflex as rx
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


DATABASE_URL = config("DATABASE_URL")

config = rx.Config(
    app_name="reflex_gpt",
    db_url=os.getenv("DATABASE_URL"),
)