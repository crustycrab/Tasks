from flask import Flask

app = Flask(__name__)

from tasks_app import views
