from flask import Flask

app = Flask(__name__)
app.config.from_object('tasks_app.config')

from tasks_app import views
