from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    port: int = int(os.getenv("PORT" , 8000))
    upload_dir :str = os.getenv("UPLOAD_DIR")
    google_api_key : str = os.getenv("GOOGLE_API_KEY" , "")
    GOOGLE_API_FOR_POLYLINE : str = os.getenv("GOOGLE_API_FOR_POLYLINE" , "")
    
    
    class Config:
        env_file = ".env"
        
        
settings = Settings()