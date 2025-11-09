from app import create_app, db
from app.models import User, BasicInfo, Major
 
app = create_app()
 
# (推荐) 添加 shell 上下文，方便调试
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, BasicInfo=BasicInfo, Major=Major)
 
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