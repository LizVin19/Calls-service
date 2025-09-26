from pydantic import BaseModel
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()
# load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')
# print('>>> DB URL from .env:', os.getenv('DATABASE_URL'))


class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL")
    sync_database_url: str = os.getenv("SYNC_DATABASE_URL")
    media_root: str = os.getenv('MEDIA_ROOT', str(Path(__file__).resolve().parent.parent / 'media' / 'recordings'))

settings = Settings()
