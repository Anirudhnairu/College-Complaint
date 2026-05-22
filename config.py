import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "college-complaint-secret-key"

    SQLALCHEMY_DATABASE_URI = \
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "complaint.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False