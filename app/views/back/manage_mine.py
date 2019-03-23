from app.views.auth.login import login_required
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,current_app
)
from . import back_blueprint as back_bp
from app.models.user_info import UserInfo
from app.models.mine_info import MineInfo
from app import db

@back_bp.route('/manage-mine',methods=['GET','POST','DELETE'])
@login_required
def manage_mine():
    error = None
    # mine_info = MineInfo.query.filter(MineInfo.company_id==g.user.id,MineInfo.is_delete==0).all()
    get_page = request.args.get('page',default=1,type=int)  # 当前页数
    if request.method == 'GET':
        pagination = MineInfo.query.filter(MineInfo.company_id==g.user.id,MineInfo.is_delete==0).order_by(MineInfo.create_time.desc())\
            .paginate(get_page, per_page=current_app.config['POSTS_PER_PAGE'],error_out=True)
    elif request.method == 'POST':
        if int(request.form["is_edit"]) == 1:
            mine_id = request.form["edit_id"]
            old_mine = MineInfo.query.filter_by(id=mine_id).first()
            old_mine.mine_code = request.form['mine_code']
            old_mine.mine_name = request.form['mine_name']
            old_mine.mine_loc = request.form['mine_loc']
            db.session.add(old_mine)
        else:
            new_mine = MineInfo()
            new_mine.company_id = g.user.id
            new_mine.mine_code = request.form['mine_code']
            new_mine.mine_name = request.form['mine_name']
            new_mine.mine_loc = request.form['mine_loc']
            db.session.add(new_mine)
        db.session.commit()
        return redirect(url_for('back.manage_mine'))
    elif request.method == 'DELETE':
        mine_id = request.form["del_id"]
        def_mine = MineInfo.query.filter(MineInfo.id == mine_id).first()
        def_mine.is_delete=1
        db.session.add(def_mine)
        db.session.commit()
        return ""
    print(pagination.total)
    return render_template('back/company/manage_mine.html',pagination=pagination)
