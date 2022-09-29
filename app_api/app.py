from flask import Flask, render_template
from config import Configuration
from flask import redirect, url_for, request


app = Flask(__name__)
app.config.from_object(Configuration)
