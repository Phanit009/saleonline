from pydantic_settings import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "ectomeres"
    jwt_secret_key: str = "your-secret-key-change-this"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    cors_origins: List[str] = ["http://localhost:3000"]
    storage_type: str = "local"
    storage_path: str = "./uploads"
    s3_bucket_name: str = ""
    s3_region: str = "us-east-1"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""

    class Config:
        env_file = ".env"

settings = Settings()

if isinstance(settings.cors_origins, str):
    settings.cors_origins = json.loads(settings.cors_origins)
