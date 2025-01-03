import reflex as rx
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

config = rx.Config(
    app_name="lending_app",
    db_url=os.getenv("DATABASE_URL"),  # Use os.getenv to get the value
)
