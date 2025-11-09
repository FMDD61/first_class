from flask import Flask, render_template, session, redirect, url_for, flash, request # 导入Flask类和render_template函数（用于渲染模板）    
from flask_bootstrap import Bootstrap # 从flask_bootstrap模块导入Bootstrap类（用于集成Bootstrap框架）   
from flask_wtf import FlaskForm # 从flask_wtf模块导入FlaskForm类（用于创建表单）
from werkzeug.security import generate_password_hash, check_password_hash # 导入密码哈希功能
from wtforms import StringField, SubmitField, SelectField, DateField, IntegerField, PasswordField, BooleanField # 从wtforms模块导入StringField类（用于定义字符串字段）、SubmitField类（用于定义提交按钮）、SelectField类（用于定义选择字段）、DateField类（用于定义日期字段）、IntegerField类（用于定义整数字段）、PasswordField类（用于定义密码字段）、BooleanField类（用于定义布尔字段）
from wtforms.validators import InputRequired, Length, EqualTo # 导入验证器：InputRequired（输入必填）、Length（长度限制）、Email（邮箱格式验证）、EqualTo（字段相等验证）
from flask_sqlalchemy import SQLAlchemy # 从flask_sqlalchemy模块导入SQLAlchemy类（用于数据库操作）
from datetime import datetime
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user # 从flask_login模块导入UserMixin类（用于实现用户认证功能）、LoginManager类（用于登录管理）、login_user函数（用于登录用户）、logout_user函数（用于注销用户）、login_required装饰器（用于保护路由，要求用户登录才能访问）、current_user变量（用于获取当前登录用户）
from functools import wraps

app = Flask(__name__) # 创建Flask应用实例，__name__是当前模块的名称
bootstrap = Bootstrap(app) # 创建Bootstrap实例，将Flask应用实例app作为参数传入
app.config['SECRET_KEY'] = 'hard to guess string' # 设置应用配置项SECRET_KEY，用于表单CSRF保护，防止外部网络攻击，这里设置为一个随机字符串
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Scarlet9961@localhost:3306/studentinfo' # 设置应用配置项SQLALCHEMY_DATABASE_URI，用于指定数据库连接URI，这里设置为MySQL数据库

db = SQLAlchemy(app) # 创建SQLAlchemy实例，将Flask应用实例app作为参数传入，用于数据库操作

login_manager = LoginManager(app) # 创建LoginManager实例，将Flask应用实例app作为参数传入，用于登录管理
login_manager.login_view = 'login' # 设置登录视图，当用户访问需要登录才能访问的路由时，会自动跳转到登录视图，这里设置为login路由

@login_manager.user_loader # 3. 实现一个“用户加载”回调函数，确保 Flask-Login 能在需要时通过ID从数据库中重新获取用户信息。
def load_user(user_id):
    return User.query.get(int(user_id))

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

def admin_required(f):
    """
    装饰器：确保用户具有admin角色才能访问该路由
    如果用户不是admin，则重定向到首页并显示错误提示
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        if current_user.role != 'admin':
            flash('权限不足！只有管理员可以访问此页面。', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

class User(UserMixin, db.Model): # 定义模型类User，继承自UserMixin类（Flask-Login提供的类，用于实现用户认证功能）和db.Model类（SQLAlchemy提供的基类）
    __tablename__ = 'users' # 定义表名，这里设置为users
    id = db.Column(db.Integer, primary_key=True) # 定义列id，整数类型，主键
    username = db.Column(db.String(64), unique=True, nullable=False) # 定义列username，字符串类型，长度为64，唯一，不能为空
    password_hash = db.Column(db.String(255), nullable=False) # 定义列password_hash，字符串类型，长度为255，不能为空
    role = db.Column(db.Enum('admin', 'guest'), default='guest', nullable=False) # 定义角色字段，枚举类型，默认值为guest
    
    def set_password(self, password):
        """设置密码，使用哈希加密"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)


class BasicInfo(db.Model): # 定义模型类BasicInfo，继承自db.Model类（SQLAlchemy提供的基类）
    __tablename__ = 'basicinfo' # 定义表名，这里设置为basicinfo
    StudentID = db.Column(db.Integer, primary_key=True) # 定义列StudentID，整数类型，主键
    Name = db.Column(db.String(255), nullable=False) # 定义列Name，字符串类型，长度为255，不能为空
    Gender = db.Column(db.Enum('male', 'female'), nullable=False) # 定义列Gender，枚举类型，只能取male或female，不能为空
    StudentBirthday = db.Column(db.Date, nullable=False) # 定义列StudentBirthday，日期类型，不能为空
    Age = db.Column(db.Integer, nullable=False) # 定义列Age，整数类型，不能为空
    # 新增外键列
    major_id = db.Column(db.Integer, db.ForeignKey('majors.id'))
    # 注意，这里的外键列名应该与Major模型的主键列名保持一致，即majors.id，且major_id列须在basicinfo中手动添加

class Major(db.Model):
    __tablename__ = 'majors'
    id = db.Column(db.Integer, primary_key=True)
    major_name = db.Column(db.String(100), unique=True, nullable=False)
    # 定义"一对多"关系中的"一"
    # 'students' 是反向引用的名称，'major' 是在 BasicInfo 中定义的 backref 名称
    students = db.relationship('BasicInfo', backref='major', lazy='dynamic') # SQLAlchemy的关系应该引用模型类名，而不是表名。
    def __repr__(self):
        return f'<Major {self.major_name}>' # 定义repr方法，返回对象的字符串表示，这里返回专业名称

class BasicForm(FlaskForm):
    StudentID = StringField('请输入学生学号')
    Name = StringField('请输入学生姓名')
    Gender = SelectField('请选择学生性别', choices=[('male', '男'), ('female', '女')])
    StudentBirthday = DateField('请输入学生出生日期', format='%Y-%m-%d')
    Age = IntegerField('请输入学生年龄')
    # 新增 SelectField，coerce=int 确保表单返回的是整数ID
    major = SelectField('Major', coerce=int)
    submit = SubmitField('提交')

class EditForm(BasicForm):  # 继承自 BasicForm
    submit = SubmitField("修改") 

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[InputRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[InputRequired(), Length(8, 255)])
    confirm_password = PasswordField('确认密码', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('注册')

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[InputRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[InputRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

@app.route('/') # 类中自带route方法，使用@app.route()装饰器定义路由
def index(): #当访问根URL时，调用index函数
    studs = BasicInfo.query.all() # 查询所有学生信息
    majors = Major.query.all() # 查询所有专业
    return render_template('index.html', studs=studs, majors=majors) # 渲染模板index.html，传递参数studs和majors
#分离前后端，将前端页面与后端逻辑分离，前端页面使用HTML、CSS、JavaScript等技术实现，后端逻辑使用Flask框架实现

@app.route('/new', methods=['GET', 'POST']) # 定义路由，当访问/new时，调用new函数
@login_required # 确保用户登录后才能访问该路由
@admin_required # 确保用户具有admin角色才能访问该路由
def new():
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
        return redirect(url_for('index')) # 重定向到根URL，很重要
    return render_template('new.html', form=form) # 渲染模板new.html，在其中渲染表单form


@app.route('/edit/<int:StudentID>', methods=['GET', 'POST']) # 定义路由，当访问/edit/StudentID时，调用edit函数
@login_required # 确保用户登录后才能访问该路由
@admin_required # 确保用户具有admin角色才能访问该路由
def edit(StudentID):
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
        return redirect(url_for('index')) # 重定向到根URL，很重要
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

@app.route('/delete/<int:StudentID>', methods=['GET', 'POST']) # 定义路由，当访问/delete/StudentID时，调用delete函数
@login_required # 确保用户登录后才能访问该路由
@admin_required # 确保用户具有admin角色才能访问该路由
def delete(StudentID):
    stud = BasicInfo.query.get(StudentID)
    db.session.delete(stud)
    db.session.commit()
    flash('学生信息删除成功！')
    return redirect(url_for('index')) # 重定向到根URL，很重要

@app.route("/major/<int:major_id>")
def filter_by_major(major_id):
    # 找到被点击的专业
    major = Major.query.get_or_404(major_id)
    # 使用 'major' 关系的反向查询 'students'
    studs = major.students.all()
    # 复用 index.html 模板，但只传入筛选后的学生
    majors = Major.query.all() # 筛选页面也需要专业列表
    return render_template('index.html', studs=studs, majors=majors)

@app.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
@anonymous_required # 确保用户未登录时才能访问该路由
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('登录成功！', 'success')
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误！', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required # 确保用户登录后才能访问该路由
def logout():
    logout_user()
    flash('您已成功退出登录。', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__': # 当作为主程序运行时
    app.run(debug=True) # 启动应用，开启调试模式
    # 调试模式下，当代码发生改变时，应用会自动重启；同时，Flask会提供详细的错误信息，方便调试
    # 但是，在生产环境下，不应该开启调试模式，因为它会暴露应用的敏感信息
    #flask --debug run 开启调试模式（默认端口5000，且主程序名必须为app.py）
    # 可以通过--port参数指定端口号，例如：flask --debug run --port 8000
    #flask run 关闭调试模式
    #flask --app test --debug run(注：运行主程序名为test.py的flask应用)
    #flask shell 进入包含网站环境上下文的命令行(注：flask主程序名必须为app.py)
    #python -m flask shell 进入包含网站环境上下文的命令行(注：flask主程序名可以任意)
    #from app import BasicInfo, db 导入模型类BasicInfo和数据库实例db
    #stud1 = BasicInfo(StudentID=1002, Name='王三', Gender='male', StudentBirthday='2000-01-01')
    #db.session.add(stud1)  # 添加到数据库会话
    #db.session.commit()  # 提交数据库会话，将数据写入数据库
    #以下为ORM查询语句
    #studs = BasicInfo.query.all()  # 查询所有学生记录
    #studs  # 查看查询结果，会返回列表[<BasicInfo 1>, <BasicInfo 2>, <BasicInfo 3>, <BasicInfo 4>, <BasicInfo 5>, <BasicInfo 1001>]
    #for stud in studs:
    #    print(stud.StudentID, stud.Name, stud.Gender, stud.StudentBirthday, stud.Age)  # 打印每个学生的信息
    #num = BasicInfo.query.count()  # 查询学生记录总数，返回6
    #BasicInfo.query.filter_by(StudentID=1002).first()  # 查询学号为1002的学生记录，返回<BasicInfo 1002>
    #BasicInfo.query.get(1)  # 根据主键查询学生记录，返回<BasicInfo 1>，如果主键不存在，则返回None，不能和filter_by()方法混用