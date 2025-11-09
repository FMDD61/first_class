from . import db  # 稍后在 __init__.py 中定义 db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# (注意：login_manager.user_loader 也会移到这里或 __init__)
from . import login_manager # 稍后在 __init__.py 中定义 login_manager

@login_manager.user_loader # 3. 实现一个“用户加载”回调函数，确保 Flask-Login 能在需要时通过ID从数据库中重新获取用户信息。
def load_user(user_id):
    return User.query.get(int(user_id))

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

class Major(db.Model):
    __tablename__ = 'majors'
    id = db.Column(db.Integer, primary_key=True)
    major_name = db.Column(db.String(100), unique=True, nullable=False)
    # 定义"一对多"关系中的"一"
    # 'students' 是反向引用的名称，'major' 是在 BasicInfo 中定义的 backref 名称
    students = db.relationship('BasicInfo', backref='major', lazy='dynamic') # SQLAlchemy的关系应该引用模型类名，而不是表名。
    def __repr__(self):
        return f'<Major {self.major_name}>' # 定义repr方法，返回对象的字符串表示，这里返回专业名称

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