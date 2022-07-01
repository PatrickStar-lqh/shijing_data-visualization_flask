from flask import Blueprint

sjdv = Blueprint('shijing_dataviz', __name__)

from . import view