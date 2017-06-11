from flask import Blueprint

safehouse_guests = Blueprint('safehouse_guests', __name__)

from . import views
