import os
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()
scheme = os.getenv("SQLDB_SCHEME")  # Database Scheme
user = os.getenv("SQLDB_USER")  # Database User
password = os.getenv("SQLDB_PASSWORD")  # Database Password
host = os.getenv("SQLDB_HOST")  # Database Host
port = os.getenv("SQLDB_PORT")  # Database Port
dbname = os.getenv("SQLDB_DBNAME")  # Database Name
engine = create_engine(f"{scheme}://{user}:{password}@{host}:{port}/{dbname}")
