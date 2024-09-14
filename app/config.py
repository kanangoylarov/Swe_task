# app/config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'thisissecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
