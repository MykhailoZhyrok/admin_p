from fastapi import Header, HTTPException, Depends
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ['POSTGRES_API_KEY']

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")
