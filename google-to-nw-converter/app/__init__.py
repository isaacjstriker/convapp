from flask import Flask

app = Flask(__name__)

from app.main import *  # Import routes from main.py to register them with the app