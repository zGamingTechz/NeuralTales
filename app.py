from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import keys

# Definitions
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config['SECRET_KEY'] = keys.secret_key
db = SQLAlchemy(app)
