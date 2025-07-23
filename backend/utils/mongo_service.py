import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables from .env file
load_dotenv()

# Get MongoDB credentials from environment variables
mongodb_password = os.getenv('MONGODB_PASSWORD')
mongodb_uri_template = os.getenv('MONGODB_URI')

if not mongodb_password:
    raise ValueError("MONGODB_PASSWORD environment variable is not set")
if not mongodb_uri_template:
    raise ValueError("MONGODB_URI environment variable is not set")

# Construct the URI by replacing the password placeholder
uri = mongodb_uri_template.format(MONGODB_PASSWORD=mongodb_password)

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)