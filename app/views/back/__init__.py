from flask import Blueprint
back_blueprint = Blueprint('back',__name__)

from . import index,user_info,manage_mine,manage_function,manage_identifier,manage_company
