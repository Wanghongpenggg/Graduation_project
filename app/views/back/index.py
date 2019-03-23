from app.views.auth.login import login_required
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import back_blueprint as back_bp

@back_bp.route('/',methods=['GET','POST'])
@login_required
def index():
    return render_template("back/index.html")
