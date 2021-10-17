import os
from datetime import timedelta

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/team_project'
SQLALCHEMY_TRACK_MODIFICATIONS = False

expires_access = timedelta(minutes=20)
expires_refresh = timedelta(days=7)
