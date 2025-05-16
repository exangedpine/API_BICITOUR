from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()  # Esta línea es esencial para cargar las variables del archivo .env

client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client["BiciTour"]
