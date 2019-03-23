from flask import render_template,redirect,session,url_for,request,flash,g
from . import auth_blueprint as auth_bp
from ... import db
from ...models.user import User
from ...models.function_bar import FunctionBar
import functools


@auth_bp.route('/login',methods=('GET','POST'))
def login():  # 登陆页面
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter(User.username == username,User.is_delete==0).first()  # 查找登陆的账户是否存在
        if user is None:
            error = "该用户不存在"
        elif not user.verify_password(password):
            error = "密码错误"

        if error is None :  # 登陆成功，设置session
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('back.index'))
        flash(error)
    return render_template("auth/login.html")  # 如果是GET则是正常访问，为其渲染页面


@auth_bp.route("/register",methods=("GET","POST"))
def register(): #注册页面
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
            error = '用户名是必须的'
        elif not password:
            error = '密码是必须的'
        elif User.query.filter(User.username==username,User.is_delete==0).first()  is not None:  # 查询是否存在相同用户名的账户
            error = '用户 {} 已被注册'.format(username)

        if error is None:  # 一切ok，写入数据库
            new_user = User(username=username,password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template("auth/register.html")  # 如果是GET则是正常访问，为其渲染页面

@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter(User.id==user_id,User.is_delete==0).first()
        g.function_list = FunctionBar.query.filter(FunctionBar.genre<=g.user.genre , FunctionBar.is_delete==0).all()
        g.user_info = g.user.user_info
        # print("===============")
        # print(g.user_info)
        # print("===============")

@auth_bp.route("/logout",methods=("GET",))
def logout():  # 注销
    session.clear()
    return redirect(url_for("auth.login"))


def login_required(view):  # 登陆判断
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view