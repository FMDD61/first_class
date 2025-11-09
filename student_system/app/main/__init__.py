from flask import Blueprint
main = Blueprint('main', __name__)
from . import routes  # 导入该蓝图的路由
# (任务五) 导入错误处理
from . import errors