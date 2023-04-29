import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DOCX_TEMPLATE_PATH = os.getenv("DOCX_TEMPLATE_PATH", "./upload")
DOCX_OUTCOMES_PATH = os.getenv("DOCX_OUTCOMES_PATH", "./result")
LIBREOFFICE_BINARY = os.getenv("LIBREOFFICE_BINARY", "/usr/bin/soffice")
SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL", "sqlite:///docx.db")

connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite://"):
    connect_args["check_same_thread"] = False

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
