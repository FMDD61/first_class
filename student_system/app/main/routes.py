from flask import render_template, redirect, url_for, flash
from . import main
from .. import db
from ..models import BasicInfo, Major
from ..forms import BasicForm, EditForm
from flask_login import login_required, current_user # (用于权限控制)
from datetime import datetime

@main.route('/') # 类中自带route方法，使用@app.route()装饰器定义路由
def index(): #当访问根URL时，调用index函数
    studs = BasicInfo.query.all() # 查询所有学生信息
    majors = Major.query.all() # 查询所有专业
    return render_template('index.html', studs=studs, majors=majors) # 渲染模板index.html，传递参数studs和majors
#分离前后端，将前端页面与后端逻辑分离，前端页面使用HTML、CSS、JavaScript等技术实现，后端逻辑使用Flask框架实现

@main.route('/new', methods=['GET', 'POST']) # 定义路由，当访问/new时，调用new函数
@login_required # 确保用户登录后才能访问该路由
def new():
    #  (任务五 权限控制)
    if current_user.role != 'admin':
        flash('您没有权限执行此操作')
        return redirect(url_for('main.index'))
    form = BasicForm()
    # 动态填充选项：(value, label) ，使用 major_name 作为显示文本
    form.major.choices = [(m.id, m.major_name) for m in Major.query.order_by('major_name').all()]
    if form.validate_on_submit():
        stud = BasicInfo(StudentID=form.StudentID.data, 
                         Name=form.Name.data, 
                         Gender=form.Gender.data, 
                         StudentBirthday=form.StudentBirthday.data, 
                         Age=form.Age.data, 
                         major_id=form.major.data) # 直接使用表单中的major ID值
        db.session.add(stud)
        db.session.commit()
        flash('学生信息添加成功！')
        return redirect(url_for('main.index')) # (任务四修复) 重定向到根URL，很重要
    return render_template('new.html', form=form) # 渲染模板new.html，在其中渲染表单form


@main.route('/edit/<int:StudentID>', methods=['GET', 'POST']) # 定义路由，当访问/edit/StudentID时，调用edit函数
@login_required # 确保用户登录后才能访问该路由
def edit(StudentID):
    #  (任务五 权限控制)
    if current_user.role != 'admin':
        flash('您没有权限执行此操作')
        return redirect(url_for('main.index'))
    stud = BasicInfo.query.get(StudentID)
    form = EditForm()
    # 同样需要动态填充选项
    form.major.choices = [(m.id, m.major_name) for m in Major.query.order_by('major_name').all()]
    if form.validate_on_submit():
        stud.StudentID = form.StudentID.data
        stud.Name = form.Name.data
        stud.Gender = form.Gender.data
        stud.StudentBirthday = form.StudentBirthday.data # 直接使用datetime对象，不需要转换为字符串
        stud.Age = form.Age.data
        stud.major_id = form.major.data # 直接使用表单中的major ID值
        db.session.commit()
        flash('学生信息更新成功！')
        return redirect(url_for('main.index')) # (任务四修复) 重定向到根URL，很重要
    form.StudentID.data = stud.StudentID
    form.Name.data = stud.Name
    form.Gender.data = stud.Gender
    # 处理StudentBirthday字段，确保它是datetime对象
    if hasattr(stud.StudentBirthday, 'strftime'):
        form.StudentBirthday.data = stud.StudentBirthday
    else:
        # 如果是字符串，转换为datetime对象
        form.StudentBirthday.data = datetime.strptime(str(stud.StudentBirthday), '%Y-%m-%d')
    form.Age.data = stud.Age
    # 页面加载时，设置下拉框的默认选中项
    if stud.major:
        form.major.data = stud.major_id
    return render_template('edit.html', form=form) # 渲染模板edit.html，在其中渲染表单form

@main.route('/delete/<int:StudentID>', methods=['GET', 'POST']) # 定义路由，当访问/delete/StudentID时，调用delete函数
@login_required # 确保用户登录后才能访问该路由
def delete(StudentID):
    #  (任务五 权限控制)
    if current_user.role != 'admin':
        flash('您没有权限执行此操作')
        return redirect(url_for('main.index'))
    stud = BasicInfo.query.get(StudentID)
    db.session.delete(stud)
    db.session.commit()
    flash('学生信息删除成功！')
    return redirect(url_for('main.index')) # (任务四修复) 重定向到根URL，很重要

@main.route("/major/<int:major_id>")
def filter_by_major(major_id):
    # 找到被点击的专业
    major = Major.query.get_or_404(major_id)
    # 使用 'major' 关系的反向查询 'students'
    studs = major.students.all()
    # 复用 index.html 模板，但只传入筛选后的学生
    majors = Major.query.all() # 筛选页面也需要专业列表
    return render_template('index.html', studs=studs, majors=majors)