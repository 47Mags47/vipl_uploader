import os 
from dotenv import load_dotenv

def env(param):
    load_dotenv()
    return os.getenv(param)
    