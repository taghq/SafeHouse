from flask import Blueprint

safehouse = Blueprint('safehouse', __name__)

from . import views
