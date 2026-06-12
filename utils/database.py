from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from utils.config_handler import db_conf

# 从 YAML 中拼装 MySQL 连接 URL
mysql_conf = db_conf.get("mysql", {})
DATABASE_URL = f"mysql+pymysql://{mysql_conf.get('user')}:{mysql_conf.get('password')}@{mysql_conf.get('host')}:{mysql_conf.get('port')}/{mysql_conf.get('database')}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=mysql_conf.get("pool_pre_ping", True),
    pool_size=mysql_conf.get("pool_size", 10),
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()