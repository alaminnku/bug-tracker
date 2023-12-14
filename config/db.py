import os
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv

# Load env
load_dotenv(find_dotenv())

# Get the uri
uri = os.environ.get('MONGO_URI')

# Create client
client = MongoClient(uri)

# Get database
db = client['bug-tracker']




