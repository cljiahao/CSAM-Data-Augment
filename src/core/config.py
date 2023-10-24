import os
import json
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:

    GOOD_QUANTITY : int = os.getenv('GOOD_QUANTITY') 
    NG_QUANTITY : int = os.getenv('NG_QUANTITY') 
    OTHER_QUANTITY : int = os.getenv('OTHER_QUANTITY') 

    IMG_TYPE: list = json.loads(os.getenv("IMG_TYPE"))

settings = Settings()