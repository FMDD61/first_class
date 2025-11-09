from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, DateField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo


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