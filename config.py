import os
import getpass
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    RESULTS_FOLDER = os.environ.get('RESULTS_FOLDER') or os.path.join(basedir, 'app','results')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'G3FE8jdstrj87fjfisaqRWAauurjsfSs6r6us'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_DIR = os.environ.get('MAIL_DIR') or ""
    MAIL_PASS = os.environ.get('MAIL_PASS') or getpass.getpass("Password: ")
