from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_cors import CORS
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin import AdminIndexView,expose
from flask import redirect, render_template, request,url_for


from stimulsoft_reports.report import StiReport
from stimulsoft_reports.viewer import StiViewer
import plotly.express as px


api =Api(doc='/api/')
db= SQLAlchemy()
cor=CORS()
login_manager=LoginManager()
bcrypt=Bcrypt()




