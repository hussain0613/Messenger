from app import create_app
from app.auth.models import User
from app import db

app = create_app()
ctx = app.test_request_context()


