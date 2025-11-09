from flask import render_template, redirect, url_for, flash, request
from . import auth  # 导入当前蓝图实例
from .. import db    # 导入 app 实例
from ..models import User
from ..forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps

def anonymous_required(f):
    """
    装饰器：确保用户未登录时才能访问该路由
    如果用户已登录，则重定向到首页
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash('您已登录，无需再次登录！', 'info')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/register', methods=['GET', 'POST'])
@anonymous_required # 确保用户未登录时才能访问该路由
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('用户名已被注册，请选择其他用户名！', 'danger')
            return render_template('register.html', form=form)
        
        # 创建新用户并设置密码
        user = User(username=form.username.data, role='guest')  # 新用户默认为guest角色
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功！请登录。', 'success')
        # (任务四修复) url_for 必须使用 '蓝图名.端点名'
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
@anonymous_required # 确保用户未登录时才能访问该路由
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('登录成功！', 'success')
            return redirect(url_for('main.index')) # (任务四修复)
        else:
            flash('用户名或密码错误！', 'danger')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required # 确保用户登录后才能访问该路由
def logout():
    logout_user()
    flash('您已成功退出登录。', 'success')
    return redirect(url_for('main.index')) # (任务四修复)