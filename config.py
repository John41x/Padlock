# config.py
from dotenv import load_dotenv
import os

load_dotenv()   # loads DB_HOST, DB_USER, DB_PASS, DB_NAME from your .env

DB_CONFIG = {
    'host':     os.getenv('DB_HOST'),
    'user':     os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME'),
}
