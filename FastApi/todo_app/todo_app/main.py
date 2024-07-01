from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Session, create_engine, select, Field
from typing import List, Optional

DATABASE_URL = "postgresql://asadbukhari65813:IXDq4RrEo7KQ@ep-lucky-paper-a5afppuw.us-east-2.aws.neon.tech/poetry_todo?sslmode=require"