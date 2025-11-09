import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Scarlet9961@localhost:3306/studentinfo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
