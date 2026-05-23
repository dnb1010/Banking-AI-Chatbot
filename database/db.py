from sqlalchemy import create_engine

DB_USER = "root"
DB_PASSWORD = "10102006"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "banking_db"

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine= create_engine(DATABASE_URL)
