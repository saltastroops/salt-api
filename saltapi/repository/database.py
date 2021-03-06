"""The database."""

import os

import databases as databases
import dotenv

dotenv.load_dotenv()

DATABASE_DSN = os.environ["DATABASE_URL"]

database = databases.Database(DATABASE_DSN)
