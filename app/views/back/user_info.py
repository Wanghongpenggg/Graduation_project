from app.views.auth.login import login_required
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import back_blueprint as back_bp
from app.models.user_info import UserInfo
from app import db

@back_bp.route('/user-info',methods=['GET','POST'])
@login_required
def user_info():
    error = None
    user_info_exist = True if g.user_info is not None else False
    if request.method == 'POST':
        if not user_info_exist:
            new_user_info = UserInfo(user_id=g.user.id,company_code=request.form['company_code'],company_name=request.form['company_name'],
            company_address=request.form['company_address'],postal_code=request.form['postal_code'],company_phone=request.form['company_phone'],
            company_mail=request.form['company_mail'],area_code=request.form['area_code'])
            db.session.add(new_user_info)
        else:
            old_user_info = UserInfo.query.filter_by(id=g.user_info.id).first()
            old_user_info.company_name=request.form['company_name']
            old_user_info.company_address=request.form['company_address']
            old_user_info.postal_code=request.form['postal_code']
            old_user_info.company_phone=request.form['company_phone']
            old_user_info.company_mail=request.form['company_mail']
            old_user_info.area_code=request.form['area_code']
            db.session.add(old_user_info)
        db.session.commit()
        return redirect(url_for('back.user_info'))
    return render_template('back/company/change_info.html',user_info = g.user_info, user_info_exist=user_info_exist)
