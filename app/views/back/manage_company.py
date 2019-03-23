from flask import g, redirect, render_template, request, session, url_for,current_app,abort
from app import db
from ..back import back_blueprint as back_bp
from ..auth.login import login_required
from ...models.user_info import UserInfo
import json

@back_bp.route('/manage-company',methods=['GET','POST','DELETE'])
@login_required
def manage_company():
    error = None
    render_dict = dict()
    get_page = request.args.get('page',default=1,type=int)  # 当前页数
    if request.method == 'GET':
        part = request.args.get('part',default='verify')
        if part == 'verify':
            pagination = UserInfo.query.filter(UserInfo.verify == 0, UserInfo.is_delete == 0).order_by(
                UserInfo.create_time.desc()) \
                .paginate(get_page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=True)
        else:
            pagination = UserInfo.query.filter(UserInfo.is_delete == 0).order_by(
                UserInfo.create_time.desc()) \
                .paginate(get_page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=True)

        render_dict = {
            "pagination": pagination,
            "part" : part
        }
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass
    return render_template('back/admin/manage_company.html',**render_dict)

@back_bp.route('/manage-company/view',methods=['POST'])
@login_required
def view_company():
    view_id = request.form.get("view_id")
    # print(view_id)
    view_company = UserInfo.query.filter(UserInfo.id==view_id).first()
    company_info={
        "id":view_company.id,
        "company_code":view_company.company_code,
        "company_name":view_company.company_name,
        "company_address":view_company.company_address,
        "postal_code":view_company.postal_code,
        "company_phone":view_company.company_phone,
        "company_mail":view_company.company_mail,
        "area_code":view_company.area_code,
        "verify":view_company.verify,
    }
    return render_template("back/admin/manage_company_part/view_company.html",**company_info)

@back_bp.route('/manage-company/verify',methods=['POST'])
@login_required
def verify_company():
    verify_id = request.form.get("verify_id")
    verify_company = UserInfo.query.filter(UserInfo.id==verify_id).first()
    btn = request.form.get("pass_btn")
    if btn=="pass":
        verify_company.verify=True
    else:
        verify_company.verify=False
    db.session.add(verify_company)
    db.session.commit()
    return redirect(url_for('back.manage_company'))

@back_bp.route('/manage-company/add',methods=['GET','POST'])
@login_required
def add_company():
    if request.method=="GET":
        return render_template("back/admin/manage_company_part/add_company.html")
    elif request.method=="POST":
        new_company = UserInfo()
        new_company.company_code = request.form.get("company_code")
        new_company.company_name = request.form.get("company_name")
        new_company.company_address = request.form.get("company_address")
        new_company.postal_code = request.form.get("postal_code")
        new_company.company_phone = request.form.get("company_phone")
        new_company.company_mail = request.form.get("company_mail")
        new_company.area_code = request.form.get("area_code")
        new_company.user_id = g.user.id
        db.session.add(new_company)
        db.session.commit()
        return redirect(url_for('back.manage_company'))

@back_bp.route('/manage-company/del',methods=['DELETE'])
@login_required
def del_company():
    del_id = request.form.get("del_id")
    del_company = UserInfo.query.filter(UserInfo.id==del_id).first()
    del_company.is_delete=1
    db.session.add(del_company)
    db.session.commit()
    return ""