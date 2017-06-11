from flask import Blueprint

safehouse_hosts = Blueprint('safehouse_hosts', __name__)

from . import views
