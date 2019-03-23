from app.views.auth.login import login_required
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,current_app
)
from . import back_blueprint as back_bp
from app.models.function_bar import FunctionBar
from app import db
from math import ceil


@back_bp.route('/manage-function',methods=['GET','POST','DELETE'])
@login_required
def manage_function():
    error = None
    #function_list = FunctionBar.query.filter(FunctionBar.is_delete==0).all()
    get_page = request.args.get('page',default=1,type=int)  # 当前页数

    if request.method == 'GET':
        pagination = FunctionBar.query.filter(FunctionBar.is_delete==0).order_by(FunctionBar.create_time.desc())\
            .paginate(get_page, per_page=current_app.config['POSTS_PER_PAGE'],error_out=True)

    elif request.method == 'POST':
        if int(request.form["is_edit"])==1:
            function_id = request.form["edit_id"]
            old_function = FunctionBar.query.filter(FunctionBar.id==function_id).first()
            old_function.function_text = request.form["function_text"]
            old_function.function_url = request.form["function_url"]
            old_function.genre = request.form["genre"]
            db.session.add(old_function)
        else:
            new_function = FunctionBar()
            new_function.function_text = request.form["function_text"]
            new_function.function_url = request.form["function_url"]
            new_function.genre = request.form["genre"]
            db.session.add(new_function)
        db.session.commit()
        return redirect(url_for('back.manage_function'))
    elif request.method == 'DELETE':
        function_id = request.form["del_id"]
        del_function = FunctionBar.query.filter(FunctionBar.id == function_id).first()
        del_function.is_delete = 1
        db.session.add(del_function)
        db.session.commit()
        return ""
    # render_dict = {
    #     "function_list" : function_list,
    #     "function_num" : function_num,
    #     "page_num" : page_num,
    #     "this_page" : this_page
    # }
    render_dict = {
        "pagination": pagination
    }
    return render_template('back/admin/change_sidebar.html',**render_dict)
